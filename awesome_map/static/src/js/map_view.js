odoo.define('awesome_map.MapView', function (require) {
"use strict";

var MapRenderer = require('awesome_map.MapRenderer');

var AbstractView = require('web.AbstractView');
var core = require('web.core');
var viewRegistry = require('web.view_registry');

var _lt = core._lt;

var MapView = AbstractView.extend({
    config: _.extend({}, AbstractView.prototype.config, {
        Renderer: MapRenderer,
    }),
    display_name: _lt('Map'),
    icon: 'fa-globe',
});

viewRegistry.add('map', MapView);

});
