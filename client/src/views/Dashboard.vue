<template>
    <v-container fluid>
        <v-btn @click="trainModel" class="primary">
            <v-icon left>mdi-replay</v-icon>
            {{ $t('trainModel') }}
        </v-btn>
    </v-container>
</template>

<script>
import { post } from '@/helpers/HTTPHelper'

export default {
    name: 'Dashboard',
    methods: {
        trainModel: async function () {
            const result = await post('/dashboard/train')
            if (result) {
                // TODO DISPLAY A SNACKBAR
            }
        },
    },
}
</script>

<style scoped>


</style>
