<script setup>
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
</script>

<template>
    <div class="w-full px-10 py-7">
        <Table>
            <TableHeader>
                <TableRow>
                    <TableHead>Disease</TableHead>
                    <TableHead>Country</TableHead>
                    <TableHead>Year</TableHead>
                    <TableHead>Value</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                <TableRow>
                    <TableCell>1</TableCell>
                    <TableCell>2</TableCell>
                    <TableCell>3</TableCell>
                    <TableCell>3</TableCell>
                </TableRow>
                <TableRow>
                    <TableCell>4</TableCell>
                    <TableCell>5</TableCell>
                    <TableCell>6</TableCell>
                    <TableCell>2</TableCell>
                </TableRow>
                <TableRow>
                    <TableCell>7</TableCell>
                    <TableCell>8</TableCell>
                    <TableCell>9</TableCell>
                    <TableCell>1</TableCell>
                </TableRow>
            </TableBody>
        </Table>
    </div>
</template>
