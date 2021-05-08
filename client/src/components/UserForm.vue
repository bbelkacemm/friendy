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
                <v-card-text>
                    <v-container fluid class="pa-0">
                        <v-text-field class="mb-2" v-model="firstName" :rules="[validationRules.required]" outlined dense
                                      hide-details="auto"
                                      :label="$t('firstName')"></v-text-field>
                        <v-text-field class="mb-2" v-model="lastName" :rules="[validationRules.required]" outlined dense
                                      hide-details="auto"
                                      :label="$t('lastName')"></v-text-field>
                        <v-text-field class="mb-2" v-model="username" :rules="[validationRules.required]" :disabled="user"
                                      outlined dense
                                      hide-details="auto"
                                      :label="$t('username')"></v-text-field>
                        <v-text-field v-if="!data" class="mb-2" v-model="password"
                                      :rules="[validationRules.required, validationRules.passwordLength]"
                                      outlined hide-details="auto"
                                      dense
                                      :label="$t('password')"
                                      type="password"></v-text-field>
                        <v-text-field v-if="!data" class="mb-2" v-model="confirmPassword" outlined dense
                                      hide-details="auto"
                                      :rules="[validationRules.required, validationRules.passwordLength, validationRules.passwordMatch(password, confirmPassword)]"
                                      :label="$t('confirmPassword')"
                                      type="password"></v-text-field>
                        <v-text-field class="mb-2" :label="$t('birthdate')" v-model="birthdate"
                                      :rules="[validationRules.required]" hide-details="auto"
                                      outlined dense
                                      type="date"></v-text-field>
                        <v-autocomplete class="mb-2" :label="$t('gender')" v-model="gender" :rules="[validationRules.required]"
                                        hide-details="auto" :items="genderList" outlined dense></v-autocomplete>
                        <v-autocomplete class="mb-2" :label="$t('role')" v-model="role" :rules="[validationRules.required]"
                                        hide-details="auto" :items="rolesAutocomplete" outlined dense></v-autocomplete>
                    </v-container>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions class="pa-0">
                    <v-btn @click="clear" text small>
                        {{ $t('clear') }}
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn @click="save" tile class="primary" small>
                        {{ $t('save') }}
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-form>
    </v-dialog>
</template>

<script>
import { post } from '@/helpers/HTTPHelper'
import { mapActions, mapGetters } from 'vuex'

export default {
    name: 'UserForm',
    props: {
        add: Boolean,
        edit: Boolean,
        data: Object,
    },
    created: function () {
        if (this.data) {
            this.username = this.data.username
            this.firstName = this.data.firstName
            this.lastName = this.data.lastName
            this.gender = this.data.gender
            this.birthdate = this.formatDateForDatePicker(this.data.birthdate)
            this.role = this.data.roleId
        }
    },
    data: function () {
        return {
            dialog: false,
            username: null,
            password: null,
            confirmPassword: null,
            firstName: null,
            lastName: null,
            gender: null,
            birthdate: null,
            role: null,
        }
    },
    computed: {
        ...mapGetters('roles', ['rolesAutocomplete']),
    },
    methods: {
        clear: function () {
            this.birthdate = null
            this.$refs.form.clear()
        },
        save: async function () {
            if (this.$refs.form.validate()) {
                if (this.add) {
                    const user = await post('/users', {
                        'first_name': this.firstName,
                        'last_name': this.lastName,
                        'username': this.username,
                        'password': this.password,
                        'birth_date': this.birthdate,
                        'gender': this.gender,
                        'role_id': this.role,
                    })
                    if (user) {
                        this.addUser(user)
                        this.dialog = false
                        this.$emit('close')
                    }
                } else if (this.edit) {
                    const user = await post(`/users/user/${this.data.id}`, {
                        'first_name': this.firstName,
                        'last_name': this.lastName,
                        'username': this.username,
                        'password': this.password,
                        'birth_date': this.birthdate,
                        'gender': this.gender,
                        'role_id': this.role,
                    })
                    if (user) {
                        this.editUser(user)
                        this.dialog = false
                        this.$emit('close')
                    }
                }
            }
        },
        close: function () {
            this.dialog = false
            this.$emit('close')
        },
        ...mapActions('users', ['addUser', 'editUser']),
    },
}
</script>

<style scoped>

</style>
