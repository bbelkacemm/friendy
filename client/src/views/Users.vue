<template>
    <v-container fluid>
        <v-toolbar dense elevation="0">
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
                <v-btn plain :disabled="selectedUsers.length !== 1 || selectedUsers.length === 0"
                       v-on:click="removeUser">
                    <v-icon left>mdi-delete</v-icon>
                    {{ $t('delete') }}
                </v-btn>

                <!-- VALIDATE -->
                <confirmation v-if="selectedUsers[0] && selectedUsers[0].status === 'pending'"
                              v-on:accept="validateUser" v-on:cancel="selectedUsers = []" type="validate"
                              :header="$t('validateUserHeader')"
                              :description="$t('validateUserDescription')"/>
                <!-- INVALIDATE -->
                <confirmation v-if="selectedUsers[0] && selectedUsers[0].status === 'pending'"
                              v-on:accept="invalidateUser" v-on:cancel="selectedUsers = []" type="invalidate"
                              :header="$t('invalidateUserHeader')"
                              :description="$t('invalidateUserDescription')"/>
            </v-toolbar-items>
        </v-toolbar>

        <v-divider></v-divider>

        <v-data-table :headers="headers"
                      :items="users"
                      :items-per-page="14"
                      v-model="selectedUsers"
                      :search="search"
                      show-select
                      single-select
                      class="elevation-0">
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

            <template v-slot:item.role.label="{item}">
                {{ capitalizeFirst(item.role.label) }}
            </template>

            <template v-slot:item.status="{item}">
                <v-icon v-if="item.status === 'pending'">mdi-timer-sand</v-icon>
                <v-icon v-if="item.status === 'valid'" color="green">mdi-check</v-icon>
                <v-icon v-if="item.status === 'invalid'" color="error">mdi-close</v-icon>
            </template>
        </v-data-table>

        <v-snackbar v-model="errorSnackbar" class="d-print-none" color="error">
            <template v-slot:default>
                {{ $t(errorMessage) }}
            </template>
            <template v-slot:action>
                <v-btn icon dark @click="errorSnackbar = false">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </template>
        </v-snackbar>
    </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import UserForm from '@/components/UserForm'
import Confirmation from '@/components/Confirmation'
import { post } from '@/helpers/HTTPHelper'

export default {
    name: 'Users',
    components: { Confirmation, UserForm },
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
                {
                    text: this.$t('role').toUpperCase(),
                    value: 'role.label',
                },
                {
                    text: this.$t('status').toUpperCase(),
                    value: 'status',
                },
            ],
            selectedUsers: [],
            formKey: 0,
            search: null,
            errorSnackbar: false,
            errorMessage: null,
        }
    },
    computed: {
        ...mapGetters('users', ['users']),
    },
    methods: {
        removeUser: async function () {
            const result = await this.deleteUser(this.selectedUsers[0])
            if (!result.value) {
                this.errorSnackbar = true
                this.errorMessage = result.message
            }
            this.selectedUsers = []
        },
        validateUser: async function () {
            const result = await post(`/users/user/${this.selectedUsers[0].id}`, {
                'status': 'valid',
            })
            if (result.value) {
                this.editUser(result.data)
            }
            this.selectedUsers = []
        },
        invalidateUser: async function () {
            const result = await post(`/users/user/${this.selectedUsers[0].id}`, {
                'status': 'invalid',
            })
            if (result.value) {
                this.editUser(result.data)
            }
            this.selectedUsers = []
        },
        ...mapActions('users', ['editUser', 'deleteUser']),
    },
}
</script>

<style scoped>

</style>
