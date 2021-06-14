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
        <v-spacer></v-spacer>

        <v-btn to="login" plain text>
            <span class="mr-2">{{ $t('login') }}</span>
            <v-icon>mdi-login</v-icon>
        </v-btn>

        <v-btn to="signup" plain text>
            <span class="mr-2">{{ $t('signup') }}</span>
            <v-icon>mdi-plus</v-icon>
        </v-btn>
    </v-app-bar>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
    name: 'AppBar',
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
        ...mapMutations('authentication', ['RESET_AUTHENTICATION_STATE']),
        ...mapMutations('contributions', ['RESET_CONTRIBUTIONS_STATE']),
        ...mapMutations('contexts', ['RESET_CONTEXTS_STATE']),
        ...mapMutations('messages', ['RESET_MESSAGES_STATE']),
        ...mapMutations('patterns', ['RESET_PATTERNS_STATE']),
        ...mapMutations('propositions', ['RESET_PROPOSITION_STATE']),
        ...mapMutations('responses', ['RESET_RESPONSES_STATE']),
        ...mapMutations('roles', ['RESET_ROLES_STATE']),
        ...mapMutations('users', ['RESET_USERS_STATE']),
    }
}
</script>

<style scoped lang="sass">

</style>
