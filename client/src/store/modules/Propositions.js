const state = {
    propositions: [],
}

const mutations = {
    SET_PROPOSITIONS: function (state, propositions) {
        state.propositions = propositions
    },
    RESET_PROPOSITION_STATE: function (state) {
        state.propositions = []
    },
}

const actions = {
    setPropositions: function (context, propositions) {
        context.commit('SET_PROPOSITIONS', propositions)
    },
}

const getters = {
    propositions: (state) => state.propositions,
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}
