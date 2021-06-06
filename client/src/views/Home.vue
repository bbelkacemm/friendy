<template>
    <v-container fluid v-if="user" class="fill-height">
        <div id="chat-bot-container" class="fill-height elevation-4">
            <div class="pa-4 grey lighten-4">
                <v-row no-gutters id="chat-header">
                    <v-col class="title text-uppercase font-weight-bold grey--text lighten-1">
                        {{ $t('mode') }} {{ mode.text }}
                    </v-col>
                    <v-col>
                        <v-switch class="ma-0" v-model="isProd" color="success" inset hide-details></v-switch>
                    </v-col>
                </v-row>
            </div>
            <div id="messages-container">
                <template v-for="(item, index) in messages">
                    <message :key="index" :value="item.value" :sender="item.sender"/>
                </template>
            </div>
            <div class="pa-4 grey--text text--lighten-1" v-if="isTyping">
                <v-icon color="grey lighten-1">mdi-dots-horizontal</v-icon>
                {{ $t('isTyping') }}
            </div>
            <div id="propositions-container">
                <template v-for="(item, index) in propositions">
                    <proposition v-on:clicked="send($event)" class="proposition-item" :value="item" :key="index"/>
                </template>
            </div>
            <v-form v-on:submit.prevent="" ref="form" id="input-grid" class="ma-2">
                <div>
                    <v-text-field v-model="message" hide-details="true" dense solo flat background-color="transparent"
                                  outline="false"></v-text-field>
                </div>
                <div>
                    <v-btn icon tile @click="validateSend" color="#291720">
                        <v-icon>mdi-send</v-icon>
                    </v-btn>
                </div>
            </v-form>
        </div>
    </v-container>
    <v-container v-else>
        <div class="title font-weight-bold text-center ma-10">
            Welcome!
        </div>
    </v-container>
</template>

<script>
import Proposition from '@/components/Proposition'
import Message from '@/components/Message'
import { get } from '@/helpers/HTTPHelper'
import { mapActions, mapGetters } from 'vuex'

export default {
    name: 'Home',
    components: { Message, Proposition },
    mounted: function () {
        this.scrollToBottom()
    },
    data: function () {
        return {
            message: null,
            isTyping: false,
            isProd: true,
        }
    },
    computed: {
        mode: function () {
            if (this.isProd)
                return {
                    text: this.$t('prod'),
                    value: 'prod',
                }
            else
                return {
                    text: this.$t('dev'),
                    value: 'dev',
                }
        },
        ...mapGetters('messages', ['messages']),
        ...mapGetters('propositions', ['propositions']),
    },
    methods: {
        validateSend: async function () {
            if (this.$refs.form.validate()) {
                const m = this.message
                this.message = null
                await this.send(m)
            }
        },
        send: async function (message) {
            this.isTyping = true
            this.addMessage({
                'value': message,
                'sender': true,
            })
            const response = await get('/', {
                'lang': 'en',
                'user-input': message,
                'tag': this.mode.value,
            })
            if (response !== 'responseError') {
                this.addMessage({
                    'value': response.response,
                })
                this.setPropositions(response.propositions)
            }
            this.scrollToBottom()
            this.isTyping = false
        },
        scrollToBottom: function () {
            const container = document.querySelector('#messages-container')
            if (container) {
                container.scrollTop = container.scrollHeight
            }
        },
        ...mapActions('messages', ['addMessage']),
        ...mapActions('propositions', ['setPropositions']),
    },
}
</script>

<style scoped lang="sass">

#chat-header
    display: grid
    grid-template-columns: 1fr auto

#chat-bot-container
    margin-left: 150px
    margin-right: 150px
    width: 100%
    display: grid
    grid-template-rows: auto 1fr auto auto

#input-grid
    display: grid
    grid-template-columns: 1fr auto
    align-items: center

#propositions-container
    display: flex
    justify-content: center
    align-items: center

#propositions-container .proposition-item
    display: inline-block

#messages-container
    overflow-y: auto

.v-text-field
    background-color: rgba(0, 0, 0, 0.05)

</style>
