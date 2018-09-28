odoo.define('awesome_map.MapController', function (require) {
"use strict";

const AbstractController = require('web.AbstractController');
const core = require('web.core');

const qweb = core.qweb;

const MapController = AbstractController.extend({
    custom_events: _.extend({}, AbstractController.prototype.custom_events, {
        record_clicked: '_onRecordClicked',
    }),
    events: _.extend({}, AbstractController.prototype.events, {
        'click button.o_map_zoom_in': '_onZoomIn',
        'click button.o_map_zoom_out': '_onZoomOut',
    }),

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    renderButtons: function ($node) {
        this.$buttons = $(qweb.render("AwesomeMapView.buttons", {widget: this}));
        this.$buttons.appendTo($node);
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {OdooEvent} ev
     */
    _onRecordClicked: function (ev) {
        this.trigger_up('switch_view', {
            view_type: 'form',
            res_id: ev.data.id,
            mode: 'readonly',
            model: this.modelName,
        });
    },
    /**
     * @private
     */
    _onZoomIn: function () {
        this.renderer.zoomIn();
    },
    /**
     * @private
     */
    _onZoomOut: function () {
        this.renderer.zoomOut();
    },
});

return MapController;

});
