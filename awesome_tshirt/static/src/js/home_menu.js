
odoo.define('awesome_tshirt.HomeMenu', function (require) {
"use strict";

const core = require('web.core');
const HomeMenu = require('web_enterprise.HomeMenu');

const qweb = core.qweb;

HomeMenu.include({
    /**
     * Overrides to load the custom message to display.
     *
     * @override
     */
    willStart: function () {
        const messageProm = this._rpc({
            route: '/awesome_tshirt/bafienistalkingtoyou',
        }).then((message) => {
            this.message = message;
        });
        return Promise.all([
            this._super.apply(this, arguments),
            messageProm
        ]);
    },

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
        this.$el.prepend(qweb.render('HomeMenu.Message', {message: this.message}));
    },
});

});
