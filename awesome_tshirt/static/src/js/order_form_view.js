odoo.define('awesome_tshirt.order_form_view', function (require) {
"use strict";

/**
 * This file defines a custom FormView for the model awesome_tshirt.order,
 * which adds a 'Print label' button to the ControlPanel.
 */

var core = require('web.core');
var FormController = require('web.FormController');
var FormView = require('web.FormView');
var viewRegistry = require('web.view_registry');

var _t = core._t;
var qweb = core.qweb;

var OrderFormController = FormController.extend({
    /**
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        // printing flag is used to prevent from doing concurrent RPCs to print
        // the label (e.g. if the user double-clicks on the button)
        this.printing = false;
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * Overrides to add the 'Print Label' button to the ControlPanel
     *
     * @override
     */
    renderButtons: function () {
        this._super.apply(this, arguments);
        this.$buttons.addClass('o_order_form_buttons');
        this.$buttons.append(qweb.render('OrderFormView.Buttons'));
        this.$buttons.on('click', '.o_print_label', this._onPrintLabel.bind(this));
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Overrides to update the style and disabled status of the custom 'Print
     * Label' button.
     */
    _updateButtons: function () {
        this._super.apply(this, arguments);
        if (this.$buttons) {
            var state = this.model.get(this.handle, {raw: true});
            var disabled = this.mode === 'edit' && !state.res_id;
            var primary = state.data.customer_id && state.data.state === 'printed';
            this.$buttons.find('.o_print_label')
                .toggleClass('btn-primary', primary)
                .toggleClass('btn-secondary', !primary)
                .attr('disabled', !!disabled);
        }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onPrintLabel: function () {
        var self = this;
        if (this.printing) {
            return;
        }
        this.printing = true;
        var res_id = this.model.get(this.handle, {raw: true}).res_id;
        this._rpc({
            model: 'awesome_tshirt.order',
            method: 'print_label',
            args: [res_id],
        }).then(function (printed) {
            if (printed) {
                self.do_notify(_t('Success'), _t('The label has been printed'));
            } else {
                self.do_warn(_t('Failure'), _t('The label cannot be printed'), {sticky: true});
            }
            self.reload();
        }).always(function () {
            self.printing = false;
        });
    },
});

var OrderFormView = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {
        Controller: OrderFormController,
    }),
});

viewRegistry.add('order_form_view', OrderFormView);

});
