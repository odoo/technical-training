odoo.define('library.client_action', function (require) {
"use strict";

var ChartWidget = require('library.ChartWidget');
var ControlPanelMixin = require('web.ControlPanelMixin');

var core = require('web.core');
var Widget = require('web.Widget');

var QWeb = core.qweb;


var ClientAction = Widget.extend(ControlPanelMixin, {
    template: 'LibraryDashboard',
    custom_events: {
        'open_books': '_onOpenBooks',
    },

    /**
     * @override
     */
    init: function (parent, action) {
        this._super.apply(this, arguments);
        this.action_manager = parent;
        this.action = action;
    },
    /**
     * @override
     */
    willStart: function () {
        var self = this;
        var def1 = this._rpc({route: '/library/statistics'}).then(function (stats) {
            self.stats = stats;
        });
        var def2 = this._super.apply(this, arguments);
        return $.when(def1, def2);
    },
    /**
     * @override
     */
    start: function () {
        this._renderButtons();
        this._updateControlPanel();
        var def1 = this._renderChart();
        var def2 = this._super.apply(this, arguments);
        return $.when(def1, def2);
    },
    /**
     * Called when coming back with the breadcrumbs
     *
     * @override
     */
    do_show: function () {
        this._super.apply(this, arguments);
        this._renderChart();
        this._updateControlPanel();
        this.action_manager.do_push_state({action: this.action.id});
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _renderButtons: function () {
        this.$buttons = $(QWeb.render('LibraryDashboard.Buttons'));
        this.$buttons.on('click', '.o_bad_customers', this._onOpenBadCustomers.bind(this));
        this.$buttons.on('click', '.o_lost_books', this._onOpenLostBooks.bind(this));
    },
    /**
     * @private
     */
    _renderChart: function () {
        var chartData = {
            nb_available_books: this.stats.nb_available_books,
            nb_rented_books: this.stats.nb_rented_books,
            nb_lost_books: this.stats.nb_lost_books,
        };
        var chart = new ChartWidget(this, chartData);
        this.$('.o_fancy_chart').empty();
        return chart.appendTo(this.$('.o_fancy_chart'));
    },
    /**
     * @private
     */
    _updateControlPanel: function () {
        this.update_control_panel({
            breadcrumbs: this.action_manager.get_breadcrumbs(),
            cp_content: {
                $buttons: this.$buttons,
            },
        });
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onOpenBadCustomers: function () {
        this.do_action('library.action_bad_customer');
    },
    /**
     * @param {OdooEvent} ev
     * @private
     */
    _onOpenBooks: function (ev) {
        var state = ev.data.state;
        var action;
        if (state === 'available') {
            action = 'library.action_available_books';
        } else if (state === 'lost') {
            action = 'library.action_lost_books';
        } else if (state === 'rented') {
            action = 'library.action_rented_books';
        } else {
            this._do_warn('Wrong state');
        }
        this.do_action(action);
    },
    /**
     * @private
     */
    _onOpenLostBooks: function () {
        this.do_action('library.action_lost_books');
    },
});

core.action_registry.add('library.dashboard', ClientAction);

});
