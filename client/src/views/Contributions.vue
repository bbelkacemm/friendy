<template>
    <v-container fluid>
        <v-toolbar dense elevation="0" class="black" dark>
            <v-toolbar-title></v-toolbar-title>
            <v-toolbar-items>
                <contribution-form add v-on:close="`${contributionFormKey++}-add`" :key="contributionFormKey"/>
            </v-toolbar-items>
        </v-toolbar>

        <v-data-table :headers="headers"
                      :items="contributions"
                      :items-per-page="5"
                      v-model="selectedContributions"
                      show-select
                      class="elevation-1">
            <template v-slot:item.description="{item}">
                <div v-if="item.description">
                    {{item.description}}
                </div>
                <v-icon v-else>mdi-minus</v-icon>
            </template>
            <template v-slot:item.status="{item}">
                <v-icon v-if="item.status === 'pending'">mdi-timer-sand</v-icon>
                <v-icon v-if="item.status === 'valid'" color="green">mdi-check</v-icon>
                <v-icon v-if="item.status === 'invalid'" color="error">mdi-close</v-icon>
            </template>
            <template v-slot:item.createdAt="{item}">
                <div v-if="item['createdAt']">
                    {{formatDate(item['createdAt']).toUpperCase()}}
                </div>
                <v-icon v-else>mdi-minus</v-icon>
            </template>
            <template v-slot:item.validatedAt="{item}">
                <div v-if="item['validatedAt']">
                    {{formatDate(item['validatedAt']).toUpperCase()}}
                </div>
                <v-icon v-else>mdi-minus</v-icon>
            </template>
        </v-data-table>
    </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import ContributionForm from '@/components/ContributionForm'

export default {
    name: 'Contributions',
    components: { ContributionForm },
    data: function () {
        return {
            headers: [
                {
                    text: this.$t('title'),
                    value: 'title',
                },
                {
                    text: this.$t('description'),
                    value: 'description',
                },
                {
                    text: this.$t('createdAt'),
                    value: 'createdAt',
                },
                {
                    text: this.$t('validatedAt'),
                    value: 'validatedAt',
                },
                {
                    text: this.$t('status'),
                    value: 'status'
                },
            ],
            selectedContributions: [],
            contributionFormKey: 0,
        }
    },
    computed: {
        ...mapGetters('contributions', ['contributions']),
    },
}
</script>

<style scoped>

</style>
