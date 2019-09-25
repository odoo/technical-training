odoo.define('awesome_tshirt.dashboard', function (require) {
"use strict";

/**
 * This file defines the Dashboard client action for the Awesome T-Shirt app. It
 * helps to manage the t-shirt business by displaying various statistics about
 * the orders and buttons to jump to specific views.
 */

const ChartWidget = require('awesome_tshirt.ChartWidget');

const AbstractAction = require('web.AbstractAction');
const core = require('web.core');
const fieldUtils = require('web.field_utils');

const _t = core._t;
const qweb = core.qweb;

const Dashboard = AbstractAction.extend({
    hasControlPanel: true,
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
        return Promise.all([
            this._loadStatistics(),
            this._super.apply(this, arguments)
        ]);
    },
    /**
     * @override
     */
    start: function () {
        return Promise.all([
            this._render(),
            this._super.apply(this, arguments)
        ]).then(() => {
            this.$('.o_cp_buttons').append(qweb.render('AwesomeDashboard.Buttons'));
        });
    },
    /**
     * Called when the dashboard will be restored (e.g. by coming back using the
     * breadcrumb).
     *
     * @override
     */
    do_show: function () {
        return this._reload();
    },
    /**
     * Called each time the dashboard is inserted into the DOM. Reloads and
     * re-renders the dashboard every 30s.
     *
     * @override
     */
    on_attach_callback: function () {
        this._reloadInterval = setInterval(this._reload.bind(this), 30000);
    },
    /**
     * Called each time the dashboard is detached from the DOM. Stops reloading
     * the dashboard every 30s if it is no longer into the DOM.
     *
     * @override
     */
    on_detach_callback: function () {
        clearInterval(this._reloadInterval);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     * @returns {Promise} resolved when the statistics have been fetched
     */
    _loadStatistics: function () {
        return this._rpc({
            route: '/awesome_tshirt/statistics',
        }).then((stats) => {
            stats.average_time = fieldUtils.format.float_time(stats.average_time);
            this.stats = stats;
        });
    },
    /**
     * Opens the list of orders created in the last 7 days.
     *
     * @private
     * @param {Object} params
     * @param {Array[]} [params.domain=[]] additional domain
     * @returns {Promise} resolved when the action is executed
     */
    _openLastWeekOrders: function (params) {
        const aWeekAgo = moment().subtract(7, 'd').locale('en').format('YYYY-MM-DD HH:mm:ss');
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
            name: params.name,
            res_model: 'awesome_tshirt.order',
            type: 'ir.actions.act_window',
            views: [[false, 'list'], [false, 'form']],
            domain: params.domain,
        });
    },
    /**
     * Reloads and re-renders the dashboard.
     *
     * @private
     * @returns {Promise} resolved when the dashboard has been re-rendered
     */
    _reload: function () {
        return this._loadStatistics().then(() => this._render());
    },
    /**
     * Renders the dashboard.
     *
     * @private
     * @return {Promise}
     */
    _render: function () {
        this.$('.o_content').html(qweb.render('AwesomeDashboard', { widget: this }));
        const chart = new ChartWidget(this, this.stats.orders_by_size);
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
            name: _.str.sprintf(_t("Orders of size %s"), ev.data.size.toUpperCase()),
            domain: [['size', '=', ev.data.size]],
        });
    },
});

core.action_registry.add('awesome_tshirt.dashboard', Dashboard);

return Dashboard;

});
