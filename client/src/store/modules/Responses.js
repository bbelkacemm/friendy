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
    EDIT_RESPONSE: function (state, payload) {
        state.responses.splice(payload.index, 1, payload.response)
    },
    DELETE_RESPONSE: function (state, index) {
        state.responses.splice(index, 1)
    },
}

const actions = {
    setResponses: function (context, responses) {
        context.commit('SET_RESPONSES', responses)
    },
    addResponse: function (context, response) {
        context.commit('ADD_RESPONSE', response)
    },
    // editResponse: function(context, response) {
    //     for (let index = 0; index < context.state.responses.length; index++) {
    //         if (context.state.responses[index].id === response.id) {
    //
    //             break
    //         }
    //     }
    // },
    // deleteResponse: function(context, response) {
    //     for(let index = 0; index < context.state.responses.length; index++) {
    //         if(context.state.responses[index].id === response.id) {
    //
    //             break
    //         }
    //     }
    // }
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
