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
        }
    },
});

registry.add('image_preview', ImagePreview);

return ImagePreview;

});
