import { get } from '@/helpers/HTTPHelper'

const state = {
    contributions: [],
}

const mutations = {
    SET_CONTRIBUTIONS: function (state, contributions) {
        state.contributions = contributions
    },
    ADD_CONTRIBUTION: function (state, contribution) {
        state.contributions.push(contribution)
    },
    EDIT_CONTRIBUTION: function (state, payload) {
        state.contributions.splice(payload.index, 1, payload.contribution)
    },
    DELETE_CONTRIBUTION: function (state, index) {
        state.contributions.splice(index, 1)
    },
}

const actions = {
    setContributions: async function (context) {
        const contributions = await get('/contributions')
        context.commit('SET_CONTRIBUTIONS', contributions)
    },
}

const getters = {
    contributions: (state) => state.contributions,
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}
