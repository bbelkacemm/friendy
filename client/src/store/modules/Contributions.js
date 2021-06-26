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
    EDIT_CONTRIBUTION: function (state, { index, contribution }) {
        state.contributions.splice(index, 1, contribution)
    },
    DELETE_CONTRIBUTION: function (state, index) {
        state.contributions.splice(index, 1)
    },
    RESET_CONTRIBUTIONS_STATE: function (state) {
        state.contributions = []
    },
}

const actions = {
    getContributions: async function (context) {
        const response = await get('/contributions')
        if (response.value) {
            context.commit('SET_CONTRIBUTIONS', response.data)
        }
    },
    addContribution: function (context, contribution) {
        context.commit('ADD_CONTRIBUTION', contribution)
    },
    editContribution: function (context, contribution) {
        context.commit('EDIT_CONTRIBUTION', {
            index: context.state.contributions.findIndex(item => item.id === contribution.id),
            contribution: contribution,
        })
    },
    deleteContribution: function (context, contribution) {
        context.commit('DELETE_CONTRIBUTION', context.state.contributions.findIndex(item => item.id === contribution.id))
    },
}

const getters = {
    contributions: (state) => state.contributions,
    pendingContributions: (state) => state.contributions.filter(contribution => contribution.status === 'pending'),
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}
