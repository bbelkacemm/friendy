<template>
    <v-app-bar app elevation="0" color="white" v-if="user">
        <v-app-bar-nav-icon @click="$emit('clicked')"></v-app-bar-nav-icon>

        <v-spacer></v-spacer>
        <div class="font-weight-bold text-uppercase grey--text body-2 ps-2 pe-2">
            {{ `${user['firstName']} ${user['lastName']}` }}
        </div>
        <v-avatar color="grey lighten-4" size="32"></v-avatar>
    </v-app-bar>
    <v-app-bar app elevation="0" v-else>
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
export default {
    name: 'AppBar',
}
</script>

<style scoped lang="sass">

</style>
