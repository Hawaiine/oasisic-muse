<template>
  <div class="library-page">
    <h1 class="page-title">媒体库</h1>
    <div class="placeholder">
      <p>已刮削的资源将在此显示</p>
      <p class="hint">对接 EMBY/Jellyfin 后自动同步媒体库信息</p>
    </div>
  </div>
</template>

<style scoped>
.library-page { max-width: 800px; }
.page-title { font-size: 24px; margin-bottom: 20px; color: #e1e8ed; }
.placeholder { text-align: center; padding: 60px 20px; background: #1a1f2e; border-radius: 12px; }
.placeholder p { font-size: 16px; color: #8899a6; margin-bottom: 8px; }
.hint { font-size: 13px; color: #556; }
</style>