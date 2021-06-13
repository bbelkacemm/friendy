const state = {
    responses: [],
    temporaryId: 0,
}

const mutations = {
    SET_RESPONSES: function (state, responses) {
        state.responses = responses
    },
    ADD_RESPONSE: function (state, response) {
        state.responses.push(response)
    },
    EDIT_RESPONSE: function (state, { index, response }) {
        state.responses.splice(index, 1, response)
    },
    DELETE_RESPONSE: function (state, index) {
        state.responses.splice(index, 1)
    },
    RESET_RESPONSES_STATE: function (state) {
        state.responses = []
    },
    INCREMENT_TEMPORARY_ID: function (state) {
        state.temporaryId++
    },
}

const actions = {
    setResponses: function (context, responses) {
        context.commit('SET_RESPONSES', responses)
    },
    addResponse: function (context, response) {
        if (!response.id) response.temporaryId = context.state.temporaryId
        context.commit('ADD_RESPONSE', response)
        context.commit('INCREMENT_TEMPORARY_ID')
    },
    editResponse: function (context, response) {
        context.commit('EDIT_RESPONSE', {
            index: context.state.responses.findIndex(item => {
                if (response.id) return item.id === response.id
                else return item.temporaryId === response.temporaryId
            }),
            response: response,
        })
    },
    deleteResponse: async function (context, response) {
        if (response.status) {
            await context.dispatch('editResponse', response)
        } else {
            context.commit('DELETE_RESPONSE', context.state.responses.findIndex(item => item.temporaryId === response.temporaryId))
        }
    },
}

const getters = {
    responses: (state) => state.responses,
    filteredResponses: (state) => state.responses.filter(item => item.status !== 'delete'),
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}
