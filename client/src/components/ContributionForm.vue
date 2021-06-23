<template>
    <v-dialog v-model="dialog" overlay-opacity=".1" scrollable width="75%" persistent>
        <template v-slot:activator="{ on, attrs }">
            <v-btn plain v-bind="attrs" v-on="on" v-if="add">
                <v-icon left>mdi-plus</v-icon>
                {{ $t('add') }}
            </v-btn>

            <v-btn plain v-bind="attrs" v-on="on" v-if="edit">
                <v-icon left>mdi-pencil</v-icon>
                {{ $t('edit') }}
            </v-btn>
        </template>
        <v-form v-on:submit.prevent="" ref="form">
            <v-card>
                <v-card-title class="pa-0">
                    <v-spacer></v-spacer>
                    <v-btn icon tile @click="close">
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pa-0">
                    <v-container fluid>
                        <!-- CONTRIBUTION'S FORM -->
                        <v-form v-on:submit.prevent="" ref="contributionForm">
                            <div class="two-columns">
                                <v-text-field class="mb-2" v-model="title" :rules="[validationRules.required]"
                                              hide-details="auto" :label="$t('title').toUpperCase()" outlined
                                              dense></v-text-field>
                                <v-combobox class="mb-2" :label="$t('contributionLanguage').toUpperCase()"
                                            v-model="contributionLanguage"
                                            :rules="[validationRules.required]"
                                            hide-details="auto" :items="contributionsLanguagesList" outlined
                                            dense></v-combobox>
                            </div>
                            <v-textarea class="mb-2" v-model="description" :label="$t('description').toUpperCase()"
                                        hide-details="auto" height="75" outlined dense></v-textarea>
                        </v-form>
                        <!-- CONTEXT'S FORM -->
                        <v-form v-on:submit.prevent="" ref="contextForm">
                            <v-text-field class="mb-2" v-model="code" :rules="[validationRules.required]"
                                          outlined
                                          dense
                                          hide-details="auto" :label="$t('code').toUpperCase()"></v-text-field>
                            <v-row no-gutters>
                                <v-col v-if="showField('en')">
                                    <v-text-field class="mb-2" v-model="contextLabelEn"
                                                  :rules="[validationRules.required]"
                                                  outlined
                                                  dense
                                                  hide-details="auto"
                                                  :label="$t('contextLabelEn').toUpperCase()"></v-text-field>
                                </v-col>
                                <v-col v-if="showField('fr')">
                                    <v-text-field class="mb-2" v-model="contextLabelFr"
                                                  :rules="[validationRules.required]"
                                                  outlined
                                                  dense
                                                  hide-details="auto"
                                                  :label="$t('contextLabelFr').toUpperCase()"></v-text-field>
                                </v-col>
                                <v-col v-if="showField('ar')">
                                    <v-text-field class="mb-2" v-model="contextLabelAr"
                                                  :rules="[validationRules.required]"
                                                  outlined
                                                  dense
                                                  hide-details="auto"
                                                  :label="$t('contextLabelAr').toUpperCase()"></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row no-gutters>
                                <v-col v-if="showField('en')">
                                    <v-text-field class="mb-2" v-model="propositionLabelEn"
                                                  :rules="[validationRules.required]"
                                                  outlined
                                                  dense
                                                  hide-details="auto"
                                                  :label="$t('propositionLabelEn').toUpperCase()"></v-text-field>
                                </v-col>
                                <v-col v-if="showField('fr')">
                                    <v-text-field class="mb-2" v-model="propositionLabelFr"
                                                  :rules="[validationRules.required]"
                                                  outlined
                                                  dense
                                                  hide-details="auto"
                                                  :label="$t('propositionLabelFr').toUpperCase()"></v-text-field>
                                </v-col>
                                <v-col v-if="showField('ar')">
                                    <v-text-field class="mb-2" v-model="propositionLabelAr"
                                                  :rules="[validationRules.required]"
                                                  outlined
                                                  dense
                                                  hide-details="auto"
                                                  :label="$t('propositionLabelAr').toUpperCase()"></v-text-field>
                                </v-col>
                            </v-row>
                        </v-form>
                    </v-container>
                    <v-tabs v-model="tab" dark background-color="primary">
                        <v-tab v-for="item in tabs" :key="item">
                            {{ item }}
                        </v-tab>
                    </v-tabs>
                    <v-tabs-items v-model="tab">
                        <v-tab-item>
                            <v-container fluid>
                                <!-- PATTERN'S FORM -->
                                <v-form v-on:submit.prevent="" ref="patternForm">
                                    <div id="pattern-form">
                                        <v-text-field class="mb-2" v-model="patternLabel"
                                                      :rules="[validationRules.required]"
                                                      outlined
                                                      dense hide-details="auto"
                                                      :label="$t('patternLabel').toUpperCase()"></v-text-field>
                                        <v-combobox class="mb-2" :label="$t('language').toUpperCase()"
                                                    v-model="patternLanguage"
                                                    :rules="[validationRules.required]"
                                                    hide-details="auto" :items="languagesList" outlined
                                                    dense></v-combobox>
                                        <v-btn @click="pushPattern" icon tile color="primary">
                                            <v-icon>mdi-plus</v-icon>
                                        </v-btn>
                                        <v-btn @click="updatePattern" icon tile color="secondary"
                                               :disabled="!selectedPatterns[0]">
                                            <v-icon>mdi-pencil</v-icon>
                                        </v-btn>
                                        <v-btn @click="removePattern" icon tile color="error"
                                               :disabled="!selectedPatterns[0]">
                                            <v-icon>mdi-delete</v-icon>
                                        </v-btn>
                                        <info :text="patternsInfo"/>
                                    </div>
                                </v-form>
                                <v-data-table :headers="patternsHeaders" :items="filteredPatterns"
                                              v-model="selectedPatterns"
                                              :items-per-page="5" v-on:item-selected="onPatternSelect" item-key="label"
                                              show-select
                                              single-select></v-data-table>
                            </v-container>
                        </v-tab-item>
                        <v-tab-item>
                            <v-container fluid>
                                <!-- RESPONSE'S FORM -->
                                <v-form v-on:submit.prevent="" ref="responseForm">
                                    <div id="response-form">
                                        <v-text-field class="mb-2" v-model="responseLabel"
                                                      :rules="[validationRules.required]"
                                                      outlined
                                                      dense hide-details="auto"
                                                      :label="$t('responseLabel').toUpperCase()"></v-text-field>
                                        <v-combobox class="mb-2" :label="$t('language').toUpperCase()"
                                                    v-model="responseLanguage"
                                                    :rules="[validationRules.required]"
                                                    hide-details="auto" :items="languagesList" outlined
                                                    dense></v-combobox>
                                        <v-btn @click="pushResponse" icon tile color="primary">
                                            <v-icon>mdi-plus</v-icon>
                                        </v-btn>
                                        <v-btn @click="updateResponse" icon tile color="secondary"
                                               :disabled="!selectedResponses[0]">
                                            <v-icon>mdi-pencil</v-icon>
                                        </v-btn>
                                        <v-btn @click="removeResponse" icon tile color="error"
                                               :disabled="!selectedResponses[0]">
                                            <v-icon>mdi-delete</v-icon>
                                        </v-btn>
                                        <info :text="responsesInfo"/>
                                    </div>
                                </v-form>
                                <v-data-table :headers="responsesHeaders" :items="filteredResponses"
                                              :items-per-page="5" v-on:item-selected="onResponseSelect"
                                              v-model="selectedResponses" show-select item-key="label"
                                              single-select></v-data-table>
                            </v-container>
                        </v-tab-item>
                        <v-tab-item>
                            <v-container fluid>
                                <v-data-table :headers="contextsHeaders" :items="contexts" v-model="selectedContexts"
                                              show-select :items-per-page="5"></v-data-table>
                            </v-container>
                        </v-tab-item>
                    </v-tabs-items>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions class="pa-0">
                    <v-spacer></v-spacer>
                    <v-btn @click="save" text color="primary">
                        <v-icon left>mdi-content-save</v-icon>
                        {{ $t('save') }}
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-form>
        <v-snackbar v-model="errorSnackbar" class="d-print-none" color="error">
            <template v-slot:default>
                {{ $t(snackbarErrorMessage) }}
            </template>
            <template v-slot:action>
                <v-btn icon dark @click="errorSnackbar = false">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </template>
        </v-snackbar>
    </v-dialog>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex'
