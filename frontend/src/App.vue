<template>
  <div class="min-h-screen bg-slate-950">
    <Navbar v-if="auth.isLoggedIn" />
    <router-view />
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth';
import Navbar from './components/Navbar.vue';
const auth = useAuthStore();
</script>
