<template>
    <v-container fluid v-if="user" class="fill-height">
        <div id="chat-bot-container" class="fill-height">
            <div class=" lighten-4" v-if="hasPrivilegesOf('contributor')">
                <v-row no-gutters id="chat-header" class="pa-4">
                    <v-col class="subtitle-1 text-uppercase font-weight-bold grey--text lighten-1">
                        {{ $t('mode') }} {{ mode.text }}
                    </v-col>
                    <v-col>
                        <v-switch class="ma-0" v-model="isProd" color="#448AFF" inset hide-details></v-switch>
                    </v-col>
                </v-row>
                <v-divider></v-divider>
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
            <v-form v-on:submit.prevent="" ref="form" class="ma-2 input-grid">
                <div>
                    <v-text-field v-model="message" :label="capitalizeFirst($t('messageHint'))" hide-details="true" dense solo flat background-color="transparent"
                                  outline="false"></v-text-field>
                </div>
                <div>
                    <v-btn icon tile @click="validateSend" color="#448AFF" :disabled="!message || message.length === 0">
                        <v-icon>mdi-send</v-icon>
                    </v-btn>
                </div>
            </v-form>
        </div>
        <v-snackbar v-model="errorSnackbar" class="d-print-none" color="error">
            <template v-slot:default>
                {{ $t(errorMessage) }}
            </template>
            <template v-slot:action>
                <v-btn icon dark @click="errorSnackbar = false">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </template>
        </v-snackbar>
    </v-container>
    <v-container fluid class="pa-0" v-else>
        <div class="two-equal-columns">
            <div class="center-items">
                <bot class="ma-16" width="400"/>
            </div>
            <div class="pa-4">
                <div class="text-h2">
                    {{ capitalizeFirst($t('homeHeader')) }}
                </div>
                <div class="text-h5 mt-10">
                    {{ capitalizeFirst($t('homeDescription')) }}
                </div>
                <v-btn class="mt-10 rounded-pill primary" @click="signup" text>
                    {{ $t('signup') }}
                    <v-icon right>mdi-arrow-right</v-icon>
                </v-btn>
            </div>
        </div>
        <v-container fluid class="center-items pa-0 grey lighten-4">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120">
                <path fill="white" fill-opacity="1" d="M0,64L1440,96L1440,0L0,0Z"></path>
            </svg>
            <div class="text-h5 grey--text text-uppercase mb-4 font-weight-bold">
                {{ $t('features') }}
            </div>
            <div class="two-columns">
                <v-card v-for="feature in features" :key="feature.title"
                        class="ma-2 elevation-0 transparent text-center" width="350" height="250">
                    <v-card-text class="center-items">
                        <div>
                            <v-icon size="64" color="black">{{ feature.icon }}</v-icon>
                        </div>
                        <div class="text-h6 ma-4">{{ feature.title }}</div>
                        <div class="subtitle-2 grey--text">{{ feature.description }}</div>
                    </v-card-text>
                </v-card>
            </div>
        </v-container>
        <footer class="pa-2 pt-10 center-items grey lighten-4 grey--text">
            Friendy © {{ new Date().getFullYear() }}
        </footer>
    </v-container>
</template>

<script>
import Proposition from '@/components/Proposition'
import Message from '@/components/Message'
import { get } from '@/helpers/HTTPHelper'
import { mapActions, mapGetters } from 'vuex'
import Bot from '@/assets/bot.svg'

export default {
    name: 'Home',
    components: { Message, Proposition, Bot },
    mounted: function () {
        this.scrollToBottom()
    },
    data: function () {
        return {
            message: null,
            isTyping: false,
            isProd: true,
            errorSnackbar: false,
            errorMessage: null,
            features: [
                {
                    icon: 'mdi-robot',
                    iconColor: 'primary',
                    title: this.capitalizeFirst(this.$t('botTitle')),
                    description: this.capitalizeFirst(this.$t('botDescription')),
                },
                {
                    icon: 'mdi-doctor',
                    iconColor: 'success',
                    title: this.capitalizeFirst(this.$t('contributionsTitle')),
                    description: this.capitalizeFirst(this.$t('contributionsDescription')),
                },
            ],
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
        signup: function () {
            this.$router.push({ name: 'signup', query: { contributor: false } })
        },
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
                'value': this.capitalizeFirst(message),
                'sender': true,
            })
            const response = await get('/', {
                'lang': this.mainLanguage,
                'user-input': message,
                'tag': this.mode.value,
            })
            if (response.value) {
                this.addMessage({
                    'value': this.capitalizeFirst(response.data.response),
                })
                this.setPropositions(response.data.propositions)
            } else {
                this.errorSnackbar = true
                this.errorMessage = response.message
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
    width: 100%
    display: grid
    grid-template-rows: auto 1fr auto auto

#propositions-container
    display: flex
    justify-content: center
    align-items: center

#propositions-container .proposition-item
    display: inline-block

#messages-container
    overflow-y: auto

</style>
