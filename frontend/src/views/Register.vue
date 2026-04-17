<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-8 w-full max-w-sm">
      <h1 class="text-2xl font-bold mb-2 text-center">Create account</h1>
      <p class="text-slate-500 text-sm text-center mb-6">Start tracking your finances</p>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <input v-model="form.name" required placeholder="Full name"
          class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
        <input v-model="form.email" type="email" required placeholder="Email"
          class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
        <input v-model="form.password" type="password" required placeholder="Password"
          class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
        <p v-if="error" class="text-red-400 text-xs">{{ error }}</p>
        <button type="submit" :disabled="loading"
          class="w-full bg-emerald-600 hover:bg-emerald-700 text-white py-2.5 rounded-xl font-semibold disabled:opacity-50 transition">
          {{ loading ? 'Creating...' : 'Sign up' }}
        </button>
      </form>
      <p class="text-center text-sm text-slate-500 mt-4">
        Have an account?
        <router-link to="/login" class="text-emerald-400 hover:underline">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const auth = useAuthStore();
const router = useRouter();
const form = ref({ name: '', email: '', password: '' });
const loading = ref(false);
const error = ref('');

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';
  try {
    await auth.register(form.value.name, form.value.email, form.value.password);
    router.push('/');
  } catch {
    error.value = 'Registration failed';
  } finally {
    loading.value = false;
  }
};
</script>
