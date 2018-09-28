odoo.define('awesome_map.MapView', function (require) {
"use strict";

var AbstractView = require('web.AbstractView');
var viewRegistry = require('web.view_registry');

var MapView = AbstractView.extend({});

viewRegistry.add('map', MapView);

});
