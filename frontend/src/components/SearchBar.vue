<script setup>
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { toTypedSchema } from "@vee-validate/zod";
import { useForm } from "vee-validate";
import * as z from "zod";
import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
} from "@/components/ui/form";
import { Checkbox } from "./ui/checkbox";

const formSchema = toTypedSchema(
    z
        .object({
            search: z.string().optional(),
            sex: z.string().optional(),
            country: z.string().optional(),
            age: z.string().optional(),
            min_year: z.coerce.number().optional(),
            max_year: z.coerce.number().optional(),
            min_value: z.coerce.number().optional(),
            max_value: z.coerce.number().optional(),
            search_for: z.array(z.string()).optional(),
        })
        .refine(
            (data) => {
                if (data.min_year && data.max_year) {
                    return data.min_year <= data.max_year;
                }
                return true;
            },
            {
                message: "Min. year must be less than max. year",
                path: ["min_year", "max_year"],
            },
        )
        .refine(
            (data) => {
                if (data.min_value && data.max_value) {
                    return data.min_value <= data.max_value;
                }
                return true;
            },
            {
                message: "Min. value must be less than max. value",
                path: ["min_value", "max_value"],
            },
        ),
);

const searchFields = [
    {
        id: "disease",
        label: "Disease Name",
    },
    {
        id: "description",
        label: "Disease Description",
    },
    {
        id: "value",
        label: "Value",
    },
    {
        id: "country",
        label: "Country",
    },
];

const { handleSubmit, meta } = useForm({
    validationSchema: formSchema,
    initialValues: {
        search_for: [],
    },
});

const onSubmit = handleSubmit( async (values) => {
    const res = await fetch("http://localhost:8000/search/", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(values),
    });
    const data = await res.json();
    console.log(data);
});
const countries = [
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
"GEO",
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
"MLI",
"NIC",
"TKL",
"BHR",
"CYP",
"DNK",
"MDA",
"PRI",
"MAC",
"DMA",
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
"COM",
"CRI",
"LCA",
"CZE",
"DEU",
"IOT",
"ETH",
"GMB",
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
"NER",
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
"LAO",
"ECU",
"SEN",
"BEN",
"ALB",
"BHS",
"AND",
"NOR",
"PRT",
"CPV",
"COD",
"NLD",
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
"LTU"];

</script>

<template>
    <form @submit="onSubmit" class="flex flex-col items-center">
        <div class="flex w-fit flex-row gap-4 p-7">
            <FormField v-slot="{ componentField }" name="search">
                <Input
                    v-bind="componentField"
                    placeholder="Search..."
                    class="w-96"
                />
            </FormField>
            <Button :disabled="!meta.valid" type="submit">Search</Button>
        </div>
        <div class="flex flex-col items-center gap-2 space-y-2 p-2">
            <div class="grid grid-cols-4 gap-7">
                <FormField v-slot="{ componentField }" name="sex">
                    <Select v-bind="componentField">
                        <SelectTrigger class="w-[180px]">
                            <SelectValue placeholder="Sex" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectItem value="both"> Both </SelectItem>
                                <SelectItem value="female"> Female </SelectItem>
                                <SelectItem value="male"> Male </SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                </FormField>
                <FormField v-slot="{ componentField }" name="country" v>
                    <Select v-bind="componentField">
                        <SelectTrigger class="w-[180px]">
                            <SelectValue placeholder="Country" />
                        </SelectTrigger>
                        <SelectContent class="max-h-96">
                            <SelectGroup>
                                <SelectItem
                                    v-for="country in countries"
                                    :key="country"
                                    :value="country"
                                >
                                    {{ country }}
                                </SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                </FormField>
                <FormField v-slot="{ componentField }" name="age">
                    <Select v-bind="componentField">
                        <SelectTrigger class="w-[180px]">
                            <SelectValue placeholder="Age" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectItem value="0-19"> 0 - 19 </SelectItem>
                                <SelectItem value="20-54"> 20 - 54 </SelectItem>
                                <SelectItem value="55-99">
                                    55 - 99+
                                </SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                </FormField>
                <div class="flex flex-row items-center justify-center gap-2">
                    <FormField v-slot="{ componentField }" name="min_year">
                        <Select v-bind="componentField">
                            <SelectTrigger class="min-w-[50px]">
                                <SelectValue placeholder="Year" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectGroup>
                                    <!-- TODO: GET YEARS FROM BACKEND -->
                                    <SelectItem value="1">2020</SelectItem>
                                    <SelectItem value="2">2021</SelectItem>
                                    <SelectItem value="11">2022</SelectItem>
                                    <SelectItem value="12">2023</SelectItem>
                                    <SelectItem value="13">2024</SelectItem>
                                </SelectGroup>
                            </SelectContent>
                        </Select>
                    </FormField>
                    to
                    <FormField v-slot="{ componentField }" name="max_year">
                        <Select v-bind="componentField">
                            <SelectTrigger class="min-w-[50px]">
                                <SelectValue placeholder="Year" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectGroup>
                                    <!-- TODO: GET YEARS FROM BACKEND -->
                                    <SelectItem value="1">2020</SelectItem>
                                    <SelectItem value="2">2021</SelectItem>
                                    <SelectItem value="11">2022</SelectItem>
                                    <SelectItem value="12">2023</SelectItem>
                                    <SelectItem value="13">2024</SelectItem>
                                </SelectGroup>
                            </SelectContent>
                        </Select>
                    </FormField>
                </div>
            </div>
            <div class="flex flex-row items-center gap-4">
                <div class="flex flex-row items-center gap-3">
                    <Label>Value</Label>
                    <FormField v-slot="{ componentField }" name="min_value">
                        <Input
                            v-bind="componentField"
                            placeholder="Min. Value"
                            class="w-[100px]"
                        />
                    </FormField>
                    -
                    <FormField v-slot="{ componentField }" name="max_value">
                        <Input
                            v-bind="componentField"
                            placeholder="Max. Value"
                            class="w-[100px]"
                        />
                    </FormField>
                </div>
                <div class="flex flex-col items-center gap-2">
                    <Label>Search for:</Label>
                    <div class="flex gap-3">
                        <FormField
                            v-for="item in searchFields"
                            v-slot="{ value, handleChange }"
                            :key="item.id"
                            name="search_for"
                        >
                            <FormItem
                                :key="item.id"
                                class="flex flex-row items-center space-x-3 space-y-0"
                            >
                                <FormControl>
                                    <Checkbox
                                        :checked="value.includes(item.id)"
                                        @update:checked="
                                            (checked) => {
                                                if (Array.isArray(value)) {
                                                    handleChange(checked? [...value,item.id,]: value.filter((id) => id !== item.id,),);
                                                }
                                            }
                                        "
                                    />
                                </FormControl>
                                <FormLabel class="font-normal">
                                    {{ item.label }}
                                </FormLabel>
                            </FormItem>
                        </FormField>
                    </div>
                </div>
            </div>
        </div>
    </form>
</template>
