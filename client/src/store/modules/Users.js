import { get } from '@/helpers/HTTPHelper'

const state = {
    users: [],
}

const mutations = {
    SET_USERS: function (state, users) {
        state.users = users
    },
    ADD_USER: function (state, user) {
        state.users.push(user)
    },
    EDIT_USER: function (state, { index, user }) {
        state.users.splice(index, 1, user)
    },
    DELETE_USER: function (state, index) {
        state.users.splice(index, 1)
    },
}

const actions = {
    setUsers: async function (context) {
        const users = await get('/users')
        context.commit('SET_USERS', users)
    },
    addUser: function (context, user) {
        context.commit('ADD_USER', user)
    },
    editUser: function (context, user) {
        context.commit('EDIT_USER', {
            index: context.state.users.findIndex(item => item.id === user.id),
            user: user,
        })
    },
}

const getters = {
    users: (state) => state.users,
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}
