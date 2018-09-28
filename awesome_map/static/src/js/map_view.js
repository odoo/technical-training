odoo.define('awesome_map.MapView', function (require) {
"use strict";

var MapController = require('awesome_map.MapController');
var MapModel = require('awesome_map.MapModel');
var MapRenderer = require('awesome_map.MapRenderer');

var AbstractView = require('web.AbstractView');
var core = require('web.core');
var viewRegistry = require('web.view_registry');

var _lt = core._lt;

var MapView = AbstractView.extend({
    config: _.extend({}, AbstractView.prototype.config, {
        Controller: MapController,
        Model: MapModel,
        Renderer: MapRenderer,
    }),
    cssLibs: ['/awesome_map/static/lib/leaflet/leaflet.css'],
    jsLibs: ['/awesome_map/static/lib/leaflet/leaflet.js'],
    display_name: _lt('Map'),
    icon: 'fa-globe',
    /**
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        this.rendererParams.latitudeField = this.arch.attrs.latitude;
        this.rendererParams.longitudeField = this.arch.attrs.longitude;

        var fieldNames = [this.rendererParams.latitudeField, this.rendererParams.longitudeField];
        var template;
        _.each(this.arch.children, function (node) {
            if (node.tag === 'field') {
                fieldNames.push(node.attrs.name);
            }
            if (node.tag === 'template') {
                template = node;
            }
        });
        this.loadParams.fieldNames = _.uniq(fieldNames);
        this.rendererParams.template = template;
    },
});

viewRegistry.add('map', MapView);

});
