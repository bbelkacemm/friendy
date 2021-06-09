<template>
    <v-container fluid id="not-authorized-container" class="pa-16">
        <div>
            <v-icon color="grey lighten-2" size="128">mdi-lock</v-icon>
        </div>
        <div class="pa-4 title">
            {{ $t('notAuthorized') }}
        </div>
    </v-container>
</template>

<script>
export default {
    name: 'NotAuthorized',
}
</script>

<style scoped lang="sass">

#not-authorized-container
    display: grid
    place-items: center

</style>
