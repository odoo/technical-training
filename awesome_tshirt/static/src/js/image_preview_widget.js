odoo.define('awesome_tshirt.ImagePreview', function (require) {
"use strict";

/**
 * This files defines an ImagePreview field widget, which is an extention of the
 * FieldChar widget displaying the image of the url encoded in the field.
 */

const basicFields = require('web.basic_fields');
const registry = require('web.field_registry');

const FieldChar = basicFields.FieldChar;

const ImagePreview = FieldChar.extend({
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Overrides to display the image instead of its url.
     *
     * @override
     * @private
     */
    _renderReadonly: function () {
        if (this.value) {
            this.$el.html($('<img>', {
                class: 'o_image_preview',
                src: this.value,
            }));
        }
    },
});

registry.add('image_preview', ImagePreview);

return ImagePreview;

});
