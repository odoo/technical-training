odoo.define('awesome_tshirt.dashboard', ['web.ajax'],, function (require) {
"use strict";

/**
 * This file defines the Dashboard client action for the Awesome T-Shirt app. It
 * helps to manage the t-shirt business by displaying various statistics about
 * the orders and buttons to jump to specific views.
 */


var Widget = require('web.Widget');
var ajax = require('web.ajax');

var Dashboard = Widget.extend({
     template: 'dashboard',
    init: function (parent) {
        this._super(parent);
        var data = this._rpc({
            route: '/awesome_tshirt/statistics/'
        });
    },
});

return Dashboard;
});
