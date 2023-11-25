<script setup>
import TableRow from "./TableRow.vue";
import TableCell from "./TableCell.vue";
import { cn } from "@/lib/utils";

const props = defineProps({
    class: { type: String, required: false, default: "" },
    colspan: { type: Number, required: false, default: 1 },
});
</script>

<template>
    <TableRow>
        <TableCell
            :class="
                cn(
                    'whitespace-nowrap p-4 align-middle text-sm text-foreground',
                    props.class,
                )
            "
            :colspan="props.colspan"
        >
            <div class="flex items-center justify-center py-10">
                <slot />
            </div>
        </TableCell>
    </TableRow>
</template>
