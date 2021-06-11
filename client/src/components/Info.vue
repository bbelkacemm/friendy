<template>
    <v-dialog v-model="dialog" overlay-opacity=".1" width="50%" scrollable persistent>
        <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on" tile>
                <v-icon>mdi-information</v-icon>
            </v-btn>
        </template>

        <v-card>
            <v-card-title class="pa-0">
                <v-spacer></v-spacer>
                <v-btn icon tile @click="close">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-0">
                <v-container fluid class="text-center font-weight-bold">
                    {{ text }}
                </v-container>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
    name: 'Info',
    props: {
        text: String,
    },
    data: function () {
        return {
            dialog: false
        }
    },
    methods: {
        close: function () {
            this.dialog = false
            this.RESET_PATTERNS_STATE()
            this.RESET_RESPONSES_STATE()
            this.$emit('close')
        },
    },
}
</script>

<style scoped>

</style>
