import { get } from '@/helpers/HTTPHelper'

const state = {
    contexts: [],
}

const mutations = {
    SET_CONTEXTS: function (state, contexts) {
        state.contexts = contexts
    },
    ADD_CONTEXT: function (state, ctx) {
        state.contexts.push(ctx)
    },
    RESET_CONTEXTS_STATE: function (state) {
        state.contexts = []
    },
}

const actions = {
    getContexts: async function (context) {
        const contexts = await get('/contexts/valid')
        context.commit('SET_CONTEXTS', contexts)
    },
    addContext: function (context, ctx) {
        context.commit('ADD_CONTEXT', ctx)
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
