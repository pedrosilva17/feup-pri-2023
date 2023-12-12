<script setup>
import { defineProps } from "vue";
import { Doughnut } from "vue-chartjs";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Button } from "@/components/ui/button";

const emit = defineEmits(["moreInfo"]);

const { values } = defineProps({
    values: Object,
    place: String,
});

const cleanedValues = Object.fromEntries(
    Object.entries(values).filter(([key, value]) => key !== "median"),
);

let generateColors = () => {
    let colors = [];

    for (let i = 0; i < Object.keys(cleanedValues).length; i++) {
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
    labels: Object.keys(cleanedValues),
    datasets: [
        {
            backgroundColor: colors,
            data: Object.values(cleanedValues),
        },
    ],
};
</script>

<template>
    <div class="flex h-full w-full flex-col items-center text-white">
        {{ place }}
        <div class="h-full w-full text-white">
            <Doughnut :data="data" :options="options" />
        </div>
        <Button type="button" class="mt-2" @click="emit('moreInfo', place)">
            + More info
        </Button>
    </div>
</template>
