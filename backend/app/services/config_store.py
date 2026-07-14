"""配置持久化存储 — 全部 Web 可配置"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class SettingsStore:
    """持久化配置存储

    所有通过 Web 页面修改的配置保存到 /data/config.json
    优先级: 持久化配置 > 环境变量 > 默认值
    """

    def __init__(self, data_dir: str = "/data"):
        self._path = Path(data_dir) / "config.json"
        self._config: dict[str, Any] = {}
        self._load()

    def _load(self):
        """从文件加载配置"""
        if self._path.exists():
            try:
                self._config = json.loads(self._path.read_text())
                logger.info("已加载持久化配置 (%d 项)", len(self._config))
            except Exception as e:
                logger.error("加载配置失败: %s", e)
                self._config = {}

    def _save(self):
        """保存配置到文件"""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(self._config, indent=2, ensure_ascii=False)
        )

    # === 读取 ===

    def get(self, key: str, default: str = "") -> str:
        return str(self._config.get(key, default))

    def get_all(self) -> dict[str, Any]:
        return dict(self._config)

    # === 写入 ===

    def set(self, key: str, value: str):
        if value:
            self._config[key] = value
        else:
            self._config.pop(key, None)
        self._save()

    def set_many(self, items: dict[str, str]):
        for k, v in items.items():
            if v:
                self._config[k] = v
            else:
                self._config.pop(k, None)
        self._save()

    # === 分类读取 ===

    @property
    def qb(self) -> dict[str, str]:
        return {
            "host": self.get("qb_host"),
            "port": self.get("qb_port", "8080"),
            "username": self.get("qb_username"),
            "password": self.get("qb_password"),
        }

    @property
    def telegram(self) -> dict[str, str]:
        return {
            "bot_token": self.get("tg_bot_token"),
            "chat_id": self.get("tg_chat_id"),
        }

    @property
    def discord(self) -> str:
        return self.get("discord_webhook")

    @property
    def emby(self) -> dict[str, str]:
        return {
            "host": self.get("emby_host"),
            "api_key": self.get("emby_api_key"),
        }

    @property
    def proxy(self) -> str:
        return self.get("proxy_url")

    @property
    def pt_cookies(self) -> dict[str, dict[str, str]]:
        """读取 PT 站点配置"""
        import json as _json
        pt_path = self._path.parent / "pt_sites.json"
        if pt_path.exists():
            try:
                return _json.loads(pt_path.read_text())
            except Exception:
                pass
        return {}


# 全局单例
store = SettingsStore()