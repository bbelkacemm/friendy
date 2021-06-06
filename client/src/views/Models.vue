<template>
    <v-container fluid>
        <v-toolbar dense elevation="0" class="primary" dark>
            <v-toolbar-title></v-toolbar-title>
            <v-toolbar-items>
                <!-- UPDATE STATE-->
                <v-btn plain v-on:click="updateState" v-if="selectedModels[0]">
                    <v-icon left>mdi-pencil</v-icon>
                    {{ $t(selectedModels[0].state === 'enabled' ? 'disable' : 'enable') }}
                </v-btn>
                <v-btn plain disabled v-else>
                    <v-icon left>mdi-pencil</v-icon>
                    {{ $t('disable') }}/{{ $t('enable') }}
                </v-btn>

                <!-- UPDATE STATE-->
                <v-btn plain v-on:click="updateTag" v-if="selectedModels[0] && selectedModels[0].state === 'enabled'">
                    <v-icon left>mdi-pencil</v-icon>
                    {{ $t(selectedModels[0].tag === 'dev' ? 'setProd' : 'setDev') }}
                </v-btn>
                <v-btn plain disabled v-else>
                    <v-icon left>mdi-pencil</v-icon>
                    {{ $t('setDev') }}/{{ $t('setProd') }}
                </v-btn>

                <!-- DELETE -->
                <v-btn plain v-on:click="removeModel" :disabled="!selectedModels[0]">
                    <v-icon left>mdi-delete</v-icon>
                    {{ $t('delete') }}
                </v-btn>
            </v-toolbar-items>
        </v-toolbar>

        <v-data-table :headers="headers"
                      :items="models"
                      :items-per-page="14"
                      v-model="selectedModels"
                      show-select
                      class="elevation-1">
            <template v-slot:item.path="{item}">
                <v-icon>mdi-folder</v-icon>
                ./server/model/output/{{ item.path }}
            </template>
            <template v-slot:item.state="{item}">
                <template v-if="item.state === 'disabled'">
                    <v-chip color="error">{{ item.state.toUpperCase() }}</v-chip>
                </template>
                <template v-else>
                    <v-chip color="success">{{ item.state.toUpperCase() }}</v-chip>
                </template>
            </template>
            <template v-slot:item.tag="{item}">
                <template v-if="item.tag === 'dev'">
                    <v-chip color="primary">{{ item.tag.toUpperCase() }}</v-chip>
                </template>
                <template v-else-if="item.tag === 'prod'">
                    <v-chip color="success">{{ item.tag.toUpperCase() }}</v-chip>
                </template>
                <template v-else>
                    <v-chip color="secondary">{{ item.tag.toUpperCase() }}</v-chip>
                </template>
            </template>
            <template v-slot:item.user="{item}">
                {{ getFullName(item.user) }}
            </template>
            <template v-slot:item.createdAt="{item}">
                {{ formatDate(item['createdAt'], true).toUpperCase() }}
            </template>
        </v-data-table>
    </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
    name: 'Models',
    data: function () {
        return {
            headers: [
                {
                    text: this.$t('path').toUpperCase(),
                    value: 'path',
                },
                {
                    text: this.$t('state').toUpperCase(),
                    value: 'state',
                },
                {
                    text: this.$t('tag').toUpperCase(),
                    value: 'tag',
                },
                {
                    text: this.$t('creator').toUpperCase(),
                    value: 'user',
                },
                {
                    text: this.$t('createdAt').toUpperCase(),
                    value: 'createdAt',
                },
            ],
            selectedModels: [],
        }
    },
    computed: {
        ...mapGetters('models', ['models']),
    },
    methods: {
        updateState: async function () {
            await this.editModel({
                model: this.selectedModels[0],
                state: this.selectedModels[0].state === 'enabled' ? 'disabled' : 'enabled',
                tag: false,
            })
            this.selectedModels = []
        },
        updateTag: async function () {
            await this.editModel({
                model: this.selectedModels[0],
                state: false,
                tag: this.selectedModels[0].tag === 'dev' ? 'prod' : 'dev',
            })
            this.selectedModels = []
        },
        removeModel: async function () {
            await this.deleteModel(this.selectedModels[0])
            this.selectedModels = []
        },
        ...mapActions('models', ['editModel', 'deleteModel']),
    },
}
</script>

<style scoped>

</style>
