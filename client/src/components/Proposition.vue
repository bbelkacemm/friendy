<template>
    <v-card @click="clicked" elevation="2" class="pa-0 ma-2" style="background-color: #F5F5F5; border-radius: 32px;">
        <v-card-text class="pa-3">
            {{ value }}
        </v-card-text>
    </v-card>
</template>

<script>
export default {
    name: 'Proposition',
    props: {
        value: String,
    },
    methods: {
        clicked: async function () {
            this.$emit('clicked', this.value)
        },
    },
}
</script>

<style scoped>

</style>