import { post } from '@/helpers/HTTPHelper'
import i18n from '@/i18n'
import Info from '@/components/Info'

export default {
    name: 'ContributionForm',
    components: { Info },
    props: {
        add: Boolean,
        edit: Boolean,
        contribution: Object,
    },
    created: function () {
        this.getContexts()
        this.RESET_PATTERNS_STATE()
        this.RESET_RESPONSES_STATE()
        if (this.edit) {
            this.title = this.contribution.title
            this.description = this.contribution.description
            this.code = this.contribution.context.code
            this.contextLabelEn = this.contribution.context.labelEn
            this.contextLabelFr = this.contribution.context.labelFr
            this.contextLabelAr = this.contribution.context.labelAr
            this.propositionLabelEn = this.contribution.context.propositionEn
            this.propositionLabelFr = this.contribution.context.propositionFr
            this.propositionLabelAr = this.contribution.context.propositionAr
            this.setPatterns(this.contribution.context.patterns.map(item => {
                item.status = 'skip'
                return item
            }))
            this.setResponses(this.contribution.context.responses.map(item => {
                item.status = 'skip'
                return item
            }))
            this.selectedContexts = this.contribution.context.contexts
        }
    },
    data: function () {
        return {
            tab: 0,
            tabs: [this.$t('patterns'), this.$t('responses'), this.$t('relatedContexts')],
            dialog: false,
            // CONTRIBUTION
            title: null,
            description: null,
            contributionLanguage: {
                text: i18n.t('fr'),
                value: 'fr',
            },
            // CONTEXT
            code: null,
            contextLabelEn: null,
            contextLabelFr: null,
            contextLabelAr: null,
            propositionLabelEn: null,
            propositionLabelFr: null,
            propositionLabelAr: null,
            // PATTERNS
            patternsInfo: `${this.$t('patternDescription')} - ${this.$t('patternExample')}`,
            patternLabel: null,
            patternLanguage: null,
            patternsHeaders: [
                {
                    text: this.$t('label').toUpperCase(),
                    value: 'label',
                },
                {
                    text: this.$t('language').toUpperCase(),
                    value: 'language',
                },
            ],
            selectedPatterns: [],
            // RESPONSES
            responsesInfo: `${this.$t('responseDescription')} - ${this.$t('responseExample')}`,
            responseLabel: null,
            responseLanguage: null,
            responsesHeaders: [
                {
                    text: this.$t('label').toUpperCase(),
                    value: 'label',
                },
                {
                    text: this.$t('language').toUpperCase(),
                    value: 'language',
                },
            ],
            selectedResponses: [],
            // RELATED CONTEXTS
            contextsHeaders: [
                {
                    text: this.$t('labelEn').toUpperCase(),
                    value: 'labelEn',
                },
                {
                    text: this.$t('labelFr').toUpperCase(),
                    value: 'labelFr',
                },
                {
                    text: this.$t('labelAr').toUpperCase(),
                    value: 'labelAr',
                },
            ],
            selectedContexts: [],
            // ERRORS
            errorSnackbar: false,
            snackbarErrorMessage: null,
        }
    },
    computed: {
        contributionsLanguagesList: function () {
            return [
                {
                    text: i18n.t('all'),
                    value: 'all',
                },
                ...this.languagesList,
            ]
        },
        ...mapGetters('contexts', ['contexts']),
        ...mapGetters('patterns', ['patterns', 'filteredPatterns']),
        ...mapGetters('responses', ['responses', 'filteredResponses']),
    },
    methods: {
        validate: function () {
            let valid = true
            // VALIDATE CONTRIBUTION'S FORM
            if (!this.$refs.contributionForm.validate()) valid = false
            // VALIDATE CONTEXT'S FORM
            if (!this.$refs.contextForm.validate()) valid = false
            // VALIDATE PATTERNS
            if (this.patterns.length === 0) {
                this.snackbarErrorMessage = this.$t('patternsRequired')
                this.errorSnackbar = true
                valid = false
            }
            // VALIDATE RESPONSES
            if (this.responses.length === 0) {
                this.snackbarErrorMessage = this.$t('responsesRequired')
                this.errorSnackbar = true
                valid = false
            }
            // VALIDATE PATTERNS/RESPONSES LANGUAGE MATCHING
            let patternsLanguageSet = new Set(this.patterns.map(p => p.language))
            let responsesLanguageSet = new Set(this.responses.map(r => r.language))
            let error = false
            if (patternsLanguageSet.size !== responsesLanguageSet.size) {
                error = true
            }
            if (!error) {
                for (let item of patternsLanguageSet) {
                    if (!responsesLanguageSet.has(item)) {
                        error = true
                        break
                    }
                }
            }
            if (error) {
                this.snackbarErrorMessage = this.$t('patternsResponsesLanguageMatch')
                this.errorSnackbar = true
                valid = false
            }
            return valid
        },
        save: async function () {
            if (this.validate()) {
                if (this.add) {
                    const result = await post('/contributions/contribution', {
                        contribution: {
                            'title': this.title,
                            'description': this.description,
                        },
                        context: {
                            'code': this.code,
                            'label_en': this.contextLabelEn,
                            'label_fr': this.contextLabelFr,
                            'label_ar': this.contextLabelAr,
                            'proposition_en': this.propositionLabelEn,
                            'proposition_fr': this.propositionLabelFr,
                            'proposition_ar': this.propositionLabelAr,
                        },
                        patterns: this.patterns,
                        responses: this.responses,
                        relatedContexts: this.selectedContexts.map(context => context.code),
                        user_id: this.user.id,
                    })
                    this.addContribution(result.data)
                } else if (this.edit) {
                    const result = await post(`/contributions/contribution/${this.contribution.id}`, {
                        contribution: {
                            'title': this.title,
                            'description': this.description,
                        },
                        context: {
                            'code': this.code,
                            'label_en': this.contextLabelEn,
                            'label_fr': this.contextLabelFr,
                            'label_ar': this.contextLabelAr,
                            'proposition_en': this.propositionLabelEn,
                            'proposition_fr': this.propositionLabelFr,
                            'proposition_ar': this.propositionLabelAr,
                        },
                        patterns: this.patterns,
                        responses: this.responses,
                        relatedContexts: this.selectedContexts.map(context => context.code),
                    })
                    this.editContribution(result.data)
                }
                this.RESET_PATTERNS_STATE()
                this.RESET_RESPONSES_STATE()
                this.dialog = false
                this.$emit('close')
            }
        },
        // PATTERNS
        pushPattern: function () {
            if (this.$refs.patternForm.validate()) {
                this.addPattern({
                    'status': 'add',
                    'label': this.patternLabel,
                    'language': this.patternLanguage.value,
                })
                this.$refs.patternForm.reset()
                this.selectedPatterns = []
            }
        },
        updatePattern: function () {
            if (this.$refs.patternForm.validate()) {
                this.editPattern({
                    'status': this.selectedPatterns[0].id ? 'edit' : 'add',
                    'temporaryId': this.selectedPatterns[0].temporaryId,
                    'id': this.selectedPatterns[0].id,
                    'label': this.patternLabel,
                    'language': this.patternLanguage,
                })
                this.$refs.patternForm.reset()
                this.selectedPatterns = []
            }
        },
        removePattern: function () {
            if (this.selectedPatterns[0].id) {
                this.deletePattern({
                    'status': 'delete',
                    'id': this.selectedPatterns[0].id,
                    'label': this.patternLabel,
                    'language': this.patternLanguage,
                })
            } else {
                this.deletePattern({
                    'label': this.patternLabel,
                    'language': this.patternLanguage.value,
                })
            }
            this.selectedPatterns = []
            this.$refs.patternForm.reset()
        },
        // RESPONSES
        pushResponse: function () {
            if (this.$refs.responseForm.validate()) {
                this.addResponse({
                    'status': 'add',
                    'label': this.responseLabel,
                    'language': this.responseLanguage.value,
                })
                this.$refs.responseForm.reset()
            }
        },
        updateResponse: function () {
            if (this.$refs.responseForm.validate()) {
                this.editResponse({
                    'status': this.selectedResponses[0].id ? 'edit' : 'add',
                    'temporaryId': this.selectedResponses[0].temporaryId,
                    'id': this.selectedResponses[0].id,
                    'label': this.responseLabel,
                    'language': this.responseLanguage,
                })
                this.$refs.responseForm.reset()
                this.selectedResponses = []
            }
        },
        removeResponse: function () {
            const response = {
                'label': this.responseLabel,
                'language': this.responseLanguage,
            }
            if (this.selectedResponses[0].id) {
                this.deleteResponse({
                    'status': 'delete',
                    'id': this.selectedResponses[0].id,
                    ...response,
                })
            } else {
                this.deleteResponse(response)
            }
            this.selectedResponses = []
            this.$refs.responseForm.reset()
        },
        close: function () {
            this.dialog = false
            this.RESET_PATTERNS_STATE()
            this.RESET_RESPONSES_STATE()
            this.$emit('close')
        },
        showField: function (language) {
            return this.contributionLanguage.value === 'all' || this.contributionLanguage.value === language
        },
        onPatternSelect: function ({ value, item }) {
            if (value) {
                this.patternLabel = item.label
                this.patternLanguage = item.language
            } else {
                this.$refs.patternForm.reset()
            }
        },
        onResponseSelect: function ({ value, item }) {
            if (value) {
                this.responseLabel = item.label
                this.responseLanguage = item.language
            } else {
                this.$refs.responseForm.reset()
            }
        },
        ...mapActions('contributions', ['addContribution', 'editContribution']),
        ...mapActions('contexts', ['getContexts']),
        ...mapActions('patterns', ['setPatterns', 'addPattern', 'editPattern', 'deletePattern']),
        ...mapActions('responses', ['setResponses', 'addResponse', 'editResponse', 'deleteResponse']),
        ...mapMutations('contexts', ['RESET_CONTEXTS_STATE']),
        ...mapMutations('patterns', ['RESET_PATTERNS_STATE']),
        ...mapMutations('responses', ['RESET_RESPONSES_STATE']),
    },
}
</script>

<style scoped lang="sass">

.two-columns
    display: grid
    grid-template-columns: 1fr auto
    grid-gap: 10px

#pattern-form
    display: grid
    grid-template-columns: 1fr 1fr repeat(4, auto)
    grid-gap: 10px

#response-form
    display: grid
    grid-template-columns: 1fr 1fr repeat(4, auto)
    grid-gap: 10px

</style>
