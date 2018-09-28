odoo.define('awesome_tshirt.customer_form_view', function (require) {
"use strict";

/**
 * This file defines a custom FormView for the model res.partner which adds a
 * 'Geolocate' button to the ControlPanel.
 */

const core = require('web.core');
const FormController = require('web.FormController');
const FormView = require('web.FormView');
const viewRegistry = require('web.view_registry');

const qweb = core.qweb;

const CustomerFormController = FormController.extend({
    events: {
        'click .o_geolocate': '_onGeolocate',
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * Overrides to add the 'Geolocate' button to the ControlPanel
     *
     * @override
     */
    renderButtons: function () {
        this._super.apply(this, arguments);
        this.$buttons.addClass('o_customer_form_buttons');
        this.$buttons.prepend(qweb.render('CustomerFormView.Buttons'));
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onGeolocate: function () {
        const resID = this.model.get(this.handle, {raw: true}).res_id;
        this._rpc({
            model: 'res.partner',
            method: 'geo_localize',
            args: [resID],
        }).then(() => this.reload());
    },
});

const CustomerFormView = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {
        Controller: CustomerFormController,
    }),
});

viewRegistry.add('customer_form_view', CustomerFormView);

});
