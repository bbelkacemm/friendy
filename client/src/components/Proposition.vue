<template>
    <v-card @click="clicked" elevation="0" class="ps-4 pe-4 pt-2 pb-2 ma-2" style="background-color: #006C67">
        <div class="font-weight-bold white--text">
            {{ value }}
        </div>
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
