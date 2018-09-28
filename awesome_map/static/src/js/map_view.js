odoo.define('awesome_map.MapView', function (require) {
"use strict";

const AbstractView = require('web.AbstractView');
const core = require('web.core');
const viewRegistry = require('web.view_registry');

const MapRenderer = require('awesome_map.MapRenderer');

const _lt = core._lt;

const MapView = AbstractView.extend({
    config: _.extend({}, AbstractView.prototype.config, {
        Renderer: MapRenderer,
    }),
    display_name: _lt('Map'),
    icon: 'fa-globe',
    viewType: 'awesome_map',
});

viewRegistry.add('awesome_map', MapView);

});
