odoo.define('awesome_tshirt.MyCounter', function (require) {
"use strict";

/**
 * This file defines the MyCounter widget, displaying a counter with two buttons
 * allowing to increment and decrement it.
 */

var Widget = require('web.Widget');

var MyCounter = Widget.extend({
    template: 'MyCounter',
    events: {
        'click .o_decrement': '_onDecrement',
        'click .o_increment': '_onIncrement',
    },

    /**
     * @override
     */
    init: function () {
        this.value = 0;
        this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Decrement the counter and re-render the widget.
     *
     * @private
     */
    _onDecrement: function () {
        this.value--;
        this.renderElement();
    },
    /**
     * Increment the counter and re-render the widget.
     *
     * @private
     */
    _onIncrement: function () {
        this.value++;
        this.renderElement();
    },
});

return MyCounter;

});
