<template>
  <div class="app">
    <div v-if="!isLogin">
      <Login @login-success="handleLogin" />
      <Register v-if="showReg" @to-login="showReg = false" />
    </div>

    <div v-else>
      <Header :quota="quota" @logout="handleLogout" />
      <Generate
        :quota="quota"
        @update-quota="quota = $event"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import Header from './components/Header.vue'
import Generate from './components/Generate.vue'

//测试的时候改成true
const isLogin = ref(true)
const showReg = ref(false)
const quota = ref(5)

const handleLogin = () => {
  isLogin.value = true
}

const handleLogout = () => {
  isLogin.value = false
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}
.app {
  max-width: 900px;
  margin: 30px auto;
  padding: 20px;
}
</style>