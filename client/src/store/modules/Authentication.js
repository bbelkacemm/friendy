const state = {
    user: null,
}

const mutations = {
    SET_USER: function (state, user) {
        state.user = user
    },
}

const actions = {
    setUser: function (context, user) {
        context.commit('SET_USER', user)
    },
}

const getters = {
    user: (state) => state.user,
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}
