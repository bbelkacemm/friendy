const state = {
    user: null,
}

const mutations = {
    SET_USER: function (state, user) {
        state.user = user
    },
    RESET_AUTHENTICATION_STATE: function (state) {
        state.user = null
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
