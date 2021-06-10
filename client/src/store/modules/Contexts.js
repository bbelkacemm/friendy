import { get } from '@/helpers/HTTPHelper'

const state = {
    contexts: [],
}

const mutations = {
    SET_CONTEXTS: function (state, contexts) {
        state.contexts = contexts
    },
    RESET_CONTEXTS_STATE: function (state) {
        state.contexts = []
    },
}

const actions = {
    getContexts: async function (context) {
        const response = await get('/contexts/valid')
        if (response.value) {
            context.commit('SET_CONTEXTS', response.data)
        }
    },
}

const getters = {
    contexts: (state) => state.contexts,
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}
