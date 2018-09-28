odoo.define('awesome_tshirt.ImagePreview', function (require) {
"use strict";

/**
 * This files defines an ImagePreview field widget, which is an extention of the
 * FieldChar widget displaying the image of the url encoded in the field.
 */

var basicFields = require('web.basic_fields');
var registry = require('web.field_registry');

var FieldChar = basicFields.FieldChar;

var ImagePreview = FieldChar.extend({
    /**
     * Overrides to display the image instead of its url.
     *
     * @override
     * @private
     */
    _renderReadonly: function () {
        if (this.value) {
            this.$el.html($('<img>', {src: this.value}));
        } else {
            this.$el.text(_("MISSING TSHIRT DESIGN"));
            this.$el.addClass('alert-danger');
        }
    },
    /**
     * Overrides to force this field to be always visible, as when it is unset,
     * we want to display a warning.
     */
    isSet: function () {
        return true;
    },
});

registry.add('image_preview', ImagePreview);

return ImagePreview;

});
