odoo.define('awesome_tshirt.dashboard', function (require) {
"use strict";

/**
 * This file defines the Dashboard client action for the Awesome T-Shirt app. It
 * helps to manage the t-shirt business by displaying various statistics about
 * the orders and buttons to jump to specific views.
 */

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');

var Dashboard = AbstractAction.extend({
    start: function () {
        this.$el.html('Hello world');
        return this._super.apply(this, arguments);
    },
});

core.action_registry.add('awesome_tshirt.dashboard', Dashboard);

return Dashboard;

});
