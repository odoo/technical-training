odoo.define('awesome_tshirt.dashboard', function (require) {
"use strict";

/**
 * This file defines the Dashboard client action for the Awesome T-Shirt app. It
 * helps to manage the t-shirt business by displaying various statistics about
 * the orders and buttons to jump to specific views.
 */

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');

var _t = core._t;

var Dashboard = AbstractAction.extend({
    template: 'AwesomeDashboard',
    events: {
        'click .o_new_orders_btn': '_onOpenNewOrders',
        'click .o_customers_btn': '_onOpenCustomers',
        'click .o_cancelled_orders_btn': '_onOpenCancelledOrders',
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Opens the list of orders created in the last 7 days.
     *
     * @private
     * @param {Object} params
     * @param {Array[]} [params.domain=[]] additional domain
     * @param {string} params.name name of the action
     * @returns {Promise} resolved when the action is executed
     */
    _openLastWeekOrders: function (params) {
       var aWeekAgo = moment().subtract(7,'d').locale('en').format('YYYY-MM-DD HH:mm:ss');
        this.do_action({
            name: params.name,
            res_model: 'awesome_tshirt.order',
            type: 'ir.actions.act_window',
            views: [[false, 'list'], [false, 'form']],
            domain: [['create_date', '>=', aWeekAgo]].concat(params.domain || []),
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
});

core.action_registry.add('awesome_tshirt.dashboard', Dashboard);

return Dashboard;

});
