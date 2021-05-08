const state = {
    messages: [],
}

const mutations = {
    SET_MESSAGES: function (state, messages) {
        state.messages = messages
    },
    ADD_MESSAGE: function (state, message) {
        state.messages.push(message)
    },
}

const actions = {
    setMessages: function (context, messages) {
        context.commit('SET_MESSAGES', messages)
    },
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
