odoo.define('awesome_tshirt.dashboard', function (require) {
"use strict";

/**
 * This file defines the Dashboard client action for the Awesome T-Shirt app. It
 * helps to manage the t-shirt business by displaying various statistics about
 * the orders and buttons to jump to specific views.
 */

const MyCounter = require('awesome_tshirt.MyCounter');

const AbstractAction = require('web.AbstractAction');
const core = require('web.core');

const Dashboard = AbstractAction.extend({
    /**
     * @override
     */
    start: function () {
        const myCounter = new MyCounter(this);
        return Promise.all([
            myCounter.appendTo(this.$('.o_content')),
            this._super.apply(this, arguments)
        ]);
    },
});

core.action_registry.add('awesome_tshirt.dashboard', Dashboard);

return Dashboard;

});
