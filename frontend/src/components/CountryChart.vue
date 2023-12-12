<script setup>
import { Doughnut } from "vue-chartjs";

const { values } = defineProps({
    values: Object,
});

let generateColors = () => {
    let colors = [];

    for (let i = 0; i < Object.keys(values).length; i++) {
        colors.push("#" + Math.floor(Math.random() * 16777215).toString(16));
    }

    return colors;
};

const colors = generateColors();

const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                fontColor: "#FFFFFF",
            },
        },
    },
};
const data = {
    labels: Object.keys(values),
    datasets: [
        {
            backgroundColor: colors,
            data: Object.values(values),
        },
    ],
};
</script>

<template>
    <!-- {{ values }}
    {{ data }} -->
    <Doughnut :data="data" :options="options" />
</template>