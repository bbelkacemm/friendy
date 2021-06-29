import Vue from 'vue'
import Vuetify from 'vuetify/lib/framework'
import '@/styles/style.sass'
import VueGraph from 'vue-graph'
import LineChart from 'vue-graph/src/components/line.js'
import BarChart from 'vue-graph/src/components/bar.js'

Vue.use(VueGraph)
Vue.use(Vuetify)

Vue.component(LineChart.name, LineChart);
Vue.component(BarChart.name, BarChart);

export default new Vuetify({
    theme: {
        light: {
            primary: '#1976D2'
        }
    }
})
