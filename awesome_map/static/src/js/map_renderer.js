odoo.define('awesome_map.MapRenderer', function (require) {
"use strict";

var AbstractRenderer = require('web.AbstractRenderer');
var QWeb = require('web.QWeb');
var session = require('web.session');
var utils = require('web.utils');

var MapRenderer = AbstractRenderer.extend({
    className: "o_map_view",

    /**
     * @override
     */
    init: function (parent, state, params) {
        this._super.apply(this, arguments);
        this.latitudeField = params.latitudeField;
        this.longitudeField = params.longitudeField;

        this.mapInitialized = false;

        this.qweb = new QWeb(session.debug, {_s: session.origin}, false);
        this.qweb.add_template(utils.json_node_to_xml(params.template));
    },
    /**
     * Initializes the map on the on_attach_callback hook, as the library
     * requires the container to be in the DOM to properly render the map.
     *
     * @override
     */
    on_attach_callback: function () {
        this._initializeMap();
        this._renderDataPoints();
        this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Initializes the map. Ensures that this is done only once.
     *
     * @private
     */
    _initializeMap: function () {
        if (this.mapInitialized) {
            return;
        }
        this.mapInitialized = true;

        var initialLat = this.state[0] ? this.state[0][this.latitudeField] : 51.505;
        var initialLong = this.state[0] ? this.state[0][this.longitudeField] : -0.09;
        var options = { zoomControl: false };
        this.leafletMap = L.map(this.el, options).setView([initialLat, initialLong], 13);
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.leafletMap);
    },
    /**
     * Renders the data points on the map.
     *
     * @private
     */
    _renderDataPoints: function () {
        var self = this;
        _.each(this.state, function (point) {
            L.marker([point[self.latitudeField], point[self.longitudeField]])
                .addTo(self.leafletMap)
                .bindPopup(self.qweb.render('map-popup', {record: point}));
        });
    },
});

return MapRenderer;

});
