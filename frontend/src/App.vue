<script setup>
import Map from "@/components/Map.vue";
import SearchBar from "./components/SearchBar.vue";
import ResultTable from "./components/ResultTable.vue";
import Country from "./components/Country.vue";
import { ref } from "vue";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

let data = ref({});
let key = ref(0);
let ckey = ref(0);
let loading = ref(false);
let country = ref([]);

const submit = async (values) => {
    loading.value = true;
    let res;
    if (values.advanced) {
        res = await fetch("http://localhost:8000/advancedSearch/", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(values),
        });
    } else {
        res = await fetch("http://localhost:8000/search/", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(values),
        });
    }
    if(!res.ok) {
        alert("Something went wrong, please try a different query");
        window.location.reload();
    }
    data.value = await res.json();
    loading.value = false;
    key.value += 1;
};

const moreInfo = (place) => {
    let docs = [];
    data.value.docs.forEach((doc) => {
        if (Object(doc).cca3[0] === place) {
            docs.push(doc);
        }
    });
    country.value = docs;
    ckey.value += 1;
    window.href="http://localhost:5173/#" + Object(docs[0]).cca3[0]; // doesnt work because emits take time :P
    console.log(country.value, ckey.value);
};
</script>

<template>
    <main
        class="dark flex flex-col items-center gap-2 bg-background text-primary"
    >
        <template v-if="loading">
            <!-- funny because leaflet apparently uses z-index to do layers so we do more z-index xD  -->
            <div
                class="fixed left-0 top-0 z-[100000] flex h-screen w-screen items-center justify-center bg-background"
            >
                <div
                    class="h-32 w-32 animate-spin rounded-full border-b-2 border-t-2 border-primary"
                ></div>
            </div>
        </template>
        <SearchBar @submit="submit" />
        <Map :data="data" :key="key" @moreInfo="moreInfo" />
        <Country
            :docs="country"
            :key="ckey"
        />
        <h1 class="text-xl font-bold pt-5">All results</h1>
        <ResultTable
            v-show="country.value == undefined && data !== undefined"
            :data="data"
        />
    </main>
</template>
