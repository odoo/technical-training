odoo.define('awesome_tshirt.QuickOrderNavigation', function (require) {
"use strict";

var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');

var QuickOrderNavigation = Widget.extend({
    template: 'QuickOrderNavigation',
    sequence: 10,
    events: {
        'keydown .o_input': '_onInputKeydown',
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {KeyEvent} ev
     */
    _onInputKeydown: function (ev) {
        if (ev.which === $.ui.keyCode.ENTER) {
            var id = parseInt(this.$('.o_input').val());
            if (!_.isNaN(id)) {
                this.do_action({
                    res_id: id,
                    res_model: 'awesome_tshirt.order',
                    target: 'new',
                    type: 'ir.actions.act_window',
                    views: [[false, 'form']],
                });
            }
        }
    },
});

SystrayMenu.Items.push(QuickOrderNavigation);

});
