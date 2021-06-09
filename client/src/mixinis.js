import Vue from 'vue'
import i18n from '@/i18n'
import { mapGetters } from 'vuex'
import moment from 'moment'

Vue.mixin({
    data: function () {
        return {
            genderList: [
                {
                    text: i18n.t('f'),
                    value: 'f',
                },
                {
                    text: i18n.t('m'),
                    value: 'm',
                },
            ],
            languagesList: [
                {
                    text: i18n.t('en'),
                    value: 'en',
                },
                {
                    text: i18n.t('fr'),
                    value: 'fr',
                },
                {
                    text: i18n.t('ar'),
                    value: 'ar',
                },
            ],
            validationRules: {
                required: value => !!value || this.$t('requiredField'),
                passwordMatch: (password, confirm) => password === confirm || this.$t('passwordMatch'),
                passwordLength: (password) => password ? password.length <= 60 && password.length >= 8 || this.$t('passwordLength') : '',
            },
        }
    },
    computed: {
        ...mapGetters('authentication', ['user']),
    },
    methods: {
        formatDate: function (date, hours = false) {
            let format = 'MMMM Do YYYY'
            if (hours) format = 'MMMM Do YYYY HH:mm'
            if (date) {
                moment.locale('fr')
                return moment(date).format(format)
            }
        },
        formatDateForDatePicker: function (date) {
            if (date) {
                return moment(date).format('YYYY-MM-DD')
            }
        },
        capitalizeFirst: function (value) {
            if (typeof value !== 'string') return ''
            return value.charAt(0).toUpperCase() + value.slice(1)
        },
        getFullName: function (user) {
            if (!user) return ''
            return `${user.firstName} ${user.lastName}`
        },
        canUse: function (module, action) {
            const permission = this.user.role.permissions.find(item => item.label === module)
            return permission[action]
        },
        hasPrivilegesOf: function (label) {
            if (!this.user) return false
            if (this.user.role.label === 'administrator') {
                return true
            } else if (this.user.role.label === 'moderator') {
                if (label === 'administrator') return false
                return true
            } else if (this.user.role.label === 'contributor') {
                if (label === 'administrator') return false
                if (label === 'moderator') return false
                return true
            } else if (this.user.role.label === 'client' || this.user.role.label === 'guest') {
                if (label === 'administrator') return false
                if (label === 'moderator') return false
                if (label === 'contributor') return false
                return true
            }
            return false
        },
    },
})
