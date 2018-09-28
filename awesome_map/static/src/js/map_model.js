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
     * @param {string} params.modelName
     * @param {string[]} [params.fieldNames]
     * @param {Object} [params.context]
     * @param {Array[]} [params.domain]
     * @returns {Promise}
     */
    load: function (params) {
        return this._rpc({
            model: params.modelName,
            method: 'search_read',
            context: params.context || {},
            fields: params.fieldNames || [],
            domain: params.domain || [],
        }).then(results => {
            this.data = results;
        });
    },
});

return MapModel;

});
