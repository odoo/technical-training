odoo.define('awesome_tshirt.dashboard', function (require) {
"use strict";

/**
 * This file defines the Dashboard client action for the Awesome T-Shirt app. It
 * helps to manage the t-shirt business by displaying various statistics about
 * the orders and buttons to jump to specific views.
 */

var ChartWidget = require('awesome_tshirt.ChartWidget');

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var fieldUtils = require('web.field_utils');

var _t = core._t;

var Dashboard = AbstractAction.extend({
    template: 'AwesomeDashboard',
    events: {
        'click .o_new_orders_btn': '_onOpenNewOrders',
        'click .o_customers_btn': '_onOpenCustomers',
        'click .o_cancelled_orders_btn': '_onOpenCancelledOrders',
    },
    custom_events: {
        open_orders: '_onOpenOrders',
    },

    /**
     * Override to load the statistics.
     *
     * @override
     */
    willStart: function () {
        var self = this;
        var statsDef = this._rpc({
            route: '/awesome_tshirt/statistics',
        }).then(function (stats) {
            stats.average_time = fieldUtils.format.float_time(stats.average_time);
            self.stats = stats;
        });
        var superDef = this._super.apply(this, arguments);
        return $.when(statsDef, superDef);
    },
    /**
     * @override
     */
    start: function () {
        var chartDef = this._renderChart();
        var superDef = this._super.apply(this, arguments);
        return $.when(chartDef, superDef);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Opens the list of orders created in the last 7 days
     *
     * @private
     * @param {Object} params
     * @param {Array[]} [params.domain=[]] additional domain
     * @returns {Promise} resolved when the action is executed
     */
    _openLastWeekOrders: function (params) {
        var aWeekAgo = moment().subtract(7,'d').locale('en').format('YYYY-MM-DD HH:mm:ss');
        params.domain = [['create_date', '>=', aWeekAgo]].concat(params.domain || []);
        return this._openOrders(params);
    },
    /**
     * Opens the list of orders matching a given domain.
     *
     * @private
     * @param {Object} params
     * @param {Array[]} [params.domain=[]]
     * @param {string} params.name name of the action
     * @returns {Promise} resolved when the action is executed
     */
    _openOrders: function (params) {
        return this.do_action({
            domain: params.domain,
            name: params.name,
            res_model: 'awesome_tshirt.order',
            type: 'ir.actions.act_window',
            views: [[false, 'list'], [false, 'form']],
        });
    },
    /**
     * Renders a PieChart widget.
     *
     * @private
     */
    _renderChart: function () {
        var chart = new ChartWidget(this, this.stats.orders_by_size);
        this.$('.o_fancy_chart').empty();
        return chart.appendTo(this.$('.o_fancy_chart'));
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onOpenCancelledOrders: function () {
        this._openLastWeekOrders({
            name: _t('Cancelled Orders'),
            domain: [['state', '=', 'cancelled']],
        });
    },
    /**
     * @private
     */
    _onOpenCustomers: function () {
        this.do_action('base.action_partner_customer_form');
    },
    /**
     * @private
     */
    _onOpenNewOrders: function () {
        this._openLastWeekOrders({
            name: _t('New Orders'),
            domain: [['state', '=', 'new']],
        });
    },
    /**
     * Opens the orders of t-shirt of the given size.
     *
     * @private
     * @param {OdooEvent} ev
     * @param {string} ev.data.size
     */
    _onOpenOrders: function (ev) {
        this._openOrders({
            name:  _.str.sprintf(_t("Orders of size %s"), ev.data.size.toUpperCase()),
            domain: [['size', '=', ev.data.size]],
        });
    },
});

core.action_registry.add('awesome_tshirt.dashboard', Dashboard);

return Dashboard;

});
