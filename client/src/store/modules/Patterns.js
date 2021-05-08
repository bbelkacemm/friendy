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
    EDIT_PATTERN: function (state, payload) {
        state.patterns.splice(payload.index, 1, payload.patterns)
    },
    DELETE_PATTERN: function (state, index) {
        state.patterns.splice(index, 1)
    },
}

const actions = {
    setPatterns: function(context, patterns) {
        context.commit('SET_PATTERNS', patterns)
    },
    addPattern: function (context, pattern) {
        context.commit('ADD_PATTERN', pattern)
    },
    // editPattern: function(context, patterns) {
    //     for (let index = 0; index < context.state.patterns.length; index++) {
    //         if (context.state.patterns[index].id === patterns.id) {
    //
    //             break
    //         }
    //     }
    // },
    // deletePattern: function(context, patterns) {
    //     for(let index = 0; index < context.state.patterns.length; index++) {
    //         if(context.state.patterns[index].id === patterns.id) {
    //
    //             break
    //         }
    //     }
    // }
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
