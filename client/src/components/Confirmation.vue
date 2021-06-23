<template>
    <v-dialog v-model="dialog" overlay-opacity=".1" width="50%" scrollable persistent>
        <template v-slot:activator="{ on, attrs }">
            <!-- VALIDATE -->
            <v-btn v-if="type === 'validate'" color="success" v-bind="attrs" v-on="on" tile text plain>
                <v-icon left>mdi-check</v-icon>
                {{ $t('validate') }}
            </v-btn>
            <!-- INVALIDATE -->
            <v-btn v-if="type === 'invalidate'" color="error" v-bind="attrs" v-on="on" tile text plain>
                <v-icon left>mdi-close</v-icon>
                {{ $t('invalidate') }}
            </v-btn>
        </template>

        <v-card>
            <v-card-title class="pa-0 ps-3">
                {{ header }}
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-0">
                <v-container fluid>
                    {{ description }}
                </v-container>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions class="pa-0">
                <v-btn @click="cancel" color="error">
                    {{ $t('cancel') }}
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn @click="accept" color="primary">
                    {{ $t('ok') }}
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
    name: 'Confirmation',
    props: {
        header: String,
        description: String,
        type: String,
    },
    data: function () {
        return {
            dialog: false,
        }
    },
    methods: {
        accept: function () {
            this.$emit('accept')
            this.dialog = false
        },
        cancel: function () {
            this.$emit('cancel')
            this.dialog = false
        },
    },
}
</script>

<style scoped>

</style>
