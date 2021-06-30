import Vue from 'vue'
import Vuex from 'vuex'
import Authentication from '@/store/modules/Authentication'
import Messages from '@/store/modules/Messages'
import Propositions from '@/store/modules/Propositions'
import createPersistedState from 'vuex-persistedstate'
import Users from '@/store/modules/Users'
import Roles from '@/store/modules/Roles'
import Patterns from '@/store/modules/Patterns'
import Responses from '@/store/modules/Responses'
import Contexts from '@/store/modules/Contexts'
import Contributions from '@/store/modules/Contributions'
import Models from '@/store/modules/Models'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        mainLanguage: 'en',
    },
    mutations: {
        SET_LANGUAGE: function (state, language) {
            state.mainLanguage = language
        },
    },
    actions: {},
    getters: {
        mainLanguage: (state) => state.mainLanguage,
    },
    modules: {
        authentication: Authentication,
        messages: Messages,
        propositions: Propositions,
        users: Users,
        roles: Roles,
        contributions: Contributions,
        contexts: Contexts,
        patterns: Patterns,
        responses: Responses,
        models: Models,
    },
    plugins: [
        createPersistedState(),
    ],
})
