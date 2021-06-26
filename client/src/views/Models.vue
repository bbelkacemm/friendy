<template>
    <v-container fluid>
        <v-toolbar dense elevation="0">
            <v-toolbar-items>
                <!-- UPDATE STATE-->
                <confirmation v-if="selectedModels[0]"
                              :type="selectedModels[0].state === 'enabled' ? 'disable' : 'enable'"
                              v-on:accept="updateState" :header="$t('enableModelHeader')"
                              :description="$t('enableModelDescription')"/>
                <v-btn plain disabled v-else>
                    <v-icon left>mdi-pencil</v-icon>
                    {{ $t('disable') }}/{{ $t('enable') }}
                </v-btn>

                <!-- UPDATE TAG-->
                <confirmation v-if="selectedModels[0] && selectedModels[0].state === 'enabled'"
                              :type="selectedModels[0].tag === 'dev' ? 'setProd' : 'setDev'"
                              v-on:accept="updateTag" :header="$t('setModelTagHeader')"
                              :description="$t('setModelTagDescription')"/>
                <v-btn plain disabled v-else>
                    <v-icon left>mdi-pencil</v-icon>
                    {{ $t('setDev') }}/{{ $t('setProd') }}
                </v-btn>

                <!-- DELETE -->
                <confirmation v-if="selectedModels[0]"
                              type="delete"
                              v-on:accept="removeModel" :header="$t('deleteHeader')"
                              :description="$t('deleteDescription')"/>
                <v-btn v-else plain disabled>
                    <v-icon left>mdi-delete</v-icon>
                    {{ $t('delete') }}
                </v-btn>
            </v-toolbar-items>
        </v-toolbar>

        <v-divider></v-divider>

        <v-data-table :headers="headers"
                      :items="models"
                      :items-per-page="14"
                      v-model="selectedModels"
                      sort-by="path"
                      item-key="path"
                      show-select
                      single-select>
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
import Confirmation from '@/components/Confirmation'

export default {
    name: 'Models',
    components: { Confirmation },
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
            await this.setModels()
            this.selectedModels = []
        },
        updateTag: async function () {
            await this.editModel({
                model: this.selectedModels[0],
                state: false,
                tag: this.selectedModels[0].tag === 'dev' ? 'prod' : 'dev',
            })
            await this.setModels()
            this.selectedModels = []
        },
        removeModel: async function () {
            await this.deleteModel(this.selectedModels[0])
            this.selectedModels = []
        },
        ...mapActions('models', ['setModels', 'editModel', 'deleteModel']),
    },
}
</script>

<style scoped>

</style>
