odoo.define('awesome_map.MapRenderer', function (require) {
"use strict";

const AbstractRenderer = require('web.AbstractRenderer');

const MapRenderer = AbstractRenderer.extend({
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    _render: function () {
        this.$el.text('Hello world');
        return this._super.apply(this, arguments);
    },
});

return MapRenderer;

});
