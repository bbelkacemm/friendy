<template>
    <v-container fluid>
        <v-toolbar dense elevation="0" class="black" dark>
            <v-toolbar-title></v-toolbar-title>
            <v-toolbar-items>
                <role-form add v-on:close="`${formKey++}-add`" :key="formKey"/>

                <role-form v-if="selectedRoles.length === 1" edit :data="selectedRoles[0]" v-on:close="`${formKey++}-edit`" :key="formKey"/>
                <v-btn v-else plain disabled>
                    <v-icon left>mdi-pencil</v-icon>
                    {{ $t('edit') }}
                </v-btn>

                <v-btn plain>
                    <v-icon left>mdi-delete</v-icon>
                    {{ $t('delete') }}
                </v-btn>
            </v-toolbar-items>
        </v-toolbar>

        <v-data-table :headers="headers"
                      :items="roles"
                      :items-per-page="5"
                      v-model="selectedRoles"
                      show-select
                      class="elevation-1"></v-data-table>
    </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import RoleForm from '@/components/RoleForm'

export default {
    name: 'Roles',
    components: { RoleForm },
    data: function () {
        return {
            headers: [
                {
                    text: this.$t('label'),
                    value: 'label',
                },
            ],
            selectedRoles: [],
            formKey: 0,
        }
    },
    computed: {
        ...mapGetters('roles', ['roles']),
    },
}
</script>

<style scoped>

</style>
