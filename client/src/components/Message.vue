<template>
    <v-card id="message-container" elevation="0" :style="{'direction': sender ? 'rtl' : 'ltr'}">
        <v-card-title>
            <v-avatar color="" style="background-color: #9CAFB7" size="32"></v-avatar>
        </v-card-title>
        <v-card-text class="pa-2 white--text font-weight-bold" style="background-color: #9CAFB7; direction: ltr">
            {{ value }}
        </v-card-text>
        <div></div>
    </v-card>
</template>

<script>
export default {
    name: 'Message',
    props: {
        sender: Boolean,
        value: String,
        time: Date,
    },
}
</script>

<style scoped lang="sass">

#message-container
    background-color: transparent
    display: grid
    grid-template-columns: auto auto 1fr
    align-items: center

</style>
