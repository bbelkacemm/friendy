<template>
    <v-container fluid>
        <v-toolbar dense elevation="0" class="primary" dark>
            <v-toolbar-title></v-toolbar-title>
            <v-toolbar-items>
                <contribution-form add v-on:close="onClose" :key="`${formKey}-add`"/>
                <contribution-form v-if="selectedContributions[0] && selectedContributions.length === 1" edit
                                   v-on:close="onClose" :key="`${formKey}-edit`"
                                   :contribution="selectedContributions[0]"/>
                <v-btn v-else plain disabled>
                    <v-icon left>mdi-pencil</v-icon>
                    {{ $t('edit') }}
                </v-btn>

                <v-btn v-on:click="validateContribution"
                       v-if="selectedContributions[0] && selectedContributions.length === 1 && (selectedContributions[0].status === 'pending' || selectedContributions[0].status === 'invalid')"
                       plain>
                    <v-icon left>mdi-check</v-icon>
                    {{ $t('validate') }}
                </v-btn>
                <v-btn v-else plain disabled>
                    <v-icon left>mdi-check</v-icon>
                    {{ $t('validate') }}
                </v-btn>
                <v-btn v-on:click="refuseContribution"
                       v-if="selectedContributions[0] && selectedContributions.length === 1 && (selectedContributions[0].status === 'pending' || selectedContributions[0].status === 'valid')"
                       plain>
                    <v-icon left>mdi-close</v-icon>
                    {{ $t('refuse') }}
                </v-btn>
                <v-btn v-else disabled plain>
                    <v-icon left>mdi-close</v-icon>
                    {{ $t('refuse') }}
                </v-btn>

                <v-btn v-if="selectedContributions[0]" plain v-on:click="removeContribution">
                    <v-icon left>mdi-delete</v-icon>
                    {{ $t('delete') }}
                </v-btn>
            </v-toolbar-items>
        </v-toolbar>

        <v-data-table :headers="headers"
                      :items="contributions"
                      :items-per-page="13"
                      sort-by="status"
                      :search="search"
                      v-model="selectedContributions"
                      show-select
                      class="elevation-1">
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

            <template v-slot:item.description="{item}">
                <div v-if="item.description">
                    {{ item.description }}
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
                    {{ formatDate(item['createdAt']).toUpperCase() }}
                </div>
                <v-icon v-else>mdi-minus</v-icon>
            </template>
            <template v-slot:item.validatedAt="{item}">
                <div v-if="item['validatedAt']">
                    {{ formatDate(item['validatedAt']).toUpperCase() }}
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
import { mapActions, mapGetters } from 'vuex'
import ContributionForm from '@/components/ContributionForm'
import { post, remove } from '@/helpers/HTTPHelper'

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
                    value: 'status',
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
    methods: {
        onClose: function () {
            this.formKey++
            this.selectedContributions = []
        },
        validateContribution: async function () {
            const contribution = await post(`/contributions/contribution/${this.selectedContributions[0].id}`, {
                'status': 'valid',
                'user_id': this.user.id,
            })
            this.editContribution(contribution)
            this.selectedContributions = []
        },
        refuseContribution: async function () {
            const contribution = await post(`/contributions/contribution/${this.selectedContributions[0].id}`, {
                'status': 'invalid',
                'user_id': this.user.id,
            })
            this.editContribution(contribution)
            this.selectedContributions = []
        },
        removeContribution: async function () {
            const result = await remove(`/contributions/contribution/${this.selectedContributions[0].id}`)
            if (result.value) {
                this.deleteContribution(this.selectedContributions[0])
                this.selectedContributions = []
            }
        },
        ...mapActions('contributions', ['editContribution', 'deleteContribution']),
    },
}
</script>

<style scoped>

</style>
