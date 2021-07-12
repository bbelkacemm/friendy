<template>
    <v-container fluid class="pa-4 fill-height">
        <v-row no-gutters>
            <!-- PENDING CONTRIBUTORS -->
            <v-col class="dashboard-card-border three-rows pa-2 ma-2">
                <div class="two-columns">
                    <div class="subtitle-1">
                        <v-icon>mdi-timer-sand</v-icon>
                        {{ pendingContributors.length }} {{ $t('pendingContributors') }}
                    </div>
                    <v-btn to="users" target="_blank" color="success" tile plain text>
                        {{ $t('users') }}
                        <v-icon right>mdi-arrow-top-right-thick</v-icon>
                    </v-btn>
                </div>
                <v-divider></v-divider>
                <v-data-table :headers="pendingContributorsHeaders" :items="pendingContributors"
                              dense></v-data-table>
            </v-col>
            <!-- PENDING CONTRIBUTIONS -->
            <v-col class="dashboard-card-border three-rows pa-2 ma-2">
                <div class="two-columns">
                    <div class="subtitle-1">
                        <v-icon>mdi-timer-sand</v-icon>
                        {{ pendingContributors.length }} {{ $t('pendingContributions') }}
                    </div>
                    <v-btn to="contributions" target="_blank" color="success" tile plain text>
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
            </v-col>
        </v-row>
        <v-row no-gutters>
            <!-- IMPORT DATA -->
            <v-col class="three-rows dashboard-card-border pa-2 ma-2">
                <div class="two-columns">
                    <div>
                        <v-icon>mdi-database</v-icon>
                        {{ capitalizeFirst($t('importData')) }}
                    </div>
                    <v-btn to="contexts" target="_blank" color="success" tile plain text>
                        {{ $t('contexts') }}
                        <v-icon right>mdi-arrow-top-right-thick</v-icon>
                    </v-btn>
                </div>
                <v-divider></v-divider>
                <v-form ref="importForm" v-on:submit.prevent="">
                    <v-row>
                        <v-col>
                            <v-file-input v-model="file" :rules="[validationRules.required]" hide-details="auto"
                                          outlined dense></v-file-input>
                        </v-col>
                        <v-col>
                            <v-autocomplete class="mb-2" :label="$t('language').toUpperCase()"
                                            v-model="lang"
                                            :rules="[validationRules.required]"
                                            hide-details="auto" :items="languagesList" outlined
                                            dense></v-autocomplete>
                        </v-col>
                    </v-row>
                    <v-btn v-on:click="importData" class="primary" block plain>
                        <v-icon left>mdi-database-import</v-icon>
                        {{ $t('import') }}
                    </v-btn>
                </v-form>
            </v-col>
            <!-- TRAIN MODEL -->
            <v-col class="three-rows dashboard-card-border pa-2 ma-2">
                <div class="two-columns">
                    <div>
                        <v-icon>mdi-brain</v-icon>
                        {{ capitalizeFirst($t('trainModel')) }}
                    </div>
                    <v-btn to="models" target="_blank" color="success" tile plain text>
                        {{ $t('models') }}
                        <v-icon right>mdi-arrow-top-right-thick</v-icon>
                    </v-btn>
                </div>
                <v-divider></v-divider>
                <div class="center-items">
                    <div v-if="isTraining" class="justify-center">
                        {{ $t('isTraining') }}
                    </div>
                    <div v-else>
                        <div v-if="models.length === 0">
                            {{ $t('noModel') }}
                        </div>
                        <div v-else>
                            {{ capitalizeFirst($t('lastTrain')) }}
                            {{ formatDate(models[models.length - 1]['createdAt'], true).toUpperCase() }}
                        </div>
                    </div>
                </div>
                <v-btn @click="trainModel" plain class="primary" block>
                    <v-icon v-if="!isTraining" left>mdi-replay</v-icon>
                    <v-progress-circular class="me-2" size="16" v-else indeterminate
                                         color="white"></v-progress-circular>
                    {{ $t('trainModel') }}
                </v-btn>
            </v-col>
        </v-row>
        <v-row no-gutters>
            <v-col class="three-rows dashboard-card-border pa-2 ma-2">
                <div class="two-columns">
                    <div>
                        <v-icon>mdi-chart-line</v-icon>
                        {{ capitalizeFirst($t('contributionsPerMonth')) }}
                    </div>
                </div>
                <v-divider></v-divider>
                <line-chart :chart-data="contributionsStats.data" :options="contributionsStats.options"/>
            </v-col>
            <v-col class="three-rows dashboard-card-border pa-2 ma-2">
                <div class="two-columns">
                    <div>
                        <v-icon>mdi-chart-bar</v-icon>
                        {{ capitalizeFirst($t('usersPerRole')) }}
                    </div>
                </div>
                <v-divider></v-divider>
                <bar-chart :chart-data="usersStats.data" :options="usersStats.options"/>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { get, post } from '@/helpers/HTTPHelper'
import { mapActions, mapGetters } from 'vuex'
import LineChart from '@/components/charts/LineChart'
import BarChart from '@/components/charts/BarChart'

export default {
    name: 'Dashboard',
    components: { BarChart, LineChart },
    created: async function () {
        let result = await get('/statistics/contributions-per-month')
        if (result.value) {
            this.contributionsPerMonth = result.data
        }
        result = await get('/statistics/users-per-role')
        if (result.value) {
            this.roles = result.data.map(i => this.capitalizeFirst(i.role))
            this.usersPerRole = result.data.map(i => i.users)
        }
    },
    data: function () {
        return {
            contributionsPerMonth: [],
            usersPerRole: [],
            roles: [],
            isTraining: false,
            file: null,
            lang: null,
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
        contributionsStats: function () {
            return {
                data: {
                    labels: this.months,
                    datasets: [
                        {
                            backgroundColor: 'transparent',
                            borderColor: 'rgba(1, 116, 188, 0.50)',
                            pointBackgroundColor: '#000',
                            data: this.contributionsPerMonth,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        display: false,
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                                precision: 0,
                            },
                        }],
                    },
                    title: {
                        display: true,
                        text: this.capitalizeFirst(this.$t('contributionsPerMonth')),
                    },
                },
            }
        },
        usersStats: function () {
            return {
                data: {
                    labels: this.roles,
                    datasets: [
                        {
                            backgroundColor: 'rgba(1, 116, 188, 0.50)',
                            data: this.usersPerRole,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {
                        display: false,
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                                precision: 0,
                            },
                        }],
                    },
                    title: {
                        display: true,
                        text: this.capitalizeFirst(this.$t('usersPerRole')),
                    },
                },
            }
        },
        ...mapGetters('models', ['models']),
        ...mapGetters('users', ['pendingContributors']),
        ...mapGetters('contributions', ['pendingContributions']),
    },
    methods: {
        importData: function () {
            if (this.$refs.importForm.validate()) {
                post(`/data/import/${this.lang}`, this.file, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
            }
        },
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
