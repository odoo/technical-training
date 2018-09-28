odoo.define('awesome_map.MapController', function (require) {
"use strict";

var AbstractController = require('web.AbstractController');

var MapController = AbstractController.extend({
    custom_events: _.extend({}, AbstractController.prototype.custom_events, {
        record_clicked: '_onRecordClicked',
    }),

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
});

return MapController;

});
