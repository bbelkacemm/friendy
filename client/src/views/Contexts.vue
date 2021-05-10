<template>
    <v-container fluid>
        <v-data-table :headers="headers"
                      :items="contexts"
                      :items-per-page="15"
                      v-model="selectedContexts"
                      :search="search"
                      show-select
                      class="elevation-1">
            <template v-slot:top>
                <v-container fluid>
                    <v-text-field :label="$t('search').toUpperCase()" v-model="search" hide-details="auto" dense outlined>
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

export default {
    name: 'Contexts',
    data: function () {
        return {
            headers: [
                {
                    text: this.$t('code'),
                    value: 'code',
                },
                {
                    text: this.$t('labelEn'),
                    value: 'label_en',
                },
                {
                    text: this.$t('labelFr'),
                    value: 'label_fr',
                },
                {
                    text: this.$t('labelAr'),
                    value: 'label_ar',
                },
                {
                    text: this.$t('propositionLabelEn'),
                    value: 'proposition_en',
                },
                {
                    text: this.$t('propositionLabelFr'),
                    value: 'proposition_fr',
                },
                {
                    text: this.$t('propositionLabelAr'),
                    value: 'proposition_ar',
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
}
</script>

<style scoped>

</style>
