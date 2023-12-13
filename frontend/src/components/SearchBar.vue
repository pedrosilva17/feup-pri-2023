<script setup>
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
// import { Separator } from '@/components/ui/separator'
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
import { defineEmits } from "vue";

const emit = defineEmits(["submit"]);

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
            advanced: z.boolean().optional(),
            k_value: z.coerce.number().optional(),
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
        id: "cause_name",
        label: "Disease Name",
    },
    {
        id: "description",
        label: "Disease Description",
    },
    // {
    //     id: "val",
    //     label: "Value",
    // },
    {
        id: "location_name",
        label: "Country",
    },
];

const { handleSubmit, meta } = useForm({
    validationSchema: formSchema,
    initialValues: {
        search_for: [],
    },
});

const onSubmit = handleSubmit(async (values) => {
    emit("submit", values);
});

const countries = [
"AFG",
"AGO",
"ALB",
"AND",
"ARE",
"ARG",
"ARM",
"ASM",
"ATG",
"AUS",
"AUT",
"AZE",
"BDI",
"BEL",
"BEN",
"BFA",
"BGD",
"BGR",
"BHR",
"BHS",
"BIH",
"BLR",
"BLZ",
"BMU",
"BOL",
"BRA",
"BRB",
"BRN",
"BTN",
"BWA",
"CAF",
"CAN",
"CHE",
"CHL",
"CIV",
"CMR",
"COD",
"COK",
"COL",
"COM",
"CPV",
"CRI",
"CUB",
"CYP",
"CZE",
"DEU",
"DJI",
"DMA",
"DNK",
"DOM",
"DZA",
"ECU",
"EGY",
"ERI",
"ESP",
"EST",
"ETH",
"FIN",
"FJI",
"FRA",
"FSM",
"GAB",
"GBR",
"GEO",
"GHA",
"GMB",
"GNB",
"GNQ",
"GRC",
"GRD",
"GRL",
"GTM",
"GUM",
"GUY",
"HND",
"HRV",
"HTI",
"HUN",
"IDN",
"IOT",
"IRN",
"IRQ",
"ISL",
"ISR",
"ITA",
"JAM",
"JOR",
"JPN",
"KAZ",
"KEN",
"KGZ",
"KHM",
"KIR",
"KNA",
"KWT",
"LAO",
"LBN",
"LBR",
"LBY",
"LCA",
"LKA",
"LSO",
"LTU",
"LUX",
"LVA",
"MAC",
"MAR",
"MCO",
"MDA",
"MDG",
"MDV",
"MEX",
"MHL",
"MKD",
"MLI",
"MLT",
"MMR",
"MNE",
"MNG",
"MNP",
"MOZ",
"MRT",
"MUS",
"MWI",
"MYS",
"NAM",
"NER",
"NGA",
"NIC",
"NIU",
"NLD",
"NOR",
"NPL",
"NRU",
"NZL",
"PAK",
"PAN",
"PER",
"PHL",
"PLW",
"PNG",
"POL",
"PRI",
"PRK",
"PRT",
"PRY",
"PSE",
"QAT",
"ROU",
"RUS",
"RWA",
"SAU",
"SEN",
"SGP",
"SLB",
"SLE",
"SLV",
"SMR",
"SOM",
"SRB",
"SSD",
"STP",
"SUR",
"SVK",
"SVN",
"SWE",
"SWZ",
"SYC",
"SYR",
"TCD",
"TGO",
"THA",
"TJK",
"TKL",
"TKM",
"TLS",
"TON",
"TTO",
"TUN",
"TUR",
"TUV",
"TWN",
"TZA",
"UGA",
"UKR",
"URY",
"USA",
"UZB",
"VCT",
"VEN",
"VIR",
"VNM",
"VUT",
"YEM",
"ZAF",
"ZMB",
"ZWE",
"COG",
"SGS",
"CHN"
];
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
            <div class="grid grid-cols-3 gap-7">
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
                                <SelectGroup class="max-h-96">
                                    <template v-for="year in 30">
                                        <SelectItem :value="(1989 + year).toString()">{{ (1989 + year).toString() }}</SelectItem>
                                    </template>
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
                                    <template v-for="year in 30">
                                        <SelectItem :value="(1989 + year).toString()">{{ (1989 + year).toString() }}</SelectItem>
                                    </template>
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
                                                    handleChange(
                                                        checked
                                                            ? [
                                                                  ...value,
                                                                  item.id,
                                                              ]
                                                            : value.filter(
                                                                  (id) =>
                                                                      id !==
                                                                      item.id,
                                                              ),
                                                    );
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
            <!-- <Separator class="my-4" /> -->
            <div class="flex flex-row gap-4">
                <FormField
                    v-slot="{ value, handleChange }"
                    name="advanced"
                >
                    <FormItem
                        class="flex flex-row items-center space-x-3 space-y-0"
                    >
                        <FormControl>
                            <Checkbox
                                :checked="value"
                                @update:checked="handleChange"
                            />
                        </FormControl>
                        <FormLabel class="font-normal">
                            Semantic Search
                        </FormLabel>
                    </FormItem>
                </FormField>
                <FormField v-slot="{ componentField }" name="k_value">
                    <Input
                        v-bind="componentField"
                        placeholder="K Value"
                        class="w-[100px]"
                    />
                </FormField>

            </div>
        </div>
    </form>
</template>
