<script setup>
import { defineProps, ref } from 'vue';
import { LGeoJson, LPopup, LFeatureGroup } from "@vue-leaflet/vue-leaflet";

const content = ref(null);
const gjson = ref(null);

const { ccode } = defineProps({
    ccode: String
})

async function printJSON() {
    const response = await fetch(`src/assets/gjsons/${ccode}.json`);
    return response.json();
}
const geojson = await printJSON();
const color = Math.floor(Math.random()*16777215).toString(16);

const style = {
    weight: 2,
    color: color,
    opacity: 1,
    fillColor: color,
    fillOpacity: 0.5
};

const openPopup = () => {
    console.log("hadskjadsfkjadsfkj", content);
    content.value.mapObject.openPopup("0, 0");
};
const test = (feature, layer) => {
    console.log(feature, layer);
};
</script>

<template>
    <LGeoJson
    ref="gjson"
    :geojson="geojson"
    :options="{ style }"
    @click="openPopup()"
    :onEachFeature="test()"
    >
        <LPopup ref="content" :options="{ maxWidth: 800 }">
            {{ cc_code }}
        </LPopup>
    </LGeoJson>
</template>