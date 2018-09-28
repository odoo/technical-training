odoo.define('awesome_tshirt.dashboard', function (require) {
"use strict";

/**
 * This file defines the Dashboard client action for the Awesome T-Shirt app. It
 * helps to manage the t-shirt business by displaying various statistics about
 * the orders and buttons to jump to specific views.
 */

var ChartWidget = require('awesome_tshirt.ChartWidget');

var AbstractAction = require('web.AbstractAction');
var ControlPanelMixin = require('web.ControlPanelMixin');
var core = require('web.core');
var fieldUtils = require('web.field_utils');

var _t = core._t;
var qweb = core.qweb;

var Dashboard = AbstractAction.extend(ControlPanelMixin, {
    template: 'AwesomeDashboard',
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
        this._renderButtons();
        return $.when(chartDef, superDef).then(this._updateControlPanel.bind(this));
    },
    /**
     * Override to unbind handlers on this.$buttons. This must be done because
     * the buttons are not appended inside the widget (as they are in the
     * ControlPanel, that attaches/detaches elements in its areas). So the
     * handlers aren't unbound automatically when this widget is destroyed.
     *
     * @override
     */
    destroy: function () {
        this._super.apply(this, arguments);
        if (this.$buttons) {
            this.$buttons.off();
        }
    },
    /**
     * Hook called when coming back to this widget using the breadcrumbs.
     *
     * @override
     */
    do_show: function () {
        this._super.apply(this, arguments);
        this._updateControlPanel();
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
     * Renders the buttons to put in the ControlPanel and binds event handlers
     * on them. Sets this.$buttons.
     */
    _renderButtons: function () {
        this.$buttons = $(qweb.render('AwesomeDashboard.Buttons'));
        this.$buttons.on('click', '.o_new_orders_btn', this._onOpenNewOrders.bind(this));
        this.$buttons.on('click', '.o_customers_btn', this._onOpenCustomers.bind(this));
        this.$buttons.on('click', '.o_cancelled_orders_btn', this._onOpenCancelledOrders.bind(this));
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
    /**
     * Puts the buttons in the control panel.
     *
     * @private
     */
    _updateControlPanel: function () {
        this.update_control_panel({
            cp_content: {
               $buttons: this.$buttons,
            },
        });
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
