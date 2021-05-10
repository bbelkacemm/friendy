import { get } from '@/helpers/HTTPHelper'

const state = {
    roles: [],
}

const mutations = {
    SET_ROLES: function (state, roles) {
        state.roles = roles
    },
    ADD_ROLE: function (state, role) {
        state.roles.push(role)
    },
    RESET_ROLES_STATE: function (state) {
        state.roles = []
    },
}

const actions = {
    setRoles: async function (context) {
        const roles = await get('/roles')
        context.commit('SET_ROLES', roles)
    },
    addRole: function (context, role) {
        context.commit('ADD_ROLE', role)
    },
}

const getters = {
    roles: (state) => state.roles,
    rolesAutocomplete: (state) => state.roles.map(item => {
        return { value: item.id, text: item.label }
    }),
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}
