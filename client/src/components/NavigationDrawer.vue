<template>
    <v-navigation-drawer app hide-overlay v-model="drawer">
        <v-list nav dense>
            <v-list-item-group>
                <v-list-item to="home">
                    <v-list-item-icon>
                        <v-icon>mdi-home</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>{{ capitalizeFirst($t('home')) }}</v-list-item-title>
                </v-list-item>

            </v-list-item-group>

            <v-subheader>{{ $t('contribution').toUpperCase() }}</v-subheader>

            <v-list-item-group>
                <v-list-item @click="item.initialize" :key="index" v-for="(item,index) in contribution" :to="item.link">
                    <v-list-item-icon>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>{{ capitalizeFirst($t(item.label)) }}</v-list-item-title>
                </v-list-item>
            </v-list-item-group>

            <v-subheader>{{ $t('administration').toUpperCase() }}</v-subheader>

            <v-list-item-group>
                <v-list-item @click="item.initialize" :key="index" v-for="(item,index) in admin" :to="item.link">
                    <v-list-item-icon>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>{{ capitalizeFirst($t(item.label)) }}</v-list-item-title>
                </v-list-item>
            </v-list-item-group>

        </v-list>

        <template v-slot:append>
            <v-btn @click="logout" block tile elevation="0" class="error">
                <v-icon left>mdi-logout</v-icon>
                {{ $t('logout') }}
            </v-btn>
        </template>
    </v-navigation-drawer>
</template>

<script>
import { mapActions, mapMutations } from 'vuex'

export default {
    name: 'NavigationDrawer',
    props: {
        drawer: Boolean,
    },
    data: function () {
        return {
            contribution: [
                {
                    icon: 'mdi-plus',
                    link: 'contributions',
                    label: 'contributions',
                    initialize: () => {
                        this.getContributions()
                    },
                },
                {
                    icon: 'mdi-plus',
                    link: 'contexts',
                    label: 'contexts',
                    initialize: () => {
                        this.getContexts()
                    },
                },
            ],
            admin: [
                {
                    icon: 'mdi-monitor-dashboard',
                    link: 'dashboard',
                    label: 'dashboard',
                    initialize: () => {

                    },
                },
                {
                    icon: 'mdi-account',
                    link: 'users',
                    label: 'users',
                    initialize: () => {
                        this.setRoles()
                        this.getUsers()
                    },
                },
                {
                    icon: 'mdi-account',
                    link: 'roles',
                    label: 'roles',
                    initialize: () => {
                        this.setRoles()
                    },
                },
            ],
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
        ...mapActions('authentication', ['setUser']),
        ...mapActions('users', ['getUsers']),
        ...mapActions('roles', ['setRoles']),
        ...mapActions('contributions', ['getContributions']),
        ...mapActions('contexts', ['getContexts']),
        ...mapMutations('authentication', ['RESET_AUTHENTICATION_STATE']),
        ...mapMutations('contributions', ['RESET_CONTRIBUTIONS_STATE']),
        ...mapMutations('contexts', ['RESET_CONTEXTS_STATE']),
        ...mapMutations('messages', ['RESET_MESSAGES_STATE']),
        ...mapMutations('patterns', ['RESET_PATTERNS_STATE']),
        ...mapMutations('propositions', ['RESET_PROPOSITION_STATE']),
        ...mapMutations('responses', ['RESET_RESPONSES_STATE']),
        ...mapMutations('roles', ['RESET_ROLES_STATE']),
        ...mapMutations('users', ['RESET_USERS_STATE']),
    },
}
</script>

<style scoped>

</style>
