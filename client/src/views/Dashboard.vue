<template>
    <v-container fluid>
        <v-row id="train-container" class="grey lighten-4 ma-2">
            <v-col align-self="center">
                <div v-if="isTraining">
                    {{ $t('isTraining') }}
                </div>
                <div v-else class="">
                    <div v-if="models.length === 0">
                        {{ $t('noModel') }}
                    </div>
                    <div v-else>
                        {{ $t('lastTrain') }} {{ formatDate(models[models.length - 1]['createdAt'], true).toUpperCase() }}
                    </div>
                </div>
            </v-col>
            <v-col align-self="center">
                <v-btn @click="trainModel" plain class="primary">
                    <v-icon v-if="!isTraining" left>mdi-replay</v-icon>
                    <v-progress-circular class="me-4" size="24" v-else indeterminate
                                         color="white"></v-progress-circular>
                    {{ $t('trainModel') }}
                </v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { post } from '@/helpers/HTTPHelper'
import { mapActions, mapGetters } from 'vuex'

export default {
    name: 'Dashboard',
    data: function () {
        return {
            isTraining: false,
        }
    },
    computed: {
        ...mapGetters('models', ['models']),
    },
    methods: {
        trainModel: async function () {
            this.isTraining = true
            const result = await post('/dashboard/train', {
                'user_id': this.user.id,
            })
            this.isTraining = false
            this.setModels()
            if (result) {
                // TODO DISPLAY A SNACKBAR
            }
        },
        ...mapActions('models', ['setModels']),
    },
}
</script>

<style scoped lang="sass">

#train-container
    display: grid
    grid-template-columns: 1fr auto

</style>
