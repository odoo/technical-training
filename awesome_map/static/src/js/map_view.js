odoo.define('awesome_map.MapView', function (require) {
"use strict";

const AbstractView = require('web.AbstractView');
const core = require('web.core');
const viewRegistry = require('web.view_registry');

const MapController = require('awesome_map.MapController');
const MapModel = require('awesome_map.MapModel');
const MapRenderer = require('awesome_map.MapRenderer');

const _lt = core._lt;

const MapView = AbstractView.extend({
    config: _.extend({}, AbstractView.prototype.config, {
        Controller: MapController,
        Model: MapModel,
        Renderer: MapRenderer,
    }),
    cssLibs: ['/awesome_map/static/lib/leaflet/leaflet.css'],
    jsLibs: ['/awesome_map/static/lib/leaflet/leaflet.js'],
    display_name: _lt('Map'),
    icon: 'fa-globe',
    viewType: 'awesome_map',

    /**
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        this.rendererParams.latitudeField = this.arch.attrs.latitude;
        this.rendererParams.longitudeField = this.arch.attrs.longitude;

        const fieldNames = [this.rendererParams.latitudeField, this.rendererParams.longitudeField];
        let template;
        this.arch.children.forEach(node => {
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

viewRegistry.add('awesome_map', MapView);

});
