<template>
    <v-container fluid>
        <v-row>
            <v-col></v-col>
            <v-col cols="6">
                <v-form v-on:submit.prevent="" ref="form">
                    <v-card elevation="1"
                            outlined
                            shaped
                            tile>
                        <v-card-text>
                            <v-text-field v-model="username" class="mb-2" :rules="[validationRules.required]"
                                          :label="$t('username')" outlined dense
                                          hide-details="auto"></v-text-field>
                            <v-text-field v-model="password"
                                          :rules="[validationRules.required, validationRules.passwordLength]"
                                          :label="$t('password')" type="password"
                                          outlined dense
                                          hide-details="auto"></v-text-field>
                        </v-card-text>

                        <v-card-actions>
                            <v-btn block @click="login" color="primary" text tile elevation="0">
                                <span class="mr-2">{{ $t('login') }}</span>
                                <v-icon>mdi-login</v-icon>
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-form>
            </v-col>
            <v-col></v-col>
        </v-row>
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

export default {
    name: 'Login',
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
            if (this.$refs.form.validate()) {
                const result = await post('/login', {
                    'username': this.username,
                    'password': this.password,
                })
                if (result.value) {
                    this.setUser(result.data)
                    await this.$router.push({ name: 'home' })
                } else {
                    this.loginErrorSnackbar = true
                    this.snackbarContent = result.message
                }
            }
        },
        ...mapActions('authentication', ['setUser']),
    },
}
</script>

<style scoped>

</style>
