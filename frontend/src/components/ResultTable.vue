<script setup>
import { defineProps } from "vue";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import {
    HoverCard,
    HoverCardContent,
    HoverCardTrigger,
} from "@/components/ui/hover-card";

const { data } = defineProps({
    data: Object,
});
</script>

<template>
    <div class="w-full px-10 py-7">
        <template v-if="data.docs?.length !== 0">
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Disease</TableHead>
                        <TableHead>Country</TableHead>
                        <TableHead>Code</TableHead>
                        <TableHead>Year</TableHead>
                        <TableHead>Value</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <template v-for="doc in data.docs">
                        <TableRow>
                            <HoverCard>
                                <HoverCardTrigger>
                                    <TableCell>{{ doc.cause_name }}</TableCell>
                                </HoverCardTrigger>
                                <HoverCardContent
                                    class="h-28 overflow-y-scroll p-0 text-white"
                                >
                                    <div class="bg-[#070708] p-3">
                                        {{ doc.description }}
                                    </div>
                                </HoverCardContent>
                            </HoverCard>
                            <TableCell>{{ doc.location_name }}</TableCell>
                            <TableCell>{{ doc.cca3[0] }}</TableCell>
                            <TableCell>{{ doc.year }}</TableCell>
                            <TableCell>{{ doc.val }}</TableCell>
                        </TableRow>
                    </template>
                </TableBody>
            </Table>
        </template>
    </div>
</template>
