<template>
    <v-container fluid id="not-found-container" class="pa-16">
        <div>
            <v-icon color="grey lighten-2" size="128">mdi-emoticon-sad</v-icon>
        </div>
        <div class="pa-4 title">
            {{ $t('notFound') }}
        </div>
    </v-container>
</template>

<script>
export default {
    name: 'NotFound',
}
</script>

<style scoped lang="sass">

#not-found-container
    display: grid
    place-items: center

</style>
