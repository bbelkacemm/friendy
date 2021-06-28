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
            <!-- ENABLE -->
            <v-btn v-if="type === 'enable'" color="success" v-bind="attrs" v-on="on" tile text plain>
                <v-icon left>mdi-check</v-icon>
                {{ $t('enable') }}
            </v-btn>
            <!-- DISABLE -->
            <v-btn v-if="type === 'disable'" color="error" v-bind="attrs" v-on="on" tile text plain>
                <v-icon left>mdi-close</v-icon>
                {{ $t('disable') }}
            </v-btn>
            <!-- SET PROD -->
            <v-btn v-if="type === 'setProd'" color="success" v-bind="attrs" v-on="on" tile text plain>
                <v-icon left>mdi-check</v-icon>
                {{ $t('setProd') }}
            </v-btn>
            <!-- SET DEV -->
            <v-btn v-if="type === 'setDev'" color="secondary" v-bind="attrs" v-on="on" tile text plain>
                <v-icon left>mdi-close</v-icon>
                {{ $t('setDev') }}
            </v-btn>
            <!-- DELETE -->
            <v-btn v-if="type === 'delete'" color="error" v-bind="attrs" v-on="on" tile text plain :disabled="disabled">
                <v-icon left>mdi-delete</v-icon>
                {{ $t('delete') }}
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
        disabled: Boolean,
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
