<template>
  <canvas class="fullscreen-bg" ref="bgCanvas"></canvas>
  <canvas class="particle-canvas left" ref="leftParticles"></canvas>
  <canvas class="particle-canvas right" ref="rightParticles"></canvas>

  <div class="middleUpperContainer">
    <div class="prts-bg"></div>
  </div>

  <div class="llm-chat-container">
    <div class="chat-history" ref="chatHistory">
      <div v-if="chatHistory.length === 0" class="empty-tip">
        请输入论文主题，点击生成论文开始对话
      </div>
      <div v-for="(msg, idx) in chatHistory" :key="idx" :class="['chat-msg', msg.role]">
        <span class="role-label">{{ msg.role === 'user' ? '我' : 'OpenClaw' }}:</span>
        <template v-if="msg.loading">
          <span class="loading-bubble">
            <span class="dot"></span><span class="dot"></span><span class="dot"></span>
          </span>
        </template>
        <template v-else>
          <pre style="white-space: pre-wrap; font-family: inherit; margin: 0;">{{ msg.content }}</pre>
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
import api from '../api.js'

export default {
  props: ['quota'],
  emits: ['update-quota'],
  data() {
    return {
      chatInput: '',
      chatHistory: [],
      isSending: false,
      bgAnimation: null
    }
  },
  mounted() {
    this.initCustomBackground()
    this.initParticles(this.$refs.leftParticles);
    this.initParticles(this.$refs.rightParticles);
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    cancelAnimationFrame(this.bgAnimation)
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
      initCustomBackground() {
      const canvas = this.$refs.bgCanvas
      if (!canvas) return
      const ctx = canvas.getContext('2d')

      const resize = () => {
        canvas.width = window.innerWidth
        canvas.height = window.innerHeight
      }
      resize()
      window.addEventListener('resize', resize)

      const particles = []
      for (let i = 0; i < 4000; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 0.05, 
          vy: (Math.random() - 0.5) * 0.05, 
          size: Math.random() * 1.3 + 0.2,
          alpha: Math.random() * 0.06 + 0.01
        })
      }

      const draw = () => {
        const gradient = ctx.createRadialGradient(
          canvas.width / 2, canvas.height / 3, 0,
          canvas.width / 2, canvas.height / 2, canvas.width
        )
        gradient.addColorStop(0, '#2b2f36')
        gradient.addColorStop(1, '#1a1c20')
        ctx.fillStyle = gradient
        ctx.fillRect(0, 0, canvas.width, canvas.height)

        particles.forEach(p => {
          p.x += p.vx
          p.y += p.vy
          if (p.x < 0 || p.x > canvas.width) p.vx *= -1
          if (p.y < 0 || p.y > canvas.height) p.vy *= -1

          ctx.beginPath()
          ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2)
          ctx.fillStyle = `rgba(255,255,255,${p.alpha})`
          ctx.fill()
        })

        this.bgAnimation = requestAnimationFrame(draw)
      }
      draw()
    },
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
          ctx.fillStyle = `rgba(255,255,255,${p.alpha})`;
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
    async sendMsg() {
      const topic = this.chatInput.trim();
      if (!topic || this.isSending) return;
      if (this.quota <= 0) {
        alert('生成次数已用完，请联系管理员')
        return
      }

      this.isSending = true;
      this.chatHistory.push({ role: 'user', content: topic });
      this.chatInput = '';

      const assistantMsg = { role: 'assistant', content: '', loading: true };
      this.chatHistory.push(assistantMsg);
      this.scrollToBottom();
      const idx = this.chatHistory.indexOf(assistantMsg);

      try {
        const res = await api.generate(topic)
        this.chatHistory[idx].content = res.data.content;
        this.chatHistory[idx].loading = false;
        this.$emit('update-quota', res.data.remaining_quota)
      } catch (err) {
        this.chatHistory[idx].content = '生成失败：' + (err.response?.data?.detail || err.message || '未知错误');
        this.chatHistory[idx].loading = false;
      } finally {
        this.isSending = false;
        this.scrollToBottom();
      }
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
  width: 200px;
  height: 200px;
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
  top: 30%;
  transform: translateX(-50%);
  width: min(1080px, 94vw);
  background: rgba(255,255,255,0.85);
  border-radius: 10px;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  padding: 24px 25px 20px 20px; 
  z-index: 20;
}
.chat-history {
  max-height: 500px; 
  min-height: 500px; 
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

.fullscreen-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1;
  display: block;
}
.fullscreen-bg, .particle-canvas {
  pointer-events: none; 
}
</style>
