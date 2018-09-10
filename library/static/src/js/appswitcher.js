odoo.define('library.AppSwitcher', function (require) {
"use strict";

var AppSwitcher = require('web_enterprise.AppSwitcher');
var core = require('web.core');

var QWeb = core.qweb;

AppSwitcher.include({
    render: function () {
        this._super.apply(this, arguments);
        if (moment().isoWeekday() === 1) {
            // only display on Mondays
            this.$el.prepend(QWeb.render('AppSwitcherWarning'));
        }
    },
});

});
