<script setup>
import { defineProps } from "vue";
import { LGeoJson } from "@vue-leaflet/vue-leaflet";

const { ccode } = defineProps({
    ccode: String,
});

async function loadGeoJSON() {
    const response = await fetch(`src/assets/gjsons/${ccode}.json`);
    return await response.json();
}

const geojson = await loadGeoJSON();

const onEachFeatureFunction = () => {
    return (feature, layer) => {
        layer.bindPopup("<p>" + ccode + "</p>");
    };
};

const style = () => {
    // TODO: make this change with the value of the data or be based down from the parent
    const scale = ["#44ce1b", "#bbdb44", "#f7e379", "#f2a134", "#e51f1f"];
    const color = scale[Math.floor(Math.random(0) * 5)];
    return {
        weight: 2,
        color: color,
        opacity: 1,
        fillColor: color,
        fillOpacity: 0.5,
    };
};

const options = {
    onEachFeature: onEachFeatureFunction(),
};
</script>

<template>
    <LGeoJson :geojson="geojson" :options="options" :optionsStyle="style" />
</template>
