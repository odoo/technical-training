odoo.define('awesome_map.MapView', function (require) {
"use strict";

const AbstractView = require('web.AbstractView');
const core = require('web.core');
const viewRegistry = require('web.view_registry');

const MapModel = require('awesome_map.MapModel');
const MapRenderer = require('awesome_map.MapRenderer');

const _lt = core._lt;

const MapView = AbstractView.extend({
    config: _.extend({}, AbstractView.prototype.config, {
        Model: MapModel,
        Renderer: MapRenderer,
    }),
    display_name: _lt('Map'),
    icon: 'fa-globe',
    viewType: 'awesome_map',

    /**
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        this.loadParams.latitudeField = this.arch.attrs.latitude;
        this.loadParams.longitudeField = this.arch.attrs.longitude;
    },
});

viewRegistry.add('awesome_map', MapView);

});
