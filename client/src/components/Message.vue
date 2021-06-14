<template>
    <v-card id="message-container" elevation="0" :style="{'direction': sender ? 'rtl' : 'ltr'}">
        <v-card-title>
            <v-avatar color="#F5F5F5" size="32"></v-avatar>
        </v-card-title>
        <v-card-text :class="sender ? 'pa-3' : 'pa-3 elevation-4'" :style="messageStyle" >
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
    computed: {
        messageStyle: function () {
            let style = 'direction: ltr;'
            if(this.sender) {
                style += 'background-color: #F5F5F5; color: black; border-radius: 16px 8px 16px 16px;'
            } else{
                style += 'background-color: #448AFF; color: white; border-radius: 8px 16px 16px 16px;'
            }
            return style
        }
    }
}
</script>

<style scoped lang="sass">

#message-container
    background-color: transparent
    display: grid
    grid-template-columns: auto auto 1fr
    align-items: center

</style>
