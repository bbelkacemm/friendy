const state = {
    patterns: [],
}

const mutations = {
    SET_PATTERNS: function (state, patterns) {
        state.patterns = patterns
    },
    ADD_PATTERN: function (state, pattern) {
        state.patterns.push(pattern)
    },
    RESET_PATTERNS_STATE: function (state) {
        state.patterns = []
    },
}

const actions = {
    setPatterns: function (context, patterns) {
        context.commit('SET_PATTERNS', patterns)
    },
    addPattern: function (context, pattern) {
        context.commit('ADD_PATTERN', pattern)
    },
}

const getters = {
    patterns: (state) => state.patterns,
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
}
