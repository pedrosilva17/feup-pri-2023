<script setup>
import { defineProps } from "vue";
import ResultTable from "./ResultTable.vue";
import CountryChart from "./CountryChart.vue";

const { docs } = defineProps({
    docs: Array,
});

const diseaseValues = () => {
    let values = {};
    docs.forEach((doc) => {
        doc = Object(doc);
        if (values[doc.cause_name] !== undefined)  {
            values[doc.cause_name][doc.year] = 0;
            values[doc.cause_name][doc.year] += doc.val;
        } else {
            values[doc.cause_name] = {};
            values[doc.cause_name][doc.year] = doc.val;
        }
    });
    return values;
};

</script>

<template>
    <template v-if="docs.length !== 0">
        <section class="pt-5 flex flex-col items-center w-full">
            <h1 :id="docs[0].cca3[0]" class="font-bold text-2xl">{{ docs[0].location_name }} - {{ docs[0].cca3[0] }}</h1>

            <div class="flex flex-row flex-wrap justify-center pt-5 gap-4">
                <template v-for="[disease, values] in Object.entries(diseaseValues())">
                    <div class="items-center">
                        <h2 class="text-center">{{disease}}</h2>
                        <div class="w-full h-60">
                            <CountryChart :values="values" />
                        </div>
                    </div>
                </template>
            </div>
            
            <ResultTable :data="{docs:docs}"></ResultTable>
        </section>
    </template>
</template>
