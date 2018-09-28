odoo.define('awesome_map.MapRenderer', function (require) {
"use strict";

const AbstractRenderer = require('web.AbstractRenderer');
const QWeb = require('web.QWeb');
const session = require('web.session');
const utils = require('web.utils');

const MapRenderer = AbstractRenderer.extend({
    className: "o_map_view",

    /**
     * @override
     */
    init: function (parent, state, params) {
        this._super.apply(this, arguments);
        this.latitudeField = params.latitudeField;
        this.longitudeField = params.longitudeField;

        this.isInDOM = false;
        this.mapInitialized = false;
        this.markers = [];

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
        this.isInDOM = true;
        this._initializeMap();
        this._renderDataPoints();
        this._super.apply(this, arguments);
    },
    /**
     * @override
     */
    on_detach_callback: function () {
        this.isInDOM = false;
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    zoomIn: function () {
        this.leafletMap.zoomIn();
    },
    zoomOut: function () {
        this.leafletMap.zoomOut();
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

        const initialLat = this.state[0] ? this.state[0][this.latitudeField] : 51.505;
        const initialLong = this.state[0] ? this.state[0][this.longitudeField] : -0.09;
        const options = { zoomControl: false };
        this.leafletMap = L.map(this.el, options).setView([initialLat, initialLong], 13);
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.leafletMap);
    },
    /**
     * @override
     */
    _render: function () {
        if (this.isInDOM) {
            this._renderDataPoints();
        }
        return this._super.apply(this, arguments);
    },
    /**
     * Renders the data points on the map.
     *
     * @private
     */
    _renderDataPoints: function () {
        _.invoke(this.markers, 'remove');
        _.each(this.state, point => {
            const marker = L.marker([point[this.latitudeField], point[this.longitudeField]])
                .addTo(this.leafletMap)
                .bindPopup(this.qweb.render('map-popup', {record: point}));
            marker.on('click', () => {
                this.trigger_up('record_clicked', {id: point.id});
            });
            this.markers.push(marker);
        });
    },
});

return MapRenderer;

});
