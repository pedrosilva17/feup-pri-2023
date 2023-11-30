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

const onSubmit = handleSubmit((values) => {
    console.log("adkjfasdfkjnasd");
    console.log("Form submitted!", values);
});
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
                <FormField v-slot="{ componentField }" name="country">
                    <Select v-bind="componentField">
                        <SelectTrigger class="w-[180px]">
                            <SelectValue placeholder="Country" />
                        </SelectTrigger>
                        <SelectContent class="max-h-96">
                            <SelectGroup>
                                <!-- TODO: FETCH COUNTRIES FROM BACKEND -->
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
