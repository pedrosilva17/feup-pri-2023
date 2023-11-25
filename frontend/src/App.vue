<script setup>
import Map from "@/components/Map.vue";
import SearchBar from "./components/SearchBar.vue";
import ResultTable from "./components/ResultTable.vue";
</script>

<template>
    <main
        class="dark flex flex-col items-center gap-2 bg-background text-primary"
    >
        <SearchBar />
        <Map />
        <ResultTable />
    </main>
</template>
