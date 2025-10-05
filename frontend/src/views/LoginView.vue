<template>
  <div class="login">
    <h2>Login</h2>
    <button @click="loginWithGoogle">Login with Google</button>
  </div>
</template>

<script setup>
const loginWithGoogle = () => {
  window.location.href = "http://localhost:8000/accounts/google/login/"
}
</script>