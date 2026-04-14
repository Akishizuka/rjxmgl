<template>
  <div class="login">
    <h2>📝 毕业论文滚滚滚</h2>
    <input v-model="account" placeholder="输入账号" />
    <input v-model="pwd" type="password" placeholder="输入密码" />
    <button @click="login">登录</button>
    <p @click="$emit('to-register')">没有账号？去注册</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const emit = defineEmits(['login-success', 'to-register'])

const account = ref('')
const pwd = ref('')

const login = () => {
  if (!account.value || !pwd.value) {
    alert('请输入账号密码')
    return
  }
  emit('login-success')
}
</script>

<style scoped>
.login {
  background: #f5f7fa;
  padding: 30px;
  border-radius: 12px;
  text-align: center;
}
input {
  width: 100%;
  padding: 10px;
  margin: 8px 0;
  border: 1px solid #ddd;
  border-radius: 6px;
}
button {
  background: #42b983;
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