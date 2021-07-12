import { Line } from 'vue-chartjs'

export default {
    extends: Line,
    props: {
        chartData: {
            type: Object,
            default: null,
        },
        options: {
            type: Object,
            default: null,
        },
    },
    mounted: function () {
        this.renderChart(this.chartData, this.options)
    },
    watch: {
        chartData: function () {
            this.renderChart(this.chartData, this.options)
        },
    },
}
