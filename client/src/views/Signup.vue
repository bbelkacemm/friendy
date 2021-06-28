<template>
    <v-container fluid class="center-items full-height two-equal-columns">
        <therapy v-if="$route.query.contributor" width="512"/>
        <children v-else width="512"/>
        <v-card tile elevation="0" width="80%" flat>
            <v-form v-on:submit.prevent="" ref="form">
                <v-card-text class="pa-0">
                    <div class="input-grid mb-2">
                        <v-text-field v-model="firstName" :rules="[validationRules.required]" dense solo flat
                                      background-color="transparent"
                                      :label="capitalizeFirst($t('firstName'))"
                                      :hint="capitalizeFirst($t('firstName'))"
                                      hide-details="auto"></v-text-field>
                    </div>
                    <div class="input-grid mb-2">
                        <v-text-field v-model="lastName" :rules="[validationRules.required]" dense solo flat
                                      background-color="transparent"
                                      :label="capitalizeFirst($t('lastName'))"
                                      :hint="capitalizeFirst($t('lastName'))"
                                      hide-details="auto"></v-text-field>
                    </div>
                    <div class="input-grid mb-2">
                        <v-text-field v-model="username" :rules="[validationRules.required]" dense solo flat
                                      background-color="transparent"
                                      :label="capitalizeFirst($t('username'))"
                                      :hint="capitalizeFirst($t('username'))"
                                      hide-details="auto"></v-text-field>
                    </div>
                    <div class="input-grid mb-2">
                        <v-text-field v-model="password"
                                      :rules="[validationRules.required, validationRules.passwordLength]" dense
                                      solo flat background-color="transparent"
                                      :label="capitalizeFirst($t('password'))"
                                      :hint="capitalizeFirst($t('password'))" hide-details="auto"
                                      type="password"></v-text-field>
                    </div>
                    <div class="input-grid mb-2">
                        <v-text-field v-model="confirmPassword" dense solo flat background-color="transparent"
                                      :rules="[validationRules.required, validationRules.passwordLength, validationRules.passwordMatch(password, confirmPassword)]"
                                      :label="capitalizeFirst($t('confirmPassword'))"
                                      :hint="capitalizeFirst($t('confirmPassword'))" hide-details="auto"
                                      type="password"></v-text-field>
                    </div>
                    <div class="input-grid mb-2">
                        <v-text-field :label="capitalizeFirst($t('birthdate'))" v-model="birthdate"
                                      :hint="capitalizeFirst($t('birthdate'))"
                                      :rules="[validationRules.required]"
                                      hide-details="auto"
                                      dense solo flat background-color="transparent"
                                      type="date"></v-text-field>
                    </div>
                    <div class="input-grid">
                        <v-combobox :label="capitalizeFirst($t('gender'))" :hint="capitalizeFirst($t('gender'))"
                                    v-model="gender" :rules="[validationRules.required]"
                                    :items="genderList" dense solo flat background-color="transparent"
                                    hide-details="auto"></v-combobox>
                    </div>
                </v-card-text>
                <v-card-actions class="pa-0 mt-4">
                    <v-btn @click="clear" text plain class="rounded-pill">
                        {{ $t('clear') }}
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn @click="signup" tile plain class="primary rounded-pill">
                        {{ $t('signup') }}
                    </v-btn>
                </v-card-actions>
            </v-form>
        </v-card>

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
import Therapy from '@/assets/therapy.svg'
import Children from '@/assets/children.svg'

export default {
    name: 'Signup',
    components: { Therapy, Children },
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
                let result
                if (this.$route.query.contributor) {
                    result = await post('/signup', {
                        'first_name': this.firstName,
                        'last_name': this.lastName,
                        'username': this.username,
                        'password': this.password,
                        'birth_date': this.birthdate,
                        'gender': this.gender === 'male' ? 'm' : 'f',
                        'status': 'pending',
                    })
                } else {
                    result = await post('/signup', {
                        'first_name': this.firstName,
                        'last_name': this.lastName,
                        'username': this.username,
                        'password': this.password,
                        'birth_date': this.birthdate,
                        'gender': this.gender === 'male' ? 'm' : 'f',
                    })
                }
                if (result.value) {
                    await this.$router.push({ name: 'login' })
                } else {
                    this.signupErrorSnackbar = true
                    this.snackbarContent = result.message
                }
            }
        },
    },
}
</script>

<style scoped>

</style>
