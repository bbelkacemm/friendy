<template>
    <v-container fluid>
        <!-- TODO GET VALID CONTEXTS -->
        <v-toolbar dense elevation="0" class="black" dark>
        </v-toolbar>

        <v-data-table :headers="headers"
                      :items="contexts"
                      :items-per-page="5"
                      v-model="selectedContexts"
                      show-select
                      class="elevation-1">
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
        }
    },
    computed: {
        ...mapGetters('contexts', ['contexts']),
    },
}
</script>

<style scoped>

</style>
