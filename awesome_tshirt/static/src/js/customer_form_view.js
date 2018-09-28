odoo.define('awesome_tshirt.customer_form_view', function (require) {
"use strict";

/**
 * This file defines a custom FormView for the model res.partner which adds a
 * 'Geolocate' button to the ControlPanel.
 */

var core = require('web.core');
var FormController = require('web.FormController');
var FormView = require('web.FormView');
var viewRegistry = require('web.view_registry');

var qweb = core.qweb;

var CustomerFormController = FormController.extend({
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
        this.$buttons.on('click', '.o_geolocate', this._onGeolocate.bind(this));
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onGeolocate: function () {
        var self = this;
        var res_id = this.model.get(this.handle, {raw: true}).res_id;
        this._rpc({
            model: 'res.partner',
            method: 'geo_localize',
            args: [res_id],
        }).then(function () {
            self.reload();
        });
    },
});

var CustomerFormView = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {
        Controller: CustomerFormController,
    }),
});

viewRegistry.add('customer_form_view', CustomerFormView);

});
