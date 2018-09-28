odoo.define('awesome_map.MapView', function (require) {
"use strict";

var MapModel = require('awesome_map.MapModel');
var MapRenderer = require('awesome_map.MapRenderer');

var AbstractView = require('web.AbstractView');
var core = require('web.core');
var viewRegistry = require('web.view_registry');

var _lt = core._lt;

var MapView = AbstractView.extend({
    config: _.extend({}, AbstractView.prototype.config, {
        Model: MapModel,
        Renderer: MapRenderer,
    }),
    display_name: _lt('Map'),
    icon: 'fa-globe',
    /**
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        this.loadParams.latitudeField = this.arch.attrs.latitude;
        this.loadParams.longitudeField = this.arch.attrs.longitude;
    },
});

viewRegistry.add('map', MapView);

});
