"""下载服务 — qBittorrent 集成（重写）

修复:
1. 新版 qBittorrent 4.6+ 强制校验 Referer
2. Session 复用（SID cookie），避免每次操作都重新登录
3. 错误分级诊断（网络不可达/鉴权失败/Referer 被拒/API 版本不兼容）
"""

from __future__ import annotations

import logging
import re
from typing import Any

import httpx

from ..config import settings

logger = logging.getLogger(__name__)


# 错误类型常量
ERR_NETWORK = "network_unreachable"       # 无法连接
ERR_AUTH = "auth_failed"                  # 用户名密码错误
ERR_REFERER = "referer_blocked"           # Referer 校验失败
ERR_API = "api_version_mismatch"          # API 版本不兼容
ERR_UNKNOWN = "unknown"                   # 其他


class QBConnectionError(Exception):
    """qBittorrent 连接异常"""
    def __init__(self, error_type: str, message: str, detail: Any = None):
        self.error_type = error_type
        self.message = message
        self.detail = detail
        super().__init__(f"[{error_type}] {message}")


class DownloaderService:
    """qBittorrent 下载管理（带 Session 复用 + 错误分类）"""

    def __init__(self):
        if not settings.qb_host:
            self._configured = False
            return

        self._configured = True
        self._base_url = f"http://{settings.qb_host}:{settings.qb_port}"
        self._sid: str | None = None  # 复用的 Session ID

        # 统一客户端，带 Referer/Origin 头（qb 4.6+ 强制要求）
        self._client = httpx.AsyncClient(
            timeout=15,
            headers={
                "Referer": f"{self._base_url}/",
                "Origin": self._base_url,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            },
        )

    # ── Session 管理 ──────────────────────────────────────────

    def _cookies_to_header(self) -> dict[str, str]:
        """把 SID 附加到请求头"""
        if self._sid:
            return {"Cookie": f"SID={self._sid}"}
        return {}

    async def _ensure_session(self) -> None:
        """确保有有效 Session，过期则重新登录"""
        if self._sid:
            # 快速检查 Session 是否仍有效
            try:
                resp = await self._client.get(
                    f"{self._base_url}/api/v2/app/version",
                    headers=self._cookies_to_header(),
                    timeout=5,
                )
                if resp.status_code == 200:
                    return  # Session 有效
            except Exception:
                pass  # 连接异常，重新登录

        # 重新登录
        await self._login()

    async def _login(self) -> None:
        """登录并保存 SID"""
        try:
            resp = await self._client.post(
                f"{self._base_url}/api/v2/auth/login",
                data={"username": settings.qb_username, "password": settings.qb_password},
            )

            if resp.status_code == 200:
                # 从 Set-Cookie 提取 SID
                set_cookie = resp.headers.get("set-cookie", "")
                sid_match = re.search(r"SID=([^;]+)", set_cookie)
                if sid_match:
                    self._sid = sid_match.group(1)
                    logger.info("qBittorrent 登录成功，SID 已缓存")
                else:
                    # 某些版本可能直接返回文本
                    self._sid = resp.text.strip()
                    logger.info("qBittorrent 登录成功（无 SID cookie）")
            elif resp.status_code == 403:
                # 403 可能是 Referer 被拒 或 用户名密码错
                # qB 4.6+ 的登录接口 403 通常意味着 Referer 校验失败
                raise QBConnectionError(
                    ERR_REFERER,
                    "qBittorrent 返回 403（可能因 Referer 校验，或登录凭据错误）",
                    {"status_code": 403, "response": resp.text[:200]},
                )
            else:
                raise QBConnectionError(
                    ERR_AUTH,
                    f"qBittorrent 登录失败，HTTP {resp.status_code}",
                    {"status_code": resp.status_code, "response": resp.text[:200]},
                )
        except httpx.ConnectError as e:
            raise QBConnectionError(
                ERR_NETWORK,
                f"无法连接到 qBittorrent ({settings.qb_host}:{settings.qb_port})",
                {"error": str(e)},
            ) from e
        except httpx.TimeoutException as e:
            raise QBConnectionError(
                ERR_NETWORK,
                f"连接 qBittorrent 超时 ({settings.qb_host}:{settings.qb_port})",
                {"error": str(e)},
            ) from e

    # ── 对外 API ──────────────────────────────────────────────

    async def check_connection(self) -> dict[str, Any]:
        """检测连通性（分级诊断）

        返回:
            connected: bool
            version: str (仅 success)
            error_type: str (仅失败)
            error_message: str (仅失败)
            detail: dict (仅失败，排查用)
        """
        if not self._configured:
            return {
                "connected": False,
                "error_type": ERR_NETWORK,
                "error_message": "qBittorrent 未配置，请在设置中填写地址",
            }

        try:
            # 先尝试获取版本（无需登录）
            resp = await self._client.get(
                f"{self._base_url}/api/v2/app/version",
                timeout=5,
            )
            if resp.status_code == 200:
                return {"connected": True, "version": resp.text.strip()}

            # 401 → 需要登录，尝试登录后再测
            if resp.status_code == 401 or resp.status_code == 403:
                try:
                    await self._login()
                    resp2 = await self._client.get(
                        f"{self._base_url}/api/v2/app/version",
                        headers=self._cookies_to_header(),
                        timeout=5,
                    )
                    if resp2.status_code == 200:
                        return {"connected": True, "version": resp2.text.strip()}
                    return {
                        "connected": False,
                        "error_type": ERR_AUTH,
                        "error_message": "qBittorrent 登录失败，请检查用户名和密码",
                        "detail": {"status_code": resp2.status_code},
                    }
                except QBConnectionError as e:
                    return {
                        "connected": False,
                        "error_type": e.error_type,
                        "error_message": e.message,
                        "detail": e.detail,
                    }

            return {
                "connected": False,
                "error_type": ERR_UNKNOWN,
                "error_message": f"qBittorrent 返回 HTTP {resp.status_code}",
                "detail": {"status_code": resp.status_code},
            }

        except httpx.ConnectError:
            return {
                "connected": False,
                "error_type": ERR_NETWORK,
                "error_message": f"无法连接到 {settings.qb_host}:{settings.qb_port}，请确认地址和端口正确",
            }
        except httpx.TimeoutException:
            return {
                "connected": False,
                "error_type": ERR_NETWORK,
                "error_message": f"连接 {settings.qb_host}:{settings.qb_port} 超时，请检查防火墙或网络",
            }
        except Exception as e:
            return {
                "connected": False,
                "error_type": ERR_UNKNOWN,
                "error_message": str(e)[:100],
            }

    async def check_version_compatibility(self) -> dict[str, Any]:
        """检查 API 版本兼容性"""
        if not self._configured:
            return {"compatible": False, "error": "未配置"}

        try:
            await self._ensure_session()
            # 获取 WebUI 版本
            resp = await self._client.get(
                f"{self._base_url}/api/v2/app/webapiVersion",
                headers=self._cookies_to_header(),
                timeout=5,
            )
            if resp.status_code == 200:
                api_ver = resp.text.strip()
                # qB 4.6+ 的 API 版本 >= 2.9
                major = 0
                try:
                    major = int(api_ver.split(".")[0])
                except (ValueError, IndexError):
                    pass
                compatible = major >= 2
                return {
                    "compatible": compatible,
                    "api_version": api_ver,
                    "note": "兼容" if compatible else "API 版本过低，建议升级 qBittorrent",
                }

            return {
                "compatible": False,
                "api_version": "unknown",
                "error": f"HTTP {resp.status_code}",
            }
        except QBConnectionError as e:
            return {"compatible": False, "error": e.message}
        except Exception as e:
            return {"compatible": False, "error": str(e)[:100]}

    async def add_torrent(self, torrent_url: str, save_path: str = "", category: str = "") -> dict[str, Any]:
        """添加种子下载"""
        if not self._configured:
            return {"success": False, "error_type": ERR_NETWORK, "error": "未配置下载器"}

        try:
            await self._ensure_session()
            data: dict[str, str] = {"urls": torrent_url}
            if save_path:
                data["savepath"] = save_path
            if category:
                data["category"] = category
            resp = await self._client.post(
                f"{self._base_url}/api/v2/torrents/add",
                headers=self._cookies_to_header(),
                data=data,
            )
            if resp.status_code == 200:
                logger.info("添加下载成功: %s", torrent_url[:50])
                return {"success": True}
            elif resp.status_code == 403:
                return {
                    "success": False,
                    "error_type": ERR_REFERER,
                    "error": "Referer 校验失败，请联系开发者",
                }
            else:
                return {
                    "success": False,
                    "error_type": ERR_UNKNOWN,
                    "error": f"HTTP {resp.status_code}",
                }
        except QBConnectionError as e:
            return {"success": False, "error_type": e.error_type, "error": e.message}
        except Exception as e:
            logger.error("添加下载异常: %s", e)
            return {"success": False, "error_type": ERR_UNKNOWN, "error": str(e)[:100]}

    async def get_torrents(self, filter: str = "all") -> list[dict]:
        """获取种子列表"""
        if not self._configured:
            return []
        try:
            await self._ensure_session()
            resp = await self._client.get(
                f"{self._base_url}/api/v2/torrents/info",
                headers=self._cookies_to_header(),
                params={"filter": filter},
            )
            return resp.json() if resp.status_code == 200 else []
        except QBConnectionError:
            return []
        except Exception as e:
            logger.error("获取种子列表异常: %s", e)
            return []

    async def get_torrent(self, hash: str) -> dict | None:
        """获取单个种子详情"""
        torrents = await self.get_torrents()
        for t in torrents:
            if t.get("hash") == hash:
                return t
        return None

    async def delete_torrent(self, hash: str, delete_files: bool = False) -> dict[str, Any]:
        """删除种子"""
        if not self._configured:
            return {"success": False, "error": "未配置"}
        try:
            await self._ensure_session()
            resp = await self._client.post(
                f"{self._base_url}/api/v2/torrents/delete",
                headers=self._cookies_to_header(),
                data={"hashes": hash, "deleteFiles": "true" if delete_files else "false"},
            )
            return {"success": resp.status_code == 200}
        except QBConnectionError as e:
            return {"success": False, "error": e.message}
        except Exception as e:
            return {"success": False, "error": str(e)[:100]}