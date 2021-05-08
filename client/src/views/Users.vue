<template>
    <v-container fluid>
        <v-toolbar dense elevation="0" class="black" dark>
            <v-toolbar-title></v-toolbar-title>
            <v-toolbar-items>
                <!-- ADD -->
                <user-form add v-on:close="`${this.addUserFormKey++}-add-user`" :key="addUserFormKey"/>

                <!-- EDIT --->
                <user-form v-if="selectedUsers[0]" edit :data="selectedUsers[0]"
                           v-on:close="`${this.editUserFormKey++}-add-user`" :key="editUserFormKey"/>
                <v-btn v-else plain disabled>
                    <v-icon left>mdi-pencil</v-icon>
                    {{ $t('edit') }}
                </v-btn>

                <!-- DELETE -->
                <v-btn plain>
                    <v-icon left>mdi-delete</v-icon>
                    {{ $t('delete') }}
                </v-btn>
            </v-toolbar-items>
        </v-toolbar>

        <v-data-table :headers="headers"
                      :items="users"
                      :items-per-page="5"
                      v-model="selectedUsers"
                      show-select
                      class="elevation-1">

            <template v-slot:item.gender="{item}">
                <div v-if="item.gender === 'f'">
                    <v-icon left>mdi-gender-female</v-icon>
                    {{ $t('f').toUpperCase() }}
                </div>
                <div v-if="item.gender === 'm'">
                    <v-icon left>mdi-gender-male</v-icon>
                    {{ $t('m').toUpperCase() }}
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
                    text: this.$t('username'),
                    value: 'username',
                },
                {
                    text: this.$t('firstName'),
                    value: 'firstName',
                },
                {
                    text: this.$t('lastName'),
                    value: 'lastName',
                },
                {
                    text: this.$t('birthdate'),
                    value: 'birthdate',
                },
                {
                    text: this.$t('gender'),
                    value: 'gender',
                },
            ],
            selectedUsers: [],
            addUserFormKey: 0,
            editUserFormKey: 0,
        }
    },
    computed: {
        ...mapGetters('users', ['users']),
    },
}
</script>

<style scoped>

</style>
