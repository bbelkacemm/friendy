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
    EDIT_CONTEXT: function (state, payload) {
        state.contexts.splice(payload.index, 1, payload.ctx)
    },
    DELETE_CONTEXT: function (state, index) {
        state.contexts.splice(index, 1)
    },
}

const actions = {
    setContexts: async function (context, contexts) {
        if (contexts) {
            context.commit('SET_CONTEXTS', contexts)
        } else {
            const contexts = await get('/contexts/valid')
            context.commit('SET_CONTEXTS', contexts)
        }
    },
    addContext: function (context, ctx) {
        context.commit('ADD_CONTEXT', ctx)
    },
    // editContext: function(context, ctx) {
    //     for (let index = 0; index < context.state.contexts.length; index++) {
    //         if (context.state.contexts[index].id === ctx.id) {
    //
    //             break
    //         }
    //     }
    // },
    // deleteContext: function(context, ctx) {
    //     for(let index = 0; index < context.state.contexts.length; index++) {
    //         if(context.state.contexts[index].id === ctx.id) {
    //
    //             break
    //         }
    //     }
    // }
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
