<template>
    <v-container fluid class="two-equal-columns full-height center-items">
        <v-card tile elevation="0" width="70%">
            <v-form v-on:submit.prevent="" ref="loginForm">
                <v-card-text class="pa-0">
                    <div class="input-grid mb-2">
                        <v-text-field v-model="username" :rules="[validationRules.required]"
                                      :label="capitalizeFirst($t('username'))" dense solo flat
                                      background-color="transparent"
                                      prepend-inner-icon="mdi-account"
                                      hide-details="auto"></v-text-field>
                    </div>
                    <div class="input-grid">
                        <v-text-field v-model="password"
                                      :rules="[validationRules.required, validationRules.passwordLength]"
                                      :label="capitalizeFirst($t('password'))" type="password"
                                      prepend-inner-icon="mdi-lock"
                                      dense solo flat background-color="transparent"
                                      hide-details="auto"></v-text-field>
                    </div>
                </v-card-text>
                <v-card-actions class="pa-0 mt-4">
                    <v-btn @click="signup" color="secondary" class="rounded-pill" plain text>
                        {{ $t('signup') }}
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn v-on:click="login" class="primary rounded-pill" text tile elevation="0">
                        <v-icon left>mdi-login</v-icon>
                        {{ $t('login') }}
                    </v-btn>
                </v-card-actions>
            </v-form>
        </v-card>
        <bot-welcome width="450"/>
        <v-snackbar v-model="loginErrorSnackbar" class="d-print-none" color="error">
            <template v-slot:default>
                {{ $t(snackbarContent) }}
            </template>
            <template v-slot:action>
                <v-btn icon dark @click="loginErrorSnackbar = false">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </template>
        </v-snackbar>
    </v-container>
</template>

<script>
import { post } from '@/helpers/HTTPHelper'
import { mapActions } from 'vuex'
import BotWelcome from '@/assets/bot-welcome.svg'

export default {
    name: 'Login',
    components: { BotWelcome },
    data: function () {
        return {
            username: null,
            password: null,
            loginErrorSnackbar: false,
            snackbarContent: null,
        }
    },
    methods: {
        login: async function () {
            if (this.$refs.loginForm.validate()) {
                const result = await post('/login', {
                    'username': this.username,
                    'password': this.password,
                })
                if (result.value) {
                    this.setUser(result.data)
                    if (['guest', 'client', 'contributor'].includes(this.user.role.label)) {
                        await this.$router.push({ name: 'home' })
                    } else {
                        await this.$router.push({ name: 'dashboard' })
                    }
                } else {
                    this.loginErrorSnackbar = true
                    this.snackbarContent = result.message
                }
            }
        },
        signup: function () {
            this.$router.push({ name: 'signup', query: { contributor: false } })
        },
        ...mapActions('authentication', ['setUser']),
    },
}
</script>

<style scoped>

</style>
