<template>
    <v-container fluid>
        <v-toolbar dense elevation="0" class="primary" dark>
            <v-toolbar-title></v-toolbar-title>
            <v-toolbar-items>
                <!-- ADD -->
                <user-form add v-on:close="formKey++" :key="`${formKey}-add-user`"/>

                <!-- EDIT --->
                <user-form v-if="selectedUsers[0] && selectedUsers.length === 1" edit :data="selectedUsers[0]"
                           v-on:close="formKey++" :key="`${formKey}-edit-user`"/>
                <v-btn v-else plain disabled>
                    <v-icon left>mdi-pencil</v-icon>
                    {{ $t('edit') }}
                </v-btn>

                <!-- DELETE -->
                <v-btn plain :disabled="selectedUsers.length !== 1">
                    <v-icon left>mdi-delete</v-icon>
                    {{ $t('delete') }}
                </v-btn>
            </v-toolbar-items>
        </v-toolbar>

        <v-data-table :headers="headers"
                      :items="users"
                      :items-per-page="14"
                      v-model="selectedUsers"
                      :search="search"
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

            <template v-slot:item.gender="{item}">
                <div v-if="item.gender === 'f'">
                    <v-icon left>mdi-gender-female</v-icon>
                    {{ capitalizeFirst($t('f').toUpperCase()) }}
                </div>
                <div v-if="item.gender === 'm'">
                    <v-icon left>mdi-gender-male</v-icon>
                    {{ capitalizeFirst($t('m').toUpperCase()) }}
                </div>
            </template>

            <template v-slot:item.birthdate="{item}">
                <div v-if="item.birthdate">
                    {{ formatDate(item.birthdate).toUpperCase() }}
                </div>
                <v-icon v-else>mdi-minus</v-icon>
            </template>

        </v-data-table>
    </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import UserForm from '@/components/UserForm'

export default {
    name: 'Users',
    components: { UserForm },
    data: function () {
        return {
            headers: [
                {
                    text: this.$t('username').toUpperCase(),
                    value: 'username',
                },
                {
                    text: this.$t('firstName').toUpperCase(),
                    value: 'firstName',
                },
                {
                    text: this.$t('lastName').toUpperCase(),
                    value: 'lastName',
                },
                {
                    text: this.$t('birthdate').toUpperCase(),
                    value: 'birthdate',
                },
                {
                    text: this.$t('gender').toUpperCase(),
                    value: 'gender',
                },
            ],
            selectedUsers: [],
            formKey: 0,
            search: null,
        }
    },
    computed: {
        ...mapGetters('users', ['users']),
    },
}
</script>

<style scoped>

</style>
