<template>
  <div class="header">
    <div class="header-left">
      <h2>毕业论文滚滚滚</h2>
      <p>OpenClaw 论文生成引擎</p>
    </div>
    <div class="header-right">
      <span class="quota">剩余次数：{{ quota }}</span>
      <button @click="$emit('logout')" class="logout-btn">退出登录</button>
    </div>
  </div>
</template>

<script setup>
defineProps(['quota'])
defineEmits(['logout'])
</script>

<style scoped>
/* 整体头部容器 */
.header {
  width: 100%;
  height: 70px;
  background: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 32px;
  box-sizing: border-box;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 999;
  backdrop-filter: blur(6px);
}

/* 左侧标题区域 */
.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-left h2 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  padding: 0;
}

.header-left p {
  font-size: 13px;
  color: #6b7280;
  margin: 0;
  padding: 0;
}

/* 右侧信息与按钮 */
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.quota {
  font-size: 14px;
  color: #4b5563;
}

.logout-btn {
  padding: 8px 16px;
  background-color: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background-color: #e5e7eb;
  border-color: #9ca3af;
}
</style>