<script setup>
import { Label } from "radix-vue";
import { cn } from "@/lib/utils";

const props = defineProps({
    for: { type: String, required: false },
    asChild: { type: Boolean, required: false },
    as: { type: null, required: false },
    class: { type: String, required: false },
});
</script>

<template>
    <Label
        v-bind="props"
        :class="
            cn(
                'block text-left text-sm font-medium tracking-tight text-foreground',
                props.class,
            )
        "
    >
        <slot />
    </Label>
</template>
