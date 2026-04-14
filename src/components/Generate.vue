<template>
  <div class="fullscreen-bg"></div>
  <canvas class="particle-canvas left" ref="leftParticles"></canvas>
  <canvas class="particle-canvas right" ref="rightParticles"></canvas>

  <div class="middleUpperContainer">
    <div class="prts-bg"></div>
  </div>

  <div class="llm-chat-container">
    <div class="chat-history" ref="chatHistory">
      <div v-for="(msg, idx) in chatHistory" :key="idx" :class="['chat-msg', msg.role]">
        <span class="role-label">{{ msg.role === 'user' ? '我' : '系统' }}:</span>
        <template v-if="msg.loading">
          <span class="loading-bubble">
            <span class="dot"></span><span class="dot"></span><span class="dot"></span>
          </span>
        </template>
        <template v-else>
          {{ msg.content }}
        </template>
      </div>
    </div>

    <div class="chat-input-row">
      <input 
        v-model="chatInput" 
        @keyup.enter="sendMsg" 
        placeholder="请输入论文主题..." 
        class="chat-input" 
      />
      <button @click="sendMsg" class="chat-send-btn">生成论文</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      chatInput: '',
      chatHistory: [],
      isSending: false
    }
  },
  mounted() {
    this.initParticles(this.$refs.leftParticles);
    this.initParticles(this.$refs.rightParticles);
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleResize() {
      [this.$refs.leftParticles, this.$refs.rightParticles].forEach(canvas => {
        if (canvas) canvas.height = window.innerHeight;
      });
    },
    initParticles(canvas) {
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const width = canvas.width = 100;
      const height = canvas.height = window.innerHeight;
      const particles = [];
      const count = 50;
      for (let i = 0; i < count; i++) {
        particles.push({
          x: Math.random() * width,
          y: height + Math.random() * 200,
          radius: Math.random() * 2 + 1,
          speed: Math.random() * 0.5 + 0.5,
          alpha: Math.random() * 0.5 + 0.2
        });
      }
      const animate = () => {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => {
          p.y -= p.speed;
          if (p.y < -10) p.y = height + Math.random() * 100;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(0,0,0,${p.alpha})`;
          ctx.fill();
        });
        requestAnimationFrame(animate);
      };
      animate();
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.chatHistory;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },
    sendMsg() {
      const topic = this.chatInput.trim();
      if (!topic || this.isSending) return;

      this.isSending = true;
      this.chatHistory.push({ role: 'user', content: topic });
      this.chatInput = '';

      const assistantMsg = { role: 'assistant', content: '', loading: true };
      this.chatHistory.push(assistantMsg);
      this.scrollToBottom();
      const idx = this.chatHistory.indexOf(assistantMsg);

      // 模拟论文生成（前端直出，不连后端）
      setTimeout(() => {
        this.chatHistory[idx].content = `# ${topic}

## 摘要
本文基于Vue3实现毕业论文自动化生成系统，采用OpenClaw引擎完成结构化内容输出，有效降低论文撰写门槛，提升创作效率。

## 一、引言
当前高校学生在毕业论文撰写过程中普遍面临灵感不足、格式繁琐、效率低下等问题。本项目以轻量化AI辅助为核心，提供一站式论文生成方案。

## 二、系统设计
1. 前端采用Vue3组件化开发，实现LLM风格交互界面。
2. 核心逻辑采用模块化设计，支持主题输入、内容生成、结果展示。
3. 严格遵循合规要求，生成内容仅作为灵感参考。

## 三、功能实现
- 论文主题输入
- 实时流式展示
- 论文结构自动排版
- 支持导出与二次编辑


## 四、总结
本系统完成MVP核心功能，界面美观、交互流畅、体验接近主流大模型产品，可直接用于课程设计与作业展示。
`;
        this.chatHistory[idx].loading = false;
        this.isSending = false;
        this.scrollToBottom();
      }, 1500);
    }
  }
}
</script>

<style scoped>
:global(html),
:global(body),
:global(#app) {
  height: 100%;
  overflow: hidden;
}

.loading-bubble {
display: inline-flex;
align-items: center;
min-width: 32px;
height: 18px;
margin-left: 6px;
margin-bottom: 2px;
vertical-align: middle;
}
.loading-bubble .dot {
  display: inline-block;
  width: 7px;
  height: 7px;
  margin: 0 2px;
  background: #bfc2c7;
  border-radius: 50%;
  animation: dot-bounce 1.2s infinite both;
}
.loading-bubble .dot:nth-child(2) { animation-delay: 0.2s; }
.loading-bubble .dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes dot-bounce {
  0%, 80%, 100% { transform: scale(1); }
  40% { transform: scale(1.5); }
}

.middleUpperContainer{
  display: flex;
  justify-content: center;
  align-items: flex-start;
  height: 90vh;
  padding-top: 20px;
}
.prts-bg{
  width: 300px;
  height: 300px;
  background-image: url('@/assets/prts.png');
  background-size: contain;
  background-repeat: no-repeat;
  max-width: 80%;
  z-index: 1;
}

.fullscreen-bg{
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-image: url('@/assets/bg.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -1;
}

.llm-chat-container {
  position: absolute;
  left: 50%;
  top: 26%;
  transform: translateX(-50%);
  width: min(1040px, 88vw);
  background: rgba(255,255,255,0.85);
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  padding: 18px 26px 14px 26px;
  z-index: 20;
}
.chat-history {
  max-height: 340px;
  overflow-y: auto;
  margin-bottom: 14px;
  font-size: 15px;
  background: #fff;
  border: 1.5px solid #bfc2c7;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  padding: 12px 10px;
}
.chat-msg {
  margin-bottom: 8px;
  line-height: 1.6;
}
.chat-msg.user {
  text-align: right;
  color: #333;
}
.chat-msg.assistant {
  text-align: left;
  color: #434547;
}
.role-label {
  font-weight: bold;
  margin-right: 4px;
}
.chat-input-row {
  display: flex;
  gap: 12px;
}
.chat-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}
.chat-send-btn {
  padding: 8px 18px;
  background: #434547;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}
.chat-send-btn:hover {
  background-color: #a1abb0;
}

.particle-canvas {
position: fixed;
width: 100px;
height: 100vh;
pointer-events: none;
z-index: 5;
}
.particle-canvas.left {
left: 0;
}
.particle-canvas.right {
right: 0;
}
</style>