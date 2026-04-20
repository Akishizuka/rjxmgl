<template>
  <div class="register-page">
    <div class="register-box">
      <h2>用户注册</h2>
      <p>创建你的账号</p>

      <input v-model="account" placeholder="设置账号" />
      <input v-model="pwd" type="password" placeholder="设置密码" />

      <button @click="register" class="btn-register">注册</button>
      <p @click="$emit('to-login')" class="link">已有账号？返回登录</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api.js'
const emit = defineEmits(['register-success', 'to-login'])

const account = ref('')
const pwd = ref('')

const register = async () => {
  if (!account.value || !pwd.value) {
    alert('请输入账号和密码')
    return
  }
  try {
    await api.register(account.value, pwd.value)
    alert('注册成功！请登录')
    emit('register-success')
  } catch (err) {
    alert(err.response?.data?.detail || '注册失败')
  }
}
</script>

<style scoped>
.register-page {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to bottom, #2d3035, #1a1c20);
  background-image:
    linear-gradient(to bottom, #2d3035, #1a1c20),
    radial-gradient(rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 100% 100%, 30px 30px;
  background-blend-mode: overlay;
  box-sizing: border-box;
  overflow: hidden;
  margin: 0;
  padding: 0;
  position: fixed;
  top: 0;
  left: 0;
}

.register-box {
  width: 380px;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 14px;
  padding: 40px 30px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.3);
  text-align: center;
  box-sizing: border-box;
}

.register-box h2 {
  margin: 0 0 6px 0;
  font-size: 22px;
  color: #fff;
}

.register-box p {
  margin: 0 0 28px 0;
  font-size: 14px;
  color: rgba(255,255,255,0.7);
}

input {
  width: 100%;
  height: 44px;
  padding: 0 14px;
  margin: 8px 0;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 8px;
  color: #fff;
  font-size: 15px;
  box-sizing: border-box;
  outline: none;
}
input::placeholder {
  color: rgba(255,255,255,0.5);
}
input:focus {
  border-color: rgba(255,255,255,0.6);
  background: rgba(255,255,255,0.15);
}

.btn-register {
  width: 100%;
  height: 46px;
  margin-top: 10px;
  background: rgba(255,255,255,0.9);
  color: #222;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 10px;
}
.btn-register:hover {
  background: #fff;
  transform: scale(1.03);
  box-shadow: 0 6px 12px rgba(255,255,255,0.2);
}

.link {
  margin-top: 10px;
  color: rgba(255,255,255,0.6);
  cursor: pointer;
  font-size: 14px;
}
.link:hover {
  color: #fff;
}
</style>