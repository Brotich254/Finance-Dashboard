<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Transactions</h1>
      <button @click="showForm = !showForm"
        class="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-xl text-sm font-semibold transition">
        + Add
      </button>
    </div>

    <!-- Add form -->
    <form v-if="showForm" @submit.prevent="handleAdd"
      class="bg-slate-900 border border-slate-800 rounded-2xl p-5 mb-6 grid grid-cols-2 gap-3">
      <input v-model="form.title" required placeholder="Title"
        class="col-span-2 bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
      <input v-model.number="form.amount" type="number" step="0.01" min="0.01" required placeholder="Amount"
        class="bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
      <select v-model="form.type"
        class="bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
        <option value="expense">Expense</option>
        <option value="income">Income</option>
      </select>
      <input v-model="form.category" required placeholder="Category (e.g. Food, Rent)"
        class="bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
      <input v-model="form.date" type="date" required
        class="bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
      <input v-model="form.note" placeholder="Note (optional)"
        class="col-span-2 bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" />
      <button type="submit" :disabled="loading"
        class="col-span-2 bg-emerald-600 hover:bg-emerald-700 text-white py-2.5 rounded-xl font-semibold disabled:opacity-50 transition">
        {{ loading ? 'Saving...' : 'Save Transaction' }}
      </button>
    </form>

    <!-- Filters -->
    <div class="flex gap-3 mb-4 flex-wrap">
      <select v-model="filter.type" @change="fetchTransactions"
        class="bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm focus:outline-none">
        <option value="">All Types</option>
        <option value="income">Income</option>
        <option value="expense">Expense</option>
      </select>
      <input v-model="filter.category" @input="fetchTransactions" placeholder="Filter category"
        class="bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm focus:outline-none w-40" />
      <select v-model.number="filter.month" @change="fetchTransactions"
        class="bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm focus:outline-none">
        <option :value="0">All Months</option>
        <option v-for="(m, i) in MONTHS" :key="i" :value="i + 1">{{ m }}</option>
      </select>
    </div>

    <!-- List -->
    <div class="space-y-2">
      <div v-for="tx in transactions" :key="tx.id"
        class="bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 flex items-center justify-between">
        <div>
          <p class="font-medium">{{ tx.title }}</p>
          <p class="text-xs text-slate-500 mt-0.5">{{ tx.category }} · {{ tx.date }}</p>
          <p v-if="tx.note" class="text-xs text-slate-600 mt-0.5">{{ tx.note }}</p>
        </div>
        <div class="flex items-center gap-4">
          <span :class="tx.type === 'income' ? 'text-emerald-400' : 'text-red-400'" class="font-bold">
            {{ tx.type === 'income' ? '+' : '-' }}${{ tx.amount.toFixed(2) }}
          </span>
          <button @click="handleDelete(tx.id)" class="text-slate-600 hover:text-red-400 transition text-xs">✕</button>
        </div>
      </div>
      <p v-if="transactions.length === 0" class="text-center text-slate-600 py-10">No transactions found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const today = new Date().toISOString().split('T')[0];

const transactions = ref([]);
const showForm = ref(false);
const loading = ref(false);
const form = ref({ title: '', amount: '', type: 'expense', category: '', date: today, note: '' });
const filter = ref({ type: '', category: '', month: new Date().getMonth() + 1 });

const fetchTransactions = async () => {
  const params = {};
  if (filter.value.type) params.type = filter.value.type;
  if (filter.value.category) params.category = filter.value.category;
  if (filter.value.month) params.month = filter.value.month;
  const { data } = await api.get('/transactions', { params });
  transactions.value = data;
};

const handleAdd = async () => {
  loading.value = true;
  try {
    const { data } = await api.post('/transactions', form.value);
    transactions.value.unshift(data);
    form.value = { title: '', amount: '', type: 'expense', category: '', date: today, note: '' };
    showForm.value = false;
  } finally {
    loading.value = false;
  }
};

const handleDelete = async (id) => {
  await api.delete(`/transactions/${id}`);
  transactions.value = transactions.value.filter(t => t.id !== id);
};

onMounted(fetchTransactions);
</script>
