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
                <v-stepper v-model="currentStep" class="elevation-0">
                    <v-stepper-header class="elevation-0">
                        <template v-for="step in steps">
                            <v-stepper-step :key="`${step}-step`" :complete="currentStep > step" :step="step">
                                {{ titles[step - 1] }}
                            </v-stepper-step>

                            <v-divider v-if="step !== steps" :key="step"></v-divider>
                        </template>
                    </v-stepper-header>

                    <v-stepper-items>
                        <v-stepper-content class="pa-0" v-for="step in steps" :key="`${step}-content`" :step="step">
                            <v-container v-if="step === 1" fluid>
                                <v-form v-on:submit.prevent="" ref="contributionForm">
                                    <v-text-field class="mb-2" v-model="title" :rules="[validationRules.required]"
                                                  hide-details="auto" :label="$t('title').toUpperCase()" outlined
                                                  dense></v-text-field>
                                    <v-textarea class="mb-2" v-model="description" :label="$t('description').toUpperCase()"
                                                hide-details="auto" outlined dense></v-textarea>
                                </v-form>
                            </v-container>
                            <v-container v-if="step === 2" fluid>
                                <v-form v-on:submit.prevent="" ref="contextForm">
                                    <v-text-field class="mb-2" v-model="code" :rules="[validationRules.required]"
                                                  outlined
                                                  dense
                                                  hide-details="auto" :label="$t('code').toUpperCase()"></v-text-field>
                                    <div id="context-labels">
                                        <v-text-field class="mb-2" v-model="contextLabelEn"
                                                      :rules="[validationRules.required]"
                                                      outlined
                                                      dense
                                                      hide-details="auto" :label="$t('contextLabelEn').toUpperCase()"></v-text-field>
                                        <v-text-field class="mb-2" v-model="contextLabelFr"
                                                      :rules="[validationRules.required]"
                                                      outlined
                                                      dense
                                                      hide-details="auto" :label="$t('contextLabelFr').toUpperCase()"></v-text-field>
                                        <v-text-field class="mb-2" v-model="contextLabelAr"
                                                      :rules="[validationRules.required]"
                                                      outlined
                                                      dense
                                                      hide-details="auto" :label="$t('contextLabelAr').toUpperCase()"></v-text-field>
                                    </div>
                                    <v-text-field class="mb-2" v-model="propositionLabelEn"
                                                  :rules="[validationRules.required]"
                                                  outlined
                                                  dense
                                                  hide-details="auto" :label="$t('propositionLabelEn').toUpperCase()"></v-text-field>
                                    <v-text-field class="mb-2" v-model="propositionLabelFr"
                                                  :rules="[validationRules.required]"
                                                  outlined
                                                  dense
                                                  hide-details="auto" :label="$t('propositionLabelFr').toUpperCase()"></v-text-field>
                                    <v-text-field class="mb-2" v-model="propositionLabelAr"
                                                  :rules="[validationRules.required]"
                                                  outlined
                                                  dense
                                                  hide-details="auto" :label="$t('propositionLabelAr').toUpperCase()"></v-text-field>
                                </v-form>
                            </v-container>
                            <v-container v-if="step === 3" fluid>
                                <v-form v-on:submit.prevent="" ref="patternForm">
                                    <div id="pattern-form">
                                        <v-text-field class="mb-2" v-model="patternLabel"
                                                      :rules="[validationRules.required]"
                                                      outlined
                                                      dense hide-details="auto"
                                                      :label="$t('patternLabel').toUpperCase()"></v-text-field>
                                        <v-combobox class="mb-2" :label="$t('language').toUpperCase()" v-model="patternLanguage"
                                                    :rules="[validationRules.required]"
                                                    hide-details="auto" :items="languagesList" outlined
                                                    dense></v-combobox>
                                        <v-btn @click="pushPattern" icon tile color="primary">
                                            <v-icon>mdi-plus</v-icon>
                                        </v-btn>
                                    </div>
                                </v-form>
                                <v-data-table :headers="patternsHeaders" :items="patterns"
                                              :items-per-page="5"></v-data-table>
                            </v-container>
                            <v-container v-if="step === 4" fluid>
                                <v-form v-on:submit.prevent="" ref="responseForm">
                                    <div id="response-form">
                                        <v-text-field class="mb-2" v-model="responseLabel"
                                                      :rules="[validationRules.required]"
                                                      outlined
                                                      dense hide-details="auto"
                                                      :label="$t('responseLabel').toUpperCase()"></v-text-field>
                                        <v-combobox class="mb-2" :label="$t('language').toUpperCase()" v-model="responseLanguage"
                                                    :rules="[validationRules.required]"
                                                    hide-details="auto" :items="languagesList" outlined
                                                    dense></v-combobox>
                                        <v-btn @click="pushResponse" icon tile color="primary">
                                            <v-icon>mdi-plus</v-icon>
                                        </v-btn>
                                    </div>
                                </v-form>
                                <v-data-table :headers="responsesHeaders" :items="responses"
                                              :items-per-page="5"></v-data-table>
                            </v-container>
                            <v-container v-if="step === 5" fluid>
                                <v-data-table :headers="contextsHeaders" :items="contexts" v-model="selectedContexts"
                                              show-select :items-per-page="5"></v-data-table>
                            </v-container>
                            <v-divider></v-divider>
                            <v-card-actions fluid elevation="0" class="pa-0">
                                <v-btn v-if="currentStep > 1" plain @click="back(step)">
                                    <v-icon left>mdi-arrow-left-thick</v-icon>
                                    {{ $t('back') }}
                                </v-btn>
                                <v-spacer></v-spacer>
                                <v-btn v-if="currentStep < steps" text color="primary" @click="next(step)">
                                    {{ $t('continue') }}
                                    <v-icon right>mdi-arrow-right-thick</v-icon>
                                </v-btn>
                                <v-btn v-else @click="save" text color="primary">
                                    <v-icon left>mdi-content-save</v-icon>
                                    {{ $t('save') }}
                                </v-btn>
                            </v-card-actions>
                        </v-stepper-content>
                    </v-stepper-items>
                </v-stepper>
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

