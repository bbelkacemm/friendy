const state = {
    messages: [],
}

const mutations = {
    ADD_MESSAGE: function (state, message) {
        state.messages.push(message)
    },
    RESET_MESSAGES_STATE: function (state) {
        state.messages = []
    },
}

const actions = {
    addMessage: function (context, { value, sender }) {
        context.commit('ADD_MESSAGE', {
            'value': value,
            'sender': sender,
        })
    },
}

const getters = {
    messages: (state) => state.messages,
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}
