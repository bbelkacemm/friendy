import { get, post, remove } from '@/helpers/HTTPHelper'

const state = {
    models: [],
}

const mutations = {
    SET_MODELS: function (state, models) {
        state.models = models
    },
    EDIT_MODEL: function (state, { index, model }) {
        state.models.splice(index, 1, model)
    },
    DELETE_MODEL: function (state, index) {
        state.models.splice(index, 1)
    },
}

const actions = {
    setModels: async function (context) {
        const response = await get('/models')
        if (response.value) {
            context.commit('SET_MODELS', response.data)
        }
    },
    editModel: async function (context, { model, state, tag }) {
        let data = {}
        if (state) {
            data['state'] = state
            data['tag'] = null
        }
        if (tag) {
            data['state'] = null
            data['tag'] = tag
        }
        const result = await post(`/models/model/${model.path}`, data)
        context.commit('EDIT_MODEL', {
            index: context.state.models.findIndex(i => i.path === model.path),
            model: result.data,
        })
    },
    deleteModel: async function (context, model) {
        const deleted = await remove(`/models/model/${model.path}`)
        if (deleted.value === true) {
            context.commit('DELETE_MODEL', context.state.models.findIndex(i => i.path === model.path))
        }
    },
}

const getters = {
    models: (state) => state.models,
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}
