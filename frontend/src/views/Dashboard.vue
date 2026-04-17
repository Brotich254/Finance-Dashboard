<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">Dashboard</h1>

    <div v-if="stats" class="space-y-6">
      <!-- Stat cards -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total Balance" :value="stats.total_balance" color="auto" />
        <StatCard label="Monthly Income" :value="stats.monthly_income" color="green" />
        <StatCard label="Monthly Expenses" :value="stats.monthly_expenses" color="red" />
        <StatCard label="Monthly Savings" :value="stats.monthly_savings" color="auto" />
      </div>

      <div class="grid lg:grid-cols-2 gap-6">
        <!-- Monthly trend chart -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <h2 class="font-semibold mb-4 text-slate-300">6-Month Trend</h2>
          <Bar :data="trendChartData" :options="chartOptions" />
        </div>

        <!-- Category breakdown -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <h2 class="font-semibold mb-4 text-slate-300">Spending by Category</h2>
          <div v-if="stats.top_categories.length === 0" class="text-slate-500 text-sm text-center py-10">
            No expenses this month.
          </div>
          <div v-else class="space-y-3">
            <div v-for="cat in stats.top_categories" :key="cat.category">
              <div class="flex justify-between text-sm mb-1">
                <span class="text-slate-300 capitalize">{{ cat.category }}</span>
                <span class="text-slate-400">${{ cat.amount.toFixed(2) }} ({{ cat.percentage }}%)</span>
              </div>
              <div class="h-2 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-emerald-500 rounded-full transition-all"
                  :style="{ width: cat.percentage + '%' }" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-slate-500 text-center py-20">Loading...</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js';
import api from '../api';
import StatCard from '../components/StatCard.vue';

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const stats = ref(null);
const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

onMounted(async () => {
  const { data } = await api.get('/analytics/dashboard');
  stats.value = data;
});

const trendChartData = computed(() => {
  if (!stats.value) return { labels: [], datasets: [] };
  const trend = stats.value.monthly_trend;
  return {
    labels: trend.map(t => MONTHS[t.month - 1]),
    datasets: [
      { label: 'Income', data: trend.map(t => t.income), backgroundColor: '#10b981', borderRadius: 4 },
      { label: 'Expenses', data: trend.map(t => t.expenses), backgroundColor: '#ef4444', borderRadius: 4 },
    ],
  };
});

const chartOptions = {
  responsive: true,
  plugins: { legend: { labels: { color: '#94a3b8' } } },
  scales: {
    x: { ticks: { color: '#64748b' }, grid: { color: '#1e293b' } },
    y: { ticks: { color: '#64748b' }, grid: { color: '#1e293b' } },
  },
};
</script>
