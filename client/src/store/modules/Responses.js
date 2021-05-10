const state = {
    responses: [],
}

const mutations = {
    SET_RESPONSES: function (state, responses) {
        state.responses = responses
    },
    ADD_RESPONSE: function (state, response) {
        state.responses.push(response)
    },
    RESET_RESPONSES_STATE: function (state) {
        state.responses = []
    },
}

const actions = {
    setResponses: function (context, responses) {
        context.commit('SET_RESPONSES', responses)
    },
    addResponse: function (context, response) {
        context.commit('ADD_RESPONSE', response)
    },
}

const getters = {
    responses: (state) => state.responses,
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}