export default {
    name: 'ContributionForm',
    props: {
        add: Boolean,
        edit: Boolean,
    },
    created: function () {
        this.getContexts()
        this.RESET_PATTERNS_STATE()
        this.RESET_RESPONSES_STATE()
    },
    data: function () {
        return {
            dialog: false,
            currentStep: 1,
            steps: 5,
            titles: [
                this.capitalizeFirst(this.$t('contributionForm')),
                this.capitalizeFirst(this.$t('contextForm')),
                this.capitalizeFirst(this.$t('patternsForm')),
                this.capitalizeFirst(this.$t('responsesForm')),
                this.capitalizeFirst(this.$t('relatedContexts')),
            ],
            // CONTRIBUTION
            title: null,
            description: null,
            // CONTEXT
            code: null,
            contextLabelEn: null,
            contextLabelFr: null,
            contextLabelAr: null,
            propositionLabelEn: null,
            propositionLabelFr: null,
            propositionLabelAr: null,
            // PATTERNS
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
            // RESPONSES
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
            // RELATED CONTEXTS
            contextsHeaders: [
                {
                    text: this.$t('labelEn').toUpperCase(),
                    value: 'label_en',
                },
                {
                    text: this.$t('labelFr').toUpperCase(),
                    value: 'label_fr',
                },
                {
                    text: this.$t('labelAr').toUpperCase(),
                    value: 'label_ar',
                },
            ],
            selectedContexts: [],
            // ERRORS
            errorSnackbar: false,
            snackbarErrorMessage: null,
        }
    },
    computed: {
        ...mapGetters('contexts', ['contexts']),
        ...mapGetters('patterns', ['patterns']),
        ...mapGetters('responses', ['responses']),
    },
    methods: {
        back: function (step) {
            this.currentStep = step - 1
        },
        next: function (step) {
            let patternsSet = null
            let responsesSet = null
            let error = false
            switch (this.currentStep) {
                case 1:
                    break
                case 2:
                    if (!this.$refs.contextForm[0].validate()) return
                    break
                case 3:
                    if (this.patterns.length === 0) {
                        this.snackbarErrorMessage = this.$t('patternsRequired')
                        this.errorSnackbar = true
                        return
                    }
                    break
                case 4:
                    if (this.responses.length === 0) {
                        this.snackbarErrorMessage = this.$t('responsesRequired')
                        this.errorSnackbar = true
                        return
                    }
                    patternsSet = new Set(this.patterns.map(p => p.language))
                    responsesSet = new Set(this.responses.map(r => r.language))
                    if (patternsSet.size !== responsesSet.size) {
                        error = true
                    }
                    if (!error) {
                        for (let item of patternsSet) {
                            if (!responsesSet.has(item)) {
                                error = true
                                break
                            }
                        }
                    }

                    if (error) {
                        this.snackbarErrorMessage = this.$t('patternsResponsesLanguageMatch')
                        this.errorSnackbar = true
                        return
                    }
                    break
            }
            this.currentStep = step + 1
        },
        save: async function () {
            const contribution = await post('/contributions/contribution', {
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
            this.addContribution(contribution)
            this.RESET_PATTERNS_STATE()
            this.RESET_RESPONSES_STATE()
            this.dialog = false
            this.$emit('close')
        },
        // PATTERNS
        pushPattern: function () {
            if (this.$refs.patternForm[0].validate()) {
                this.addPattern({
                    label: this.patternLabel,
                    language: this.patternLanguage.value,
                })
                this.$refs.patternForm[0].reset()
            }
        },
        pushResponse: function () {
            if (this.$refs.responseForm[0].validate()) {
                this.addResponse({
                    label: this.responseLabel,
                    language: this.responseLanguage.value,
                })
                this.$refs.responseForm[0].reset()
            }
        },
        close: function () {
            this.dialog = false
            this.RESET_PATTERNS_STATE()
            this.RESET_RESPONSES_STATE()
            this.$emit('close')
        },
        ...mapActions('contributions', ['addContribution']),
        ...mapActions('contexts', ['getContexts']),
        ...mapActions('patterns', ['setPatterns', 'addPattern']),
        ...mapActions('responses', ['setResponses', 'addResponse']),
        ...mapMutations('contexts', ['RESET_CONTEXTS_STATE']),
        ...mapMutations('patterns', ['RESET_PATTERNS_STATE']),
        ...mapMutations('responses', ['RESET_RESPONSES_STATE']),
    },
}
</script>

<style scoped lang="sass">

#context-labels
    display: grid
    grid-template-columns: 1fr 1fr 1fr
    grid-gap: 10px

#pattern-form
    display: grid
    grid-template-columns: 1fr 1fr auto
    grid-gap: 10px

#response-form
    display: grid
    grid-template-columns: 1fr 1fr auto
    grid-gap: 10px

</style>
