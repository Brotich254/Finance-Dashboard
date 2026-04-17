<template>
  <nav class="bg-slate-900 border-b border-slate-800 px-4 py-3">
    <div class="max-w-6xl mx-auto flex items-center justify-between">
      <router-link to="/" class="text-xl font-bold text-emerald-400">💰 FinFlow</router-link>
      <div class="flex items-center gap-5 text-sm">
        <router-link to="/" class="text-slate-400 hover:text-white transition" active-class="text-white">Dashboard</router-link>
        <router-link to="/transactions" class="text-slate-400 hover:text-white transition" active-class="text-white">Transactions</router-link>
        <router-link to="/budgets" class="text-slate-400 hover:text-white transition" active-class="text-white">Budgets</router-link>
        <div class="flex items-center gap-3 ml-2">
          <span class="text-slate-500 text-xs">{{ auth.user?.name }}</span>
          <button @click="handleLogout" class="text-slate-500 hover:text-red-400 transition text-xs">Logout</button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
const auth = useAuthStore();
const router = useRouter();
const handleLogout = () => { auth.logout(); router.push('/login'); };
</script>
