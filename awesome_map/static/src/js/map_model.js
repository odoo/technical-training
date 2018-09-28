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
     */
    load: function (params) {
        this.fieldNames = params.fieldNames || [];
        this.modelName = params.modelName;
        return this._load(params);
    },
    /**
     * @override
     */
    reload: function (_, params) {
        return this._load(params);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {Object} params
     * @param {Object} [params.context]
     * @param {Array[]} [params.domain]
     * @returns {Deferred}
     */
    _load: function (params) {
        return this._rpc({
            model: this.modelName,
            method: 'search_read',
            context: params.context || {},
            fields: this.fieldNames,
            domain: params.domain || [],
        }).then(results => {
            this.data = results;
        });
    },
});

return MapModel;

});
