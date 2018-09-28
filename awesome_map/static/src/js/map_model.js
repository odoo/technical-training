odoo.define('awesome_map.MapModel', function (require) {
"use strict";

var AbstractModel = require('web.AbstractModel');

var MapModel = AbstractModel.extend({
    /**
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        this.data = null;
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @override
     * @returns {Object}
     */
    get: function () {
        return this.data;
    },

    /**
     * @override
     * @param {Object} params
     * @param {string} params.latitudeField
     * @param {string} params.longitudeField
     * @param {Object} params.context
     * @param {Array[]} params.domain
     * @returns {Deferred}
     */
    load: function (params) {
        var self = this;
        return this._rpc({
            model: params.modelName,
            method: 'search_read',
            context: params.context,
            fields: params.fieldNames,
            domain: params.domain
        }).then(function (results) {
            self.data = results;
        });
    },
});

return MapModel;

});
