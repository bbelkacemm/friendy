<template>
    <v-container fluid>
        <v-toolbar dense elevation="0">
            <v-toolbar-items>
                <!-- DETAILS -->
                <context v-if="selectedContexts[0]" :context="selectedContexts[0]" v-on:close="clearSelection"/>
                <v-btn v-else plain disabled>
                    <v-icon left>mdi-file-document</v-icon>
                    {{ $t('details') }}
                </v-btn>
            </v-toolbar-items>
        </v-toolbar>

        <v-divider></v-divider>

        <v-data-table :headers="headers"
                      :items="contexts"
                      :items-per-page="15"
                      v-model="selectedContexts"
                      :search="search"
                      show-select
                      single-select>
            <template v-slot:top>
                <v-container fluid>
                    <v-text-field :label="$t('search').toUpperCase()" v-model="search" hide-details="auto" dense
                                  outlined>
                        <template v-slot:append>
                            <v-icon>mdi-magnify</v-icon>
                        </template>
                    </v-text-field>
                </v-container>
            </template>
        </v-data-table>
    </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import Context from '@/components/Context'

export default {
    name: 'Contexts',
    components: { Context },
    data: function () {
        return {
            headers: [
                {
                    text: this.$t('code'),
                    value: 'code',
                },
                {
                    text: this.$t('labelEn'),
                    value: 'labelEn',
                },
                {
                    text: this.$t('labelFr'),
                    value: 'labelFr',
                },
                {
                    text: this.$t('labelAr'),
                    value: 'labelAr',
                },
                {
                    text: this.$t('propositionLabelEn'),
                    value: 'propositionEn',
                },
                {
                    text: this.$t('propositionLabelFr'),
                    value: 'propositionFr',
                },
                {
                    text: this.$t('propositionLabelAr'),
                    value: 'propositionAr',
                },
            ],
            selectedContexts: [],
            contributionFormKey: 0,
            search: null,
        }
    },
    computed: {
        ...mapGetters('contexts', ['contexts']),
    },
    methods: {
        clearSelection: function () {
            this.selectedContexts = []
        }
    }
}
</script>

<style scoped>

</style>
