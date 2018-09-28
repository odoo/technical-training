odoo.define('awesome_tshirt.order_form_view', function (require) {
"use strict";

/**
 * This file defines a custom FormView for the model awesome_tshirt.order,
 * which adds a 'Print label' button to the ControlPanel.
 */

const core = require('web.core');
const FormController = require('web.FormController');
const FormView = require('web.FormView');
const viewRegistry = require('web.view_registry');

const _t = core._t;
const qweb = core.qweb;

const OrderFormController = FormController.extend({
    events: {
        'click .o_print_label': '_onPrintLabel',
    },

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
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Overrides to update the style and disabled status of the custom 'Print
     * Label' button.
     *
     * @override
     */
    _updateButtons: function () {
        this._super.apply(this, arguments);
        if (this.$buttons) {
            const state = this.model.get(this.handle, {raw: true});
            const disabled = this.mode === 'edit' && !state.res_id;
            const primary = state.data.customer_id && state.data.state === 'printed';
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
        if (this.printing) {
            return;
        }
        this.printing = true;
        const resID = this.model.get(this.handle, {raw: true}).res_id;
        this._rpc({
            model: 'awesome_tshirt.order',
            method: 'print_label',
            args: [resID],
        }).then((printed) => {
            this.printing = false;
            if (printed) {
                this.do_notify(_t('Success'), _t('The label has been printed'));
            } else {
                this.do_warn(_t('Failure'), _t('The label cannot be printed'), {sticky: true});
            }
            this.reload();
        }).guardedCatch(() => {
            this.printing = false;
            this.do_warn(_t('Error'), _t('An unexpected error occured'), {sticky: true});
        });
    },
});

const OrderFormView = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {
        Controller: OrderFormController,
    }),
});

viewRegistry.add('order_form_view', OrderFormView);

});
