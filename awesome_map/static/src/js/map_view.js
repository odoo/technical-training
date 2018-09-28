odoo.define('awesome_map.MapView', function (require) {
"use strict";

const AbstractView = require('web.AbstractView');
const viewRegistry = require('web.view_registry');

const MapView = AbstractView.extend({});

viewRegistry.add('awesome_map', MapView);

});
