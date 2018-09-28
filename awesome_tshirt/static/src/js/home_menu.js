
odoo.define('awesome_tshirt.HomeMenu', function (require) {
"use strict";

var core = require('web.core');
var HomeMenu = require('web_enterprise.HomeMenu');

var _t = core._t;

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
        var $message = $('<div>', {
            class: 'p-2 alert-warning o_custom_message',
        }).text(_t("Bafien Ckinpaers is watching you!"));
        $('<i class="fa fa-eye"></i><i class="fa fa-eye"></i>').appendTo($message);
        this.$('.o_custom_message').remove();
        this.$el.prepend($message);
    },
});

});
