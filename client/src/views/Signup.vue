<template>
    <v-container fluid>
        <v-form v-on:submit.prevent="" ref="form">
            <v-row>
                <v-col></v-col>
                <v-col cols="6">
                    <v-card tile elevation="1">
                        <v-card-text>
                            <v-text-field v-model="firstName" :rules="[validationRules.required]" outlined dense
                                          :label="$t('firstName')"></v-text-field>
                            <v-text-field v-model="lastName" :rules="[validationRules.required]" outlined dense
                                          :label="$t('lastName')"></v-text-field>
                            <v-text-field v-model="username" :rules="[validationRules.required]" outlined dense
                                          :label="$t('username')"></v-text-field>
                            <v-text-field v-model="password" :rules="[validationRules.required, validationRules.passwordLength]" outlined
                                          dense
                                          :label="$t('password')"
                                          type="password"></v-text-field>
                            <v-text-field v-model="confirmPassword" outlined dense
                                          :rules="[validationRules.required, validationRules.passwordLength, validationRules.passwordMatch(password, confirmPassword)]"
                                          :label="$t('confirmPassword')"
                                          type="password"></v-text-field>
                            <v-text-field :label="$t('birthdate')" v-model="birthdate" :rules="[validationRules.required]"
                                          outlined dense
                                          type="date"></v-text-field>
                            <v-combobox :label="$t('gender')" v-model="gender" :rules="[validationRules.required]"
                                        :items="genderList" outlined
                                        dense></v-combobox>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn @click="clear" text large>
                                {{ $t('clear') }}
                            </v-btn>
                            <v-spacer></v-spacer>
                            <v-btn @click="signup" tile class="primary" large>
                                {{ $t('signup') }}
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
                <v-col></v-col>
            </v-row>
        </v-form>

        <v-snackbar v-model="signupErrorSnackbar" class="d-print-none" color="error">
            <template v-slot:default>
                {{ $t(snackbarContent) }}
            </template>
            <template v-slot:action>
                <v-btn icon dark @click="signupErrorSnackbar = false">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </template>
        </v-snackbar>
    </v-container>
</template>

<script>
import { post } from '@/helpers/HTTPHelper'

export default {
    name: 'Signup',
    data: function () {
        return {
            firstName: null,
            lastName: null,
            username: null,
            password: null,
            confirmPassword: null,
            birthdate: null,
            gender: null,
            signupErrorSnackbar: false,
            snackbarContent: null,
        }
    },
    methods: {
        clear: function () {
            this.$refs.form.reset()
            this.birthdate = null
        },
        signup: async function () {
            if (this.$refs.form.validate()) {
                const response = await post('/signup', {
                    'first_name': this.firstName,
                    'last_name': this.lastName,
                    'username': this.username,
                    'password': this.password,
                    'birth_date': this.birthdate,
                    'gender': this.gender === 'male' ? 'm' : 'f',
                })
                if (response === true) {
                    await this.$router.push({ name: 'login' })
                } else {
                    this.signupErrorSnackbar = true
                    this.snackbarContent = response
                }
            }
        },
    },
}
</script>

<style scoped>

</style>
