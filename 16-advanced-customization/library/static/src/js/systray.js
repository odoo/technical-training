odoo.define('library.systray', function (require) {
"use strict";

var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');


var LibraryItem = Widget.extend({
    template: 'LibrarySystrayItem',
    sequence: 10,
    events: {
        'input .o_input': '_onInput',
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @override
     * @private
     */
    _onInput: function () {
        var id = parseInt(this.$('.o_input').val());
        if (!_.isNaN(id)) {
            this.do_action('library.action_customer_form', {
                res_id: id,
            });
        }
    },
});

SystrayMenu.Items.push(LibraryItem);

});
