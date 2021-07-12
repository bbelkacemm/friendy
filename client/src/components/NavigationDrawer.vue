<template>
    <v-navigation-drawer app hide-overlay v-model="drawer" :right="$vuetify.rtl">
        <v-list nav dense>
            <v-list-item-group>
                <v-list-item to="home">
                    <v-list-item-icon>
                        <v-icon>mdi-home</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>{{ capitalizeFirst($t('home')) }}</v-list-item-title>
                </v-list-item>

            </v-list-item-group>

            <v-subheader>{{ $t('administration').toUpperCase() }}</v-subheader>

            <v-list-item-group>
                <v-list-item @click="item.initialize" :key="index" v-for="(item,index) in admin" :to="item.link"
                             :disabled="!item.canUse">
                    <v-list-item-icon>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>{{ capitalizeFirst($t(item.label)) }}</v-list-item-title>
                </v-list-item>
            </v-list-item-group>

            <v-subheader>{{ $t('contribution').toUpperCase() }}</v-subheader>

            <v-list-item-group>
                <v-list-item @click="item.initialize" :key="index" v-for="(item,index) in contribution" :to="item.link"
                             :disabled="!item.canUse">
                    <v-list-item-icon>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>{{ capitalizeFirst($t(item.label)) }}</v-list-item-title>
                </v-list-item>
            </v-list-item-group>

        </v-list>
    </v-navigation-drawer>
</template>

<script>
import { mapActions } from 'vuex'

export default {
    name: 'NavigationDrawer',
    props: {
        drawer: Boolean,
    },
    computed: {
        admin: function () {
            return [
                {
                    icon: 'mdi-monitor-dashboard',
                    link: 'dashboard',
                    label: 'dashboard',
                    canUse: this.hasPrivilegesOf('administrator'),
                    initialize: () => {
                        this.setModels()
                        this.getUsers()
                        this.getContributions()
                    },
                },
                {
                    icon: 'mdi-account',
                    link: 'users',
                    label: 'users',
                    canUse: this.hasPrivilegesOf('administrator'),
                    initialize: () => {
                        this.setRoles()
                        this.getUsers()
                    },
                },
                {
                    icon: 'mdi-badge-account-outline',
                    link: 'roles',
                    label: 'roles',
                    canUse: this.hasPrivilegesOf('administrator'),
                    initialize: () => {
                        this.setRoles()
                    },
                },
                {
                    icon: 'mdi-brain',
                    link: 'models',
                    label: 'models',
                    canUse: this.hasPrivilegesOf('administrator'),
                    initialize: () => {
                        this.setModels()
                    },
                },
            ]
        },
        contribution: function () {
            return [
                {
                    icon: 'mdi-clipboard-edit-outline',
                    link: 'contributions',
                    label: 'contributions',
                    canUse: this.hasPrivilegesOf('contributor'),
                    initialize: () => {
                        this.getContributions()
                    },
                },
                {
                    icon: 'mdi-file-document',
                    link: 'contexts',
                    label: 'contexts',
                    canUse: this.hasPrivilegesOf('contributor'),
                    initialize: () => {
                        this.getContexts()
                    },
                },
            ]
        },
    },
    methods: {
        ...mapActions('authentication', ['setUser']),
        ...mapActions('users', ['getUsers']),
        ...mapActions('roles', ['setRoles']),
        ...mapActions('contributions', ['getContributions']),
        ...mapActions('contexts', ['getContexts']),
        ...mapActions('models', ['setModels']),
    },
}
</script>

<style scoped>

</style>
