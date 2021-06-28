<template>
    <v-dialog v-model="dialog" overlay-opacity=".1" scrollable width="85%" persistent>
        <template v-slot:activator="{ on, attrs }">
            <v-btn plain v-bind="attrs" v-on="on">
                <v-icon left>mdi-file-document</v-icon>
                {{ $t('details') }}
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
                        <v-row>
                            <v-col>
                                <div class="font-weight-bold">{{ $t('code') }}</div>
                                <div>{{ context['code'] }}</div>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <div class="font-weight-bold">{{ $t('labelEn') }}</div>
                                <div>{{ context['labelEn'] }}</div>
                            </v-col>
                            <v-col>
                                <div class="font-weight-bold">{{ $t('labelFr') }}</div>
                                <div>{{ context['labelFr'] }}</div>
                            </v-col>
                            <v-col>
                                <div class="font-weight-bold">{{ $t('labelAr') }}</div>
                                <div>{{ context['labelAr'] }}</div>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <div class="font-weight-bold">{{ $t('propositionEn') }}</div>
                                <div>{{ context['propositionEn'] }}</div>
                            </v-col>
                            <v-col>
                                <div class="font-weight-bold">{{ $t('propositionFr') }}</div>
                                <div>{{ context['propositionFr'] }}</div>
                            </v-col>
                            <v-col>
                                <div class="font-weight-bold">{{ $t('propositionAr') }}</div>
                                <div>{{ context['propositionAr'] }}</div>
                            </v-col>
                        </v-row>
                    </v-container>
                    <v-tabs v-model="tab" dark background-color="primary">
                        <v-tab v-for="item in tabs" :key="item">
                            {{ item }}
                        </v-tab>
                    </v-tabs>
                    <v-tabs-items v-model="tab">
                        <v-tab-item v-for="dataItem in tabsData" :key="dataItem.key">
                            <v-data-table class="pa-2" :headers="dataItem.headers" :items="dataItem.list" dense></v-data-table>
                        </v-tab-item>
                    </v-tabs-items>
                </v-card-text>
            </v-card>
        </v-form>
    </v-dialog>
</template>

<script>
export default {
    name: 'Context',
    props: {
        context: Object,
    },
    data: function () {
        return {
            dialog: false,
            tab: 0,
        }
    },
    computed: {
        tabs: function () {
            return [this.$t('patterns'), this.$t('responses'), this.$t('relatedContexts')]
        },
        tabsData: function () {
            return [
                {
                    key: 0,
                    headers: [
                        {
                            text: this.$t('label').toUpperCase(),
                            value: 'label',
                        },
                        {
                            text: this.$t('language').toUpperCase(),
                            value: 'language',
                        },
                    ],
                    list: this.context.patterns,
                },
                {
                    key: 1,
                    headers: [
                        {
                            text: this.$t('label').toUpperCase(),
                            value: 'label',
                        },
                        {
                            text: this.$t('language').toUpperCase(),
                            value: 'language',
                        },
                    ],
                    list: this.context.responses,
                },
                {
                    key: 2,
                    headers: [
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
                    list: this.context.contexts,
                },
            ]
        },
    },
    methods: {
        close: function () {
            this.dialog = false
            this.$emit('close')
        },
    },
}
</script>

<style scoped>

</style>
