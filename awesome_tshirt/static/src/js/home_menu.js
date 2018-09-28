
odoo.define('awesome_tshirt.HomeMenu', function (require) {
"use strict";

const core = require('web.core');
const HomeMenu = require('web_enterprise.HomeMenu');
const session = require('web.session');

const qweb = core.qweb;

HomeMenu.include({
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     * @private
     */
    _render: function () {
        this._super.apply(this, arguments);
        this.$('.o_custom_message').remove();
        this.$el.prepend(qweb.render('HomeMenu.Message', {
            message: session.home_menu_message,
        }));
    },
});

});
