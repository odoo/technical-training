odoo.define('awesome_tshirt.MyCounter', function (require) {
"use strict";

/**
 * This file defines the MyCounter widget, displaying a counter with two buttons
 * allowing to increment and decrement it.
 */

var Widget = require('web.Widget');

var Buttons = Widget.extend({
    template: 'Buttons',
    events: {
        'click .all_customers': '_onAllCustomers',
        'click .recent_orders': '_onRecentOrders',
        'click .cancelled_orders': '_onCancelledOrders',
    },

    /**
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * When clicking button, display kanban with all customers.
     *
     * @private
     */
    _onAllCustomers: function () {
        // TODO
        this.renderElement();
    },
    /**
     * When clicking button, display a list of recent orders.
     *
     * @private
     */
    _onRecentOrders: function () {
        this.renderElement();
    },
    /**
     * When clicking button, display a list of cancelled orders.
     *
     * @private
     */
    _onCancelledOrders: function () {
        this.renderElement();
    },
});

return Buttons;

});
