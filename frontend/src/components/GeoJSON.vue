<script setup>
import { defineProps, h, ref } from "vue";
import { LGeoJson } from "@vue-leaflet/vue-leaflet";
import Popup from "./Popup.vue";

const emit = defineEmits(["moreInfo"]);

const popup = ref("");

const { ccode, values, color } = defineProps({
    ccode: String,
    values: Object,
    color: String,
});

async function loadGeoJSON() {
    const response = await fetch(`src/assets/gjsons/${ccode}.json`);
    return await response.json();
}

const geojson = await loadGeoJSON();

const onEachFeatureFunction = () => {
    return (feature, layer) => {
        layer.bindPopup(popup.value.$el);
    };
};

const style = () => {
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
    <template v-show="false">
        <Popup
            ref="popup"
            :values="values"
            :place="ccode"
            @moreInfo="(place) => emit('moreInfo', place)"
        />
    </template>
</template>

<style>
.leaflet-popup-content-wrapper {
    background-color: hsl(var(--background));
    width: 250px;
    height: 250px;
    padding: 0;
    margin: 0;
    border-radius: 10px;
}

.leaflet-popup-content-wrapper .leaflet-popup-content {
    padding: 1em;
    margin: 0;
    width: 250px;
    height: 250px;
    border-radius: 10px;
}

.leaflet-popup-tip-container {
    display: none;
}
</style>
