odoo.define('awesome_tshirt.dashboard', ['web.core'], function (require) {
"use strict";

/**
 * This file defines the Dashboard client action for the Awesome T-Shirt app. It
 * helps to manage the t-shirt business by displaying various statistics about
 * the orders and buttons to jump to specific views.
 */
var core = require('web.core');

var Statistics = Widget.extend({
    template: 'dashboard',
    init: function () {
        this.data = this._rpc({
            route: '/awesome_tshirt/statistics/'
        });
        var def = this.data.appendTo(this.$el);

        return $.when(def, this._super.apply(this, arguments));
    }
});


var Dashboard = AbstractAction.extend({
    /**
     * @override
     */
    start: function () {
        var statistics = new Statistics(this);
        var statisticsDef = statistics.appendTo(this.$el);
        var superDef = this._super.apply(this, arguments);
        return $.when(statisticsDef, superDef);
    },
});

core.action_registry.add('awesome_tshirt.dashboard', Dashboard);

return Dashboard;
});
