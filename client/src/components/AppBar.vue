<template>
    <v-app-bar app elevation="0" color="white" v-if="user">
        <v-app-bar-nav-icon v-if="hasPrivilegesOf('contributor')" @click="$emit('clicked')"></v-app-bar-nav-icon>

        <v-spacer></v-spacer>
        <div>
            <v-menu v-model="menu"
                    :close-on-content-click="false"
                    :nudge-width="200"
                    offset-y>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn plain v-bind="attrs" v-on="on">
                        <div class="me-4">{{ getFullName(user) }}</div>
                        <v-avatar color="#F5F5F5" size="32"></v-avatar>
                    </v-btn>
                </template>

                <v-card>
                    <v-list>
                        <v-list-item>
                            <v-list-item-avatar>
                                <v-avatar color="#F5F5F5" size="32"></v-avatar>
                            </v-list-item-avatar>

                            <v-list-item-content>
                                <v-list-item-title>{{ getFullName(user) }}</v-list-item-title>
                                <v-list-item-subtitle>{{ $t(user.role.label) }}</v-list-item-subtitle>
                            </v-list-item-content>

                            <v-list-item-action>
                                <configuration-dialog/>
                            </v-list-item-action>
                            <v-list-item-action>
                                <v-btn icon @click="logout">
                                    <v-icon>mdi-logout</v-icon>
                                </v-btn>
                            </v-list-item-action>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-menu>
        </div>
    </v-app-bar>
    <v-app-bar v-else app elevation="0" color="white">
        <v-app-bar-title>Friendy</v-app-bar-title>

        <v-btn to="home" plain text class="ms-4 rounded-pill">
            {{ $t('home') }}
        </v-btn>

        <v-spacer></v-spacer>

        <v-btn to="login" plain text class="rounded-pill">
            {{ $t('login') }}
        </v-btn>

        <v-btn @click="signupContributor" plain class="success rounded-pill">
            <span class="mr-2">{{ $t('signupContributor') }}</span>
        </v-btn>

        <v-menu offset-y>
            <template v-slot:activator="{ attrs, on }">
                <v-btn text class="rounded-pill" v-bind="attrs" v-on="on">
                    <v-icon left>mdi-translate</v-icon>
                    {{ $t('language') }}
                </v-btn>
            </template>

            <v-list>
                <v-list-item v-for="item in languagesList" :key="item.value" link v-on:click="setLanguage(item.value)">
                    <v-list-item-title v-text="capitalizeFirst(item.text)"></v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>
    </v-app-bar>
</template>

<script>
import { mapMutations } from 'vuex'
import ConfigurationDialog from '@/components/ConfigurationDialog'

export default {
    name: 'AppBar',
    components: { ConfigurationDialog },
    data: function () {
        return {
            menu: false,
        }
    },
    methods: {
        logout: async function () {
            this.RESET_AUTHENTICATION_STATE()
            this.RESET_CONTRIBUTIONS_STATE()
            this.RESET_CONTEXTS_STATE()
            this.RESET_MESSAGES_STATE()
            this.RESET_PATTERNS_STATE()
            this.RESET_PROPOSITION_STATE()
            this.RESET_RESPONSES_STATE()
            this.RESET_ROLES_STATE()
            this.RESET_USERS_STATE()
            this.$emit('logout')
            await this.$router.push({ name: 'home' })
        },
        signupContributor: function () {
            this.$router.push({ name: 'signup', query: { contributor: true } })
        },
        setLanguage: function (language) {
            this.$i18n.locale = language
            this.SET_LANGUAGE(language)
        },
        ...mapMutations('authentication', ['RESET_AUTHENTICATION_STATE']),
        ...mapMutations('contributions', ['RESET_CONTRIBUTIONS_STATE']),
        ...mapMutations('contexts', ['RESET_CONTEXTS_STATE']),
        ...mapMutations('messages', ['RESET_MESSAGES_STATE']),
        ...mapMutations('patterns', ['RESET_PATTERNS_STATE']),
        ...mapMutations('propositions', ['RESET_PROPOSITION_STATE']),
        ...mapMutations('responses', ['RESET_RESPONSES_STATE']),
        ...mapMutations('roles', ['RESET_ROLES_STATE']),
        ...mapMutations('users', ['RESET_USERS_STATE']),
        ...mapMutations(['SET_LANGUAGE']),

    },
}
</script>

<style scoped lang="sass">

</style>
