odoo.define('awesome_tshirt.ImagePreview', function (require) {
"use strict";

/**
 * This files defines an ImagePreview field widget, which is an extention of the
 * FieldChar widget displaying the image of the url encoded in the field.
 */

const basicFields = require('web.basic_fields');
const core = require('web.core');
const registry = require('web.field_registry');

const _t = core._t;
const FieldChar = basicFields.FieldChar;

const ImagePreview = FieldChar.extend({
    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * Overrides to force this field to be always visible, as when it is unset,
     * we want to display a warning.
     *
     * @override
     */
    isSet: function () {
        return true;
    },

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
        } else {
            this.$el.text(_t("MISSING TSHIRT DESIGN"));
            this.$el.addClass('alert-danger');
        }
    },
});

registry.add('image_preview', ImagePreview);

return ImagePreview;

});
