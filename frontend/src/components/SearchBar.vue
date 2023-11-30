<script setup>
import { ref } from "vue";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger,
} from "@/components/ui/collapsible";
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

const isOpen = ref(false);
const formSchema = toTypedSchema(
    z.object({
        search: z.string(),
        sex: z.string(),
        country: z.string(),
        age: z.string(),
        min_year: z.string(),
        max_year: z.string(),
        min_value: z.string(),
        max_value: z.string(),
    }),
);
const form = useForm({
    validationSchema: formSchema,
});
const onSubmit = form.handleSubmit((values) => {
    console.log("Form submitted!", values);
});
</script>

<template>
    <form @submit="onSubmit">    
    <div class="flex w-fit flex-row gap-4 p-7">
        <FormField v-slot="{componentField}" name="search">
            <Input v-bind="componentField" placeholder="Search..." class="w-96" />
        </FormField>
        <Button type="submit">Search</Button>
    </div>
    <Collapsible v-model:open="isOpen" class="space-y-2">
        <div class="flex items-center justify-center space-x-4 px-4">
            <CollapsibleTrigger as-child>
                <Button variant="secondary"
                    ><span class="pr-2 font-bold">+</span> Advanced
                    Search</Button
                >
            </CollapsibleTrigger>
        </div>
        <CollapsibleContent class="flex flex-col items-center gap-2 space-y-2 p-2">
                <div class="grid grid-cols-4 gap-7">
                    <FormField v-slot="{componentField}" name="sex">
                        <Select v-bind="componentFiled">
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
                    <FormField v-slot="{componentField}" name="country">
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
                    <FormField v-slot="{componentField}" name="age">
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
                    <div
                        class="flex flex-row items-center justify-center gap-2"
                    >
                        <FormField v-slot="{componentField}" name="min_year">
                            <Select v-bind="componentField">
                                <SelectTrigger class="min-w-[50px]">
                                    <SelectValue placeholder="Year" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectGroup>
                                        <!-- TODO: GET YEARS FROM BACKEND -->
                                        <SelectItem value="apple">2020</SelectItem>
                                        <SelectItem value="1">2020</SelectItem>
                                        <SelectItem value="11">2020</SelectItem>
                                        <SelectItem value="12">2020</SelectItem>
                                        <SelectItem value="13">2020</SelectItem>
                                    </SelectGroup>
                                </SelectContent>
                            </Select>
                        </FormField>
                        to
                        <FormField v-slot="{componentField}" name="max_year">
                            <Select v-bind="componentField">
                                <SelectTrigger class="min-w-[50px]">
                                    <SelectValue placeholder="Year" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectGroup>
                                        <!-- TODO: GET YEARS FROM BACKEND -->
                                        <SelectItem value="apple">2020</SelectItem>
                                        <SelectItem value="1">2020</SelectItem>
                                        <SelectItem value="11">2020</SelectItem>
                                        <SelectItem value="12">2020</SelectItem>
                                        <SelectItem value="13">2020</SelectItem>
                                    </SelectGroup>
                                </SelectContent>
                            </Select>
                        </FormField>
                    </div>
                </div>
                <div class="flex flex-row items-center gap-3">
                    <Label>Value</Label>
                    <FormField v-slot="{componentField}" name="min_value">
                        <Input v-bind="componentField" placeholder="Min. Value" class="w-[100px]" />
                    </FormField>
                    -
                    <FormField v-slot="{componentField}" name="max_value">
                        <Input v-bind="componentField" placeholder="Max. Value" class="w-[100px]" />
                    </FormField>
                </div>
            </CollapsibleContent>
        </Collapsible>
    </form>
</template>
