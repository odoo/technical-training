odoo.define('awesome_tshirt.order_kanban_view', function (require) {
"use strict";

var core = require('web.core');
var KanbanController = require('web.KanbanController');
var KanbanView = require('web.KanbanView');
var view_registry = require('web.view_registry');

var _lt = core._lt;
var QWeb = core.qweb;


var OrderKanbanController = KanbanController.extend({
    events: _.extend({}, KanbanController.prototype.events, {
        'click .o_customer': '_onCustomerClicked',
        'input .o_customer_search': '_onCustomerSearchInput',
    }),

    /**
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        this.activeCustomerID = false;
    },
    /**
     * @override
     */
    willStart: function () {
        var superDef = this._super.apply(this, arguments);
        var customerDef = this._loadCustomers();
        return $.when(superDef, customerDef);
    },
    /**
     * @override
     */
    start: function () {
        this.$el.addClass('o_order_kanban_view');
        return this._super.apply(this, arguments);
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
        var superDefs = this._super(params);
        var customerDef = this._loadCustomers();
        return $.when(superDefs, customerDef);
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
            domain: [['has_active_order', '=', true]],
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
            self.$('.o_kanban_view').prepend(QWeb.render('OrderKanban.CustomerSidebar', {
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
    /**
     * @private
     */
    _onCustomerSearchInput: function () {
        var self = this;
        var searchVal = this.$('.o_customer_search').val();
        var matches = fuzzy.filter(searchVal, _.pluck(this.customers, 'display_name'));
        var indexes = _.pluck(matches, 'index');
        var customers = _.map(indexes, function (index) {
            return self.customers[index];
        });
        this.$('.o_customer_list').replaceWith(QWeb.render('OrderKanban.CustomerList', {
            activeCustomerID: this.activeCustomerID,
            customers: customers,
        }));
    },
});

var OrderKanbanView = KanbanView.extend({
    config: _.extend({}, KanbanView.prototype.config, {
        Controller: OrderKanbanController,
    }),
    display_name: _lt('Order Kanban'),
    icon: 'fa-th-list',
});

view_registry.add('order_kanban_view', OrderKanbanView);

});
