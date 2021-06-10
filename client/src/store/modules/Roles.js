import { get, remove } from '@/helpers/HTTPHelper'

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
    EDIT_ROLE: function (state, { index, role }) {
        state.roles.splice(index, 1, role)
    },
    DELETE_ROLE: function (state, index) {
        state.roles.splice(index, 1)
    },
    RESET_ROLES_STATE: function (state) {
        state.roles = []
    },
}

const actions = {
    setRoles: async function (context) {
        const response = await get('/roles')
        if (response.value) {
            context.commit('SET_ROLES', response.data)
        }
    },
    addRole: function (context, role) {
        context.commit('ADD_ROLE', role)
    },
    editRole: function (context, role) {
        context.commit('EDIT_ROLE', {
            index: context.state.roles.findIndex(i => i.id === role.id),
            role: role,
        })
    },
    deleteRole: async function (context, role) {
        const deleted = await remove(`/roles/role/${role.id}`)
        if (deleted.value === true) {
            context.commit('DELETE_ROLE', context.state.roles.findIndex(i => i.id === role.id))
            return true
        }
        return false
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
