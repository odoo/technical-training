odoo.define('library.ChartWidget', function (require) {
"use strict";

var ajax = require('web.ajax');
var Widget = require('web.Widget');

// var QWeb = core.qweb;
// var _t = core._t;


var ChartWidget = Widget.extend({
    tagName: 'canvas',
    jsLibs: ['/library/static/lib/chart.js/Chart.js'],

    /**
     * @override
     */
    init: function (parent, data) {
        this._super.apply(this, arguments);
        this.data = data;
    },
    /**
     * @override
     */
    willStart: function () {
        return $.when(ajax.loadLibs(this), this._super.apply(this, arguments));
    },
    /**
     * @override
     */
    start: function () {
        this._renderChart();
        return this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Renders the chart
     *
     * @private
     */
    _renderChart: function () {
        var self = this;
        new Chart(this.el, {
            type: 'pie',
            data: {
                labels: ["Available", "Rented", "Lost"],
                datasets: [{
                    label: '# of Books',
                    data: [
                        this.data.nb_available_books,
                        this.data.nb_rented_books,
                        this.data.nb_lost_books,
                    ],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255,99,132,1)',
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                onClick: function (event, chartElements) {
                    var types = ['available', 'rented', 'lost'];
                    if (chartElements && chartElements.length) {
                        self.trigger_up('open_books', {state: types[chartElements[0]._index]});
                    }
                },
            },
        });
    },
});

return ChartWidget;

});
