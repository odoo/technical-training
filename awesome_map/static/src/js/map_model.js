odoo.define('awesome_map.MapModel', function (require) {
"use strict";

const AbstractModel = require('web.AbstractModel');

const MapModel = AbstractModel.extend({
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
     * @param {string} params.latitudeField
     * @param {string} params.longitudeField
     * @param {string} params.modelName
     * @param {Object} [params.context]
     * @param {Array[]} [params.domain]
     * @returns {Promise}
     */
    load: function (params) {
        const fields = [params.latitudeField, params.longitudeField];
        return this._rpc({
            model: params.modelName,
            method: 'search_read',
            context: params.context || {},
            fields: fields,
            domain: params.domain || [],
        }).then((results) => {
            this.data = _.map(results, (result) => {
                return {
                    id: result.id,
                    latitude: result[params.latitudeField],
                    longitude: result[params.longitudeField],
                };
            });
        });
    },
});

return MapModel;

});
