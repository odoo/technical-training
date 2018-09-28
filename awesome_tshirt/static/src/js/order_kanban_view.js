odoo.define('awesome_tshirt.order_kanban_view', function (require) {
"use strict";

const core = require('web.core');
const KanbanController = require('web.KanbanController');
const KanbanView = require('web.KanbanView');
const view_registry = require('web.view_registry');

const _lt = core._lt;
const QWeb = core.qweb;


const OrderKanbanController = KanbanController.extend({
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
        return Promise.all([
            this._super.apply(this, arguments),
            this._loadCustomers()
        ]);
    },
    /**
     * @override
     */
    start: function () {
        this.$el.addClass('o_order_kanban_view');
        this.$('.o_content').prepend(QWeb.render('OrderKanban.CustomerSidebar', {
            activeCustomerID: this.activeCustomerID,
            customers: this.customers,
        }));
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
            params.domain = params.domain || [];
            params.domain.push(['customer_id', '=', this.activeCustomerID]);
        }
        return Promise.all([
            this._super(params),
            this._loadCustomers()
        ]);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     * @returns {Promise}
     */
    _loadCustomers: function () {
        return this._rpc({
            route: '/web/dataset/search_read',
            model: 'res.partner',
            fields: ['display_name'],
            domain: [['has_active_order', '=', true]],
        }).then((result) => {
            this.customers = result.records;
        });
    },
    /**
     * @override
     */
    _update: function () {
        return this._super.apply(this, arguments).then(() => this._updateCustomerList());
    },
    /**
     * Updates the customer list according to the currnet search and active id
     *
     * @private
     */
    _updateCustomerList: function () {
        var searchVal = this.$('.o_customer_search').val();
        var matches = fuzzy.filter(searchVal, _.pluck(this.customers, 'display_name'));
        var indexes = _.pluck(matches, 'index');
        var customers = _.map(indexes, (index) => this.customers[index]);
        this.$('.o_customer_list').replaceWith(QWeb.render('OrderKanban.CustomerList', {
            activeCustomerID: this.activeCustomerID,
            customers: customers,
        }));
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
        this._updateCustomerList();
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
