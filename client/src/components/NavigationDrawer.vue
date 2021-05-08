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
import { mapActions } from 'vuex'

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
                        this.setContributions()
                    },
                },
                {
                    icon: 'mdi-plus',
                    link: 'contexts',
                    label: 'contexts',
                    initialize: () => {
                        this.setContexts(null)
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
                        this.setUsers()
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
        logout: function () {
            this.setUser(null)
            this.setMessages([])
            this.setPropositions([])
            // TODO DELETE NEW DATA
            this.$emit('logout')
        },
        ...mapActions('authentication', ['setUser']),
        ...mapActions('messages', ['setMessages']),
        ...mapActions('propositions', ['setPropositions']),
        ...mapActions('users', ['setUsers']),
        ...mapActions('roles', ['setRoles']),
        ...mapActions('contributions', ['setContributions']),
        ...mapActions('contexts', ['setContexts']),
    },
}
</script>

<style scoped>

</style>
