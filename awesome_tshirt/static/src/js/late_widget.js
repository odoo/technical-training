odoo.define('awesome_tshirt.LateWidget', function (require) {
"use strict";

const basicFields = require('web.basic_fields');
const registry = require('web.field_registry');

const FieldBoolean = basicFields.FieldBoolean;

const LateWidget = FieldBoolean.extend({
    className: 'o_field_late_boolean',

    /**
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        this.lateColor = this.nodeOptions.late_color || 'red';
        this.notLateColor = this.nodeOptions.not_late_color || 'green';
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     * @private
     */
    _render: function () {
        this.$el.html($('<div>').css({
            backgroundColor: this.value ? this.lateColor : this.notLateColor
        }));
    },
});

registry.add('late_boolean', LateWidget);

return LateWidget;

});
