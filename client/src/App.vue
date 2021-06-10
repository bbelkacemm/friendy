<template>
    <v-app>
        <app-bar v-on:clicked="clicked" v-on:logout="drawer = false"/>

        <navigation-drawer :drawer="drawer"></navigation-drawer>

        <v-main>
            <router-view></router-view>
        </v-main>
    </v-app>
</template>

<script>
import AppBar from '@/components/AppBar'
import NavigationDrawer from '@/components/NavigationDrawer'

export default {
    name: 'App',
    components: {
        NavigationDrawer,
        AppBar,
    },
    data: function () {
        return {
            drawer: false,
        }
    },
    methods: {
        clicked: function () {
            this.drawer = !this.drawer
        },
    },
}
</script>

<style lang="sass">
html
    overflow: auto !important

.v-main
    height: 1vh !important

</style>
