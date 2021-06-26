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
                        {{ $t('lastTrain') }} {{ formatDate(models[models.length - 1]['createdAt'], true).toUpperCase()
                        }}
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
        <v-row no-gutters>
            <!-- PENDING CONTRIBUTORS -->
            <v-col>
                <v-container fluid>
                    <div class="pb-2" id="pending-contributors-header">
                        <div class="subtitle-1">{{ pendingContributors.length }} {{ $t('pendingContributors') }}</div>
                        <v-btn to="users" target="_blank" tile plain text>
                            {{ $t('users') }}
                            <v-icon right>mdi-arrow-top-right-thick</v-icon>
                        </v-btn>
                    </div>
                    <v-divider></v-divider>
                    <v-data-table :headers="pendingContributorsHeaders" :items="pendingContributors"
                                  dense></v-data-table>
                </v-container>
            </v-col>
            <v-divider vertical></v-divider>
            <!-- PENDING CONTRIBUTIONS -->
            <v-col>
                <v-container fluid>
                    <div class="pb-2" id="pending-contributions-header">
                        <div class="subtitle-1">{{ pendingContributors.length }} {{ $t('pendingContributions') }}</div>
                        <v-btn to="contributions" target="_blank" tile plain text>
                            {{ $t('contributions') }}
                            <v-icon right>mdi-arrow-top-right-thick</v-icon>
                        </v-btn>
                    </div>
                    <v-divider></v-divider>

                    <v-data-table :headers="pendingContributionsHeaders" :items="pendingContributions" dense>
                        <template v-slot:item.contributor="{item}">
                            <div v-if="item.contributor">
                                {{ item.contributor.firstName + ' ' + item.contributor.lastName }}
                            </div>
                            <div v-else>
                                <v-icon>mdi-minus</v-icon>
                            </div>
                        </template>
                        <template v-slot:item.createdAt="{item}">
                            <div v-if="item['createdAt']">
                                {{ formatDate(item['createdAt']).toUpperCase() }}
                            </div>
                            <v-icon v-else>mdi-minus</v-icon>
                        </template>
                    </v-data-table>
                </v-container>
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
            pendingContributorsHeaders: [
                {
                    text: this.$t('username').toUpperCase(),
                    value: 'username',
                },
                {
                    text: this.$t('firstName').toUpperCase(),
                    value: 'firstName',
                },
                {
                    text: this.$t('lastName').toUpperCase(),
                    value: 'lastName',
                },
            ],
            pendingContributionsHeaders: [
                {
                    text: this.$t('title').toUpperCase(),
                    value: 'title',
                },
                {
                    text: this.$t('contributor').toUpperCase(),
                    value: 'contributor',
                },
                {
                    text: this.$t('createdAt').toUpperCase(),
                    value: 'createdAt',
                },
            ],
        }
    },
    computed: {
        ...mapGetters('models', ['models']),
        ...mapGetters('users', ['pendingContributors']),
        ...mapGetters('contributions', ['pendingContributions']),
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

#pending-contributors-header
    display: grid
    grid-template-columns: 1fr auto
    align-items: center

#pending-contributions-header
    display: grid
    grid-template-columns: 1fr auto
    align-items: center
</style>
