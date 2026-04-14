<template>
  <div class="register">
    <h2>用户注册</h2>
    <input v-model="account" placeholder="设置账号" />
    <input v-model="pwd" type="password" placeholder="设置密码" />
    <button @click="register">注册</button>
    <p @click="$emit('to-login')">已有账号？返回登录</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const emit = defineEmits(['to-login'])

const account = ref('')
const pwd = ref('')

const register = () => {
  alert('注册成功！请登录')
  emit('to-login')
}
</script>

<style scoped>
.register {
  background: #f5f7fa;
  padding: 30px;
  border-radius: 12px;
  text-align: center;
  margin-top: 20px;
}
input {
  width: 100%;
  padding: 10px;
  margin: 8px 0;
  border: 1px solid #ddd;
  border-radius: 6px;
}
button {
  background: #1890ff;
  color: white;
  border: none;
  padding: 10px;
  width: 100%;
  border-radius: 6px;
  margin-top: 10px;
}
p {
  margin-top: 10px;
  color: #666;
  cursor: pointer;
}
</style>