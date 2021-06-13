const state = {
    patterns: [],
    temporaryId: 0,
}

const mutations = {
    SET_PATTERNS: function (state, patterns) {
        state.patterns = patterns
    },
    ADD_PATTERN: function (state, pattern) {
        state.patterns.push(pattern)
    },
    EDIT_PATTERN: function (state, { index, pattern }) {
        state.patterns.splice(index, 1, pattern)
    },
    DELETE_PATTERN: function (state, index) {
        state.patterns.splice(index, 1)
    },
    RESET_PATTERNS_STATE: function (state) {
        state.patterns = []
    },
    INCREMENT_TEMPORARY_ID: function (state) {
        state.temporaryId++
    },
}

const actions = {
    setPatterns: function (context, patterns) {
        context.commit('SET_PATTERNS', patterns)
    },
    addPattern: function (context, pattern) {
        if (!pattern.id) pattern.temporaryId = context.state.temporaryId
        context.commit('ADD_PATTERN', pattern)
        context.commit('INCREMENT_TEMPORARY_ID')
    },
    editPattern: function (context, pattern) {
        context.commit('EDIT_PATTERN', {
            index: context.state.patterns.findIndex(item => {
                if (pattern.id) return item.id === pattern.id
                else return item.temporaryId === pattern.temporaryId
            }),
            pattern: pattern,
        })
    },
    deletePattern: async function (context, pattern) {
        if (pattern.status) {
            await context.dispatch('editPattern', pattern)
        } else {
            context.commit('DELETE_PATTERN', context.state.patterns.findIndex(item => item.temporaryId === pattern.temporaryId))
        }
    },
}

const getters = {
    patterns: (state) => state.patterns,
    filteredPatterns: (state) => state.patterns.filter(item => item.status !== 'delete'),
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}
