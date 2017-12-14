odoo.define('library.LibraryKanbanView', function (require) {
"use strict";

var core = require('web.core');
var KanbanController = require('web.KanbanController');
var KanbanModel = require('web.KanbanModel');
var KanbanRenderer = require('web.KanbanRenderer');
var KanbanView = require('web.KanbanView');
var view_registry = require('web.view_registry');

var _lt = core._lt;
var QWeb = core.qweb;


var LibraryKanbanController = KanbanController.extend({
    events: {
        'click .o_customer': '_onCustomerClicked',
    },

    /**
     * @override
     */
    willStart: function () {
        var def1 = this._super.apply(this, arguments);
        var def2 = this._loadCustomers();
        return $.when(def1, def2);
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    reload: function (params) {
        if (this.activeCustomerID) {
            params = params || {};
            params.domain = [['customer_id', '=', this.activeCustomerID]];
        }
        var def1 = this._super(params);
        var def2 = this._loadCustomers();
        return $.when(def1, def2);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     * @returns {Deferred}
     */
    _loadCustomers: function () {
        var self = this;
        return this._rpc({
            route: '/web/dataset/search_read',
            model: 'res.partner',
            fields: ['display_name'],
            limit: 80,
        }).then(function (result) {
            self.customers = result.records;
        });
    },
    /**
     * @override
     */
    _update: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            self.$('.o_kanban_view').prepend(QWeb.render('CustomerList', {
                activeCustomerID: self.activeCustomerID,
                customers: self.customers,
            }));
        });
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onCustomerClicked: function (ev) {
        this.activeCustomerID = $(ev.currentTarget).data('id');
        this.reload();
    },
});

var LibraryKanbanView = KanbanView.extend({
    config: _.extend({}, KanbanView.prototype.config, {
        Model: KanbanModel,
        Renderer: KanbanRenderer,
        Controller: LibraryKanbanController,
    }),
    display_name: _lt('Library Kanban'),
    icon: 'fa-th-list',
});

view_registry.add('library_kanban', LibraryKanbanView);

});
