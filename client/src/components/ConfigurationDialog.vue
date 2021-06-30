<template>
    <v-dialog v-model="dialog" overlay-opacity=".1" scrollable width="50%" persistent>
        <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on">
                <v-icon>mdi-cog</v-icon>
            </v-btn>
        </template>
        <v-card>
            <v-card-title class="pa-0">
                <v-spacer></v-spacer>
                <v-btn icon tile @click="close">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-0">
                <div id="configuration-container">
                    <v-navigation-drawer permanent>
                        <v-list dense nav>
                            <v-list-item v-for="(item, index) in items" :key="item.title" link
                                         v-model="item.active" v-on:click="onSelect(index, item.value)">
                                <v-list-item-icon>
                                    <v-icon>{{ item.icon }}</v-icon>
                                </v-list-item-icon>

                                <v-list-item-content>
                                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                                </v-list-item-content>
                            </v-list-item>
                        </v-list>
                    </v-navigation-drawer>
                    <v-container v-if="selected === 'general'" fluid>
                        <v-menu offset-y rounded="xl">
                            <template v-slot:activator="{ attrs, on }">
                                <v-btn block text color="secondary" class="rounded-pill" v-bind="attrs" v-on="on">
                                    <v-icon left>mdi-translate</v-icon>
                                    {{ $t('language') }}
                                </v-btn>
                            </template>

                            <v-list>
                                <v-list-item v-for="item in languagesList" :key="item.value" link
                                             v-on:click="setLanguage(item.value)">
                                    <v-list-item-title v-text="capitalizeFirst(item.text)"></v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-menu>
                    </v-container>
                    <div v-else>
                        <v-container>
                            <v-form v-on:submit.prevent="" ref="profileForm">
                                <div class="input-grid mb-2">
                                    <v-text-field v-model="username" :rules="[validationRules.required]" dense solo flat
                                                  background-color="transparent" disabled
                                                  :label="capitalizeFirst($t('username'))"
                                                  :hint="capitalizeFirst($t('username'))" persistent-hint
                                                  hide-details="auto"></v-text-field>
                                </div>
                                <div class="input-grid mb-2">
                                    <v-text-field v-model="firstName" :rules="[validationRules.required]" dense solo
                                                  flat
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
                                    <v-text-field :label="capitalizeFirst($t('birthdate'))" v-model="birthdate"
                                                  :hint="capitalizeFirst($t('birthdate'))"
                                                  :rules="[validationRules.required]"
                                                  hide-details="auto"
                                                  dense solo flat background-color="transparent"
                                                  type="date"></v-text-field>
                                </div>
                                <div class="input-grid">
                                    <v-autocomplete :label="capitalizeFirst($t('gender'))"
                                                :hint="capitalizeFirst($t('gender'))"
                                                v-model="gender" :rules="[validationRules.required]"
                                                :items="genderList" dense solo flat background-color="transparent"
                                                hide-details="auto"></v-autocomplete>
                                </div>
                            </v-form>
                        </v-container>
                        <v-container class="justify-end">
                            <v-btn block text class="primary rounded-pill" v-on:click="save">
                                <v-icon left>mdi-content-save</v-icon>
                                {{ $t('save') }}
                            </v-btn>
                        </v-container>
                    </div>
                </div>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions class="pa-0">

            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { post } from '@/helpers/HTTPHelper'
import { mapActions } from 'vuex'

export default {
    name: 'ConfigurationDialog',
    created: function () {
        this.firstName = this.user.firstName
        this.lastName = this.user.lastName
        this.username = this.user.username
        this.birthdate = this.formatDateForDatePicker(this.user.birthdate)
        this.gender = this.user.gender
    },
    data: function () {
        return {
            dialog: false,
            // GENERAL
            items: [
                {
                    title: this.$t('general'),
                    value: 'general',
                    active: true,
                    icon: 'mdi-tune',
                },
                {
                    title: this.$t('profile'),
                    value: 'profile',
                    active: false,
                    icon: 'mdi-account',
                },
            ],
            selected: 'general',
            // PROFILE
            firstName: null,
            lastName: null,
            username: null,
            birthdate: null,
            gender: null,
        }
    },
    methods: {
        setLanguage: function (language) {
            this.$i18n.locale = language
            this.SET_LANGUAGE(language)
        },
        onSelect: function (index, value) {
            this.selected = value
            this.items.forEach(item => item.active = false)
            this.items[index].active = value === this.selected
        },
        close: function () {
            this.dialog = false
        },
        save: async function () {
            if (this.$refs.profileForm.validate()) {
                const result = await post(`/users/user/profile/${this.user.id}`, {
                    'first_name': this.firstName,
                    'last_name': this.lastName,
                    'birth_date': this.birthdate,
                    'gender': this.gender,
                })
                if (result.value) {
                    this.setUser(result.data)
                    this.close()
                }
            }
        },
        ...mapActions('authentication', ['setUser']),
    },
}
</script>

<style scoped lang="sass">

#configuration-container
    display: grid
    grid-template-columns: auto 1fr

</style>
