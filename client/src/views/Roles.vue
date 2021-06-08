<template>
    <v-container fluid>
        <v-toolbar dense elevation="0" class="primary" dark>
            <v-toolbar-title></v-toolbar-title>
            <v-toolbar-items>
                <role-form add v-on:close="formKey++" :key="`${formKey}-add`"/>

                <role-form v-if="selectedRoles.length === 1 && selectedRoles.length === 1" edit :data="selectedRoles[0]"
                           v-on:close="`${formKey++}-edit`" :key="formKey"/>
                <v-btn v-else plain disabled>
                    <v-icon left>mdi-pencil</v-icon>
                    {{ $t('edit') }}
                </v-btn>

                <v-btn plain :disabled="selectedRoles.length !== 1 || selectedRoles.length === 0"
                       v-on:click="removeRole">
                    <v-icon left>mdi-delete</v-icon>
                    {{ $t('delete') }}
                </v-btn>
            </v-toolbar-items>
        </v-toolbar>

        <v-data-table :headers="headers"
                      :items="roles"
                      :items-per-page="14"
                      :search="search"
                      v-model="selectedRoles"
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
        </v-data-table>
    </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import RoleForm from '@/components/RoleForm'

export default {
    name: 'Roles',
    components: { RoleForm },
    data: function () {
        return {
            headers: [
                {
                    text: this.$t('label').toUpperCase(),
                    value: 'label',
                },
            ],
            selectedRoles: [],
            formKey: 0,
            search: null,
        }
    },
    computed: {
        ...mapGetters('roles', ['roles']),
    },
    methods: {
        removeRole: function () {
            this.deleteRole(this.selectedRoles[0])
            this.selectedRoles = []
        },
        ...mapActions('roles', ['deleteRole']),
    },
}
</script>

<style scoped>

</style>
