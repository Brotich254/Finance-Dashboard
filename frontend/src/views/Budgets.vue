<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Budgets</h1>
      <div class="flex items-center gap-3">
        <select v-model.number="month" @change="fetchBudgets"
          class="bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm focus:outline-none">
          <option v-for="(m, i) in MONTHS" :key="i" :value="i + 1">{{ m }}</option>
        </select>
        <select v-model.number="year" @change="fetchBudgets"
          class="bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm focus:outline-none">
          <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
        </select>
        <button @click="showForm = !showForm"
          class="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-xl text-sm font-semibold transition">
          + Budget
        </button>
      </div>
    </div>

    <!-- Add form -->
    <form v-if="showForm" @submit.prevent="handleAdd"
      class="bg-slate-900 border border-slate-800 rounded-2xl p-5 mb-6 flex gap-3">
      <input v-model="form.category" required placeholder="Category"
        class="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
      <input v-model.number="form.amount" type="number" step="0.01" min="1" required placeholder="Monthly limit ($)"
        class="w-40 bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
      <button type="submit"
        class="bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded-xl font-semibold transition">
        Save
      </button>
    </form>

    <!-- Budget cards -->
    <div class="space-y-4">
      <div v-for="b in budgets" :key="b.id"
        class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
        <div class="flex items-center justify-between mb-3">
          <div>
            <p class="font-semibold capitalize">{{ b.category }}</p>
            <p class="text-xs text-slate-500 mt-0.5">
              ${{ b.spent.toFixed(2) }} spent of ${{ b.amount.toFixed(2) }}
            </p>
          </div>
          <div class="text-right">
            <p :class="b.remaining > 0 ? 'text-emerald-400' : 'text-red-400'" class="font-bold">
              ${{ b.remaining.toFixed(2) }} left
            </p>
            <button @click="handleDelete(b.id)" class="text-xs text-slate-600 hover:text-red-400 transition mt-1">Remove</button>
          </div>
        </div>
        <div class="h-2.5 bg-slate-800 rounded-full overflow-hidden">
          <div class="h-full rounded-full transition-all"
            :class="b.percentage >= 100 ? 'bg-red-500' : b.percentage >= 80 ? 'bg-yellow-500' : 'bg-emerald-500'"
            :style="{ width: Math.min(b.percentage, 100) + '%' }" />
        </div>
        <p class="text-xs text-slate-600 mt-1.5">{{ b.percentage }}% used</p>
      </div>
      <p v-if="budgets.length === 0" class="text-center text-slate-600 py-10">
        No budgets set for this month.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
const now = new Date();
const month = ref(now.getMonth() + 1);
const year = ref(now.getFullYear());
const years = [now.getFullYear() - 1, now.getFullYear(), now.getFullYear() + 1];

const budgets = ref([]);
const showForm = ref(false);
const form = ref({ category: '', amount: '' });

const fetchBudgets = async () => {
  const { data } = await api.get('/budgets', { params: { month: month.value, year: year.value } });
  budgets.value = data;
};

const handleAdd = async () => {
  await api.post('/budgets', { ...form.value, month: month.value, year: year.value });
  form.value = { category: '', amount: '' };
  showForm.value = false;
  await fetchBudgets();
};

const handleDelete = async (id) => {
  await api.delete(`/budgets/${id}`);
  budgets.value = budgets.value.filter(b => b.id !== id);
};

onMounted(fetchBudgets);
</script>
