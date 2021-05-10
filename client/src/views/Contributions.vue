<template>
    <v-container fluid>
        <v-toolbar dense elevation="0" class="primary" dark>
            <v-toolbar-title></v-toolbar-title>
            <v-toolbar-items>
                <contribution-form add v-on:close="formKey++" :key="`${formKey}-add`"/>
            </v-toolbar-items>
        </v-toolbar>

        <v-data-table :headers="headers"
                      :items="contributions"
                      :items-per-page="13"
                      :search="search"
                      v-model="selectedContributions"
                      show-select
                      class="elevation-1">
            <template v-slot:top>
                <v-container fluid>
                    <v-text-field :label="$t('search')" v-model="search" hide-details="auto" dense outlined>
                        <template v-slot:append>
                            <v-icon>mdi-magnify</v-icon>
                        </template>
                    </v-text-field>
                </v-container>
            </template>

            <template v-slot:item.description="{item}">
                <div v-if="item.description">
                    {{item.description}}
                </div>
                <v-icon v-else>mdi-minus</v-icon>
            </template>
            <template v-slot:item.contributor="{item}">
                <div v-if="item.contributor">
                    {{ item.contributor.firstName + ' ' + item.contributor.lastName }}
                </div>
                <div v-else>
                    <v-icon>mdi-minus</v-icon>
                </div>
            </template>
            <template v-slot:item.validator="{item}">
                <div v-if="item.validator">
                    {{ item.validator.firstName + ' ' + item.validator.lastName }}
                </div>
                <div v-else>
                    <v-icon>mdi-minus</v-icon>
                </div>
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
            <template v-slot:item.status="{item}">
                <v-icon v-if="item.status === 'pending'">mdi-timer-sand</v-icon>
                <v-icon v-if="item.status === 'valid'" color="green">mdi-check</v-icon>
                <v-icon v-if="item.status === 'invalid'" color="error">mdi-close</v-icon>
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
                    text: this.$t('title').toUpperCase(),
                    value: 'title',
                },
                {
                    text: this.$t('description').toUpperCase(),
                    value: 'description',
                },
                {
                    text: this.$t('contributor').toUpperCase(),
                    value: 'contributor',
                },
                {
                    text: this.$t('validator').toUpperCase(),
                    value: 'validator',
                },
                {
                    text: this.$t('createdAt').toUpperCase(),
                    value: 'createdAt',
                },
                {
                    text: this.$t('validatedAt').toUpperCase(),
                    value: 'validatedAt',
                },
                {
                    text: this.$t('status').toUpperCase(),
                    value: 'status'
                },
            ],
            selectedContributions: [],
            formKey: 0,
            search: null,
        }
    },
    computed: {
        ...mapGetters('contributions', ['contributions']),
    },
}
</script>

<style scoped>

</style>
