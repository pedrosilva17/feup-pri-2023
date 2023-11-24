<script setup>
import { LMap, LTileLayer, LGeoJson } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
import { Suspense, defineAsyncComponent } from "vue";

const GeoJSON = defineAsyncComponent(() => import("./components/GeoJSON.vue"));

const zoom = 1;
const center = [0, 0];
const url = 'https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png';
const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
const bounds = [
        [90, 0],
        [-90, 180]
];

const codes = [
"AZE",
"BRN",
"ARG",
"CHL",
"GRC",
"GNB",
"LBR",
"THA",
"BGD",
"ASM",
"DJI",
"TUV",
"BWA",
"LSO",
"BMU",
"VIR",
"TLS",
"KWT",
"LBN",
"HND",
"MEX",
"GUY",
"HTI",
"MNE",
"POL",
"SGS",
"GBR",
"CUB",
"VUT",
"SWE",
"ARE",
"YEM",
"SLV",
"PHL",
"FIN",
"FRA",
"DOM",
"BDI",
"HUN",
"ISL",
"TZA",
"ARM",
"IRQ",
"GNQ",
"GAB",
"SMR",
"URY",
"LKA",
"NAM",
"VNM",
"JPN",
"GHA",
"BTN",
"CHE",
"ZMB",
"AFG",
"GRD",
"UKR",
"GTM",
"MDV",
"BGR",
"HRV",
"PNG",
"ERI",
"JAM",
"UGA",
"COL",
"SOM",
"NIC",
"TKL",
"BHR",
"CYP",
"DNK",
"MDA",
"PRI",
"MAC",
"DOM",
"CIV",
"EGY",
"JOR",
"LBY",
"KAZ",
"RUS",
"PLW",
"MKD",
"MMR",
"COK",
"ROU",
"GBR",
"COM",
"CRI",
"LCA",
"CZE",
"DEU",
"IOT",
"ETH",
"GMB",
"PRK",
"PRK",
"KNA",
"MRT",
"ZAF",
"CAN",
"MAR",
"GRL",
"SGP",
"FJI",
"PAN",
"ISR",
"NPL",
"KGZ",
"SRB",
"PSE",
"KEN",
"SWZ",
"VCT",
"NGA",
"USA",
"GUM",
"ITA",
"PAK",
"SUR",
"SVK",
"MNG",
"MDG",
"KIR",
"LUX",
"ZWE",
"AUS",
"SVN",
"BRA",
"ROU",
"MHL",
"AGO",
"KHM",
"TJK",
"TTO",
"NGA",
"MCO",
"NZL",
"QAT",
"ATG",
"MWI",
"IDN",
"MLT",
"PRY",
"STP",
"TKM",
"NRU",
"MUS",
"BLR",
"CAF",
"SAU",
"SLB",
"ASM",
"LAO",
"ECU",
"SEN",
"BEN",
"ALB",
"PNG",
"BHS",
"AND",
"NOR",
"PRT",
"CPV",
"COG",
"AUT",
"TUN",
"MOZ",
"SYC",
"BRB",
"DZA",
"TGO",
"PER",
"BIH",
"EST",
"NIU",
"SYR",
"COD",
"BFA",
"CMR",
"SLE",
"BEL",
"MYS",
"SOM",
"UZB",
"TUR",
"TCD",
"LVA",
"TON",
"ESP",
"BLZ",
"MNP",
"RWA",
"LTU"
]

const onEachFeature = (feature, layer) => {
  console.log("hi");
};
</script>

<template>
  <LMap
      :zoom="zoom"
      class="z-10 cursor-auto border border-solid border-black"
      :zoom-animation="true"
      :center="center"
      :use-global-leaflet="false"
      :scroll-wheel-zoom="false"
      :bounds="bounds"
      :noWrap="true"
      :on-each-feature="onEachFeature"
      style="height: 400px; width: 800px"
  >
    <LTileLayer
        :url="url"
        :attribution="attribution"
        layer-type="base"
    />
    <template v-for="ccode in codes">
      <Suspense>
        <GeoJSON :ccode="ccode" />
      </Suspense>
    </template>
  </LMap>
  {{ codes.length }}
</template>
