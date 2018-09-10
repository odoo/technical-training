odoo.define('library.fields', function (require) {
"use strict";

var basicFields = require('web.basic_fields');
var core = require('web.core');
var fieldRegistry = require('web.field_registry');

var qweb = core.qweb;

var RawFieldInteger = basicFields.FieldInteger.extend({
    /**
     * @override
     */
    _formatValue: function (value) {
        return value;
    },
});

var LateWidget = basicFields.FieldBoolean.extend({
    className: 'o_field_late_boolean',
    init: function () {
        this._super.apply(this, arguments);
        this.lateColor = this.nodeOptions.late_color || 'red';
        this.notLateColor = this.nodeOptions.not_late_color || 'green';
    },
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

var LibraryWarning = basicFields.FieldFloat.extend({
    /**
     * @override
     * @private
     */
    _renderReadonly: function () {
        if (this.value > 1) {
            this.$el.html(qweb.render('LibraryWarning', {amount: this.value}));
        } else {
            this.$el.empty();
        }
    },


});

fieldRegistry.add('raw-field-integer', RawFieldInteger);
fieldRegistry.add('late-boolean', LateWidget);
fieldRegistry.add('library-debt-warning', LibraryWarning);

});