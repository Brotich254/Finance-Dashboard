<template>
  <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
    <p class="text-slate-400 text-sm">{{ label }}</p>
    <p class="text-2xl font-bold mt-1" :class="valueClass">
      {{ prefix }}{{ formatted }}
    </p>
    <p v-if="sub" class="text-xs text-slate-500 mt-1">{{ sub }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue';
const props = defineProps({
  label: String,
  value: Number,
  prefix: { type: String, default: '$' },
  sub: String,
  color: { type: String, default: 'white' },
});
const formatted = computed(() => Math.abs(props.value ?? 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
const valueClass = computed(() => ({
  'text-emerald-400': props.color === 'green' || (props.color === 'auto' && props.value >= 0),
  'text-red-400': props.color === 'red' || (props.color === 'auto' && props.value < 0),
  'text-white': props.color === 'white',
  'text-blue-400': props.color === 'blue',
}));
</script>
