import { get, remove } from '@/helpers/HTTPHelper'

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
    RESET_USERS_STATE: function (state) {
        state.users = []
    },
}

const actions = {
    getUsers: async function (context) {
        const response = await get('/users')
        if (response.value) {
            context.commit('SET_USERS', response.data)
        }
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
    deleteUser: async function (context, user) {
        const deleted = await remove(`/users/user/${user.id}`)
        if (deleted.value === true) {
            context.commit('DELETE_USER', context.state.users.findIndex(item => item.id === user.id))
            return true
        } else {
            return deleted
        }
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
