odoo.define('awesome_tshirt.OrderKanbanViewTests', function (require) {
"use strict";

require('awesome_tshirt.order_kanban_view');

const testUtils = require('web.test_utils');
const viewRegistry = require('web.view_registry');

const createView = testUtils.createView;
const OrderKanbanView = viewRegistry.get('order_kanban_view');

QUnit.module('awesome_tshirt', function () {

    QUnit.module('Custom Kanban View', {
        beforeEach: function () {
            this.data = {};
            this.data['awesome_tshirt.order'] = {
                fields: {
                    customer_id: {string: 'Customer', type: 'many2one', relation: 'res.partner'},
                    quantity: {string: 'Quantity', type: 'integer'},
                    size: {string: 'Size', type: 'selection', selection: [["s", "S"], ["m", "M"], ["l", "L"], ["xl", "XL"]]},
                },
                records: [{
                    customer_id: 1,
                    quantity: 3,
                    size: 'm',
                }, {
                    customer_id: 1,
                    quantity: 2,
                    size: 'xl',
                }, {
                    customer_id: 2,
                    quantity: 1,
                    size: 's',
                }],
            };
            this.data['res.partner'] = {
                fields: {
                    has_active_order: {string: 'Has active order', type: 'boolean'},
                },
                records: [{
                    id: 1,
                    display_name: 'Partner 1',
                    has_active_order: true,
                }, {
                    id: 2,
                    display_name: 'Partner 2',
                    has_active_order: true,
                }, {
                    id: 3,
                    display_name: 'Partner 3',
                    has_active_order: false,
                }],
            };
            this.arch = `
                <kanban>
                    <templates>
                        <t t-name="kanban-box">
                            <div>
                                <div><field name="customer_id"/></div>
                                <div><field name="quantity"/></div>
                                <div><field name="size"/></div>
                            </div>
                        </t>
                    </templates>
                </kanban>
            `;
        },
    });

    QUnit.test('basic rendering', async function (assert) {
        assert.expect(7);

        const kanban = await createView({
            View: OrderKanbanView,
            model: 'awesome_tshirt.order',
            data: this.data,
            arch: this.arch,
            mockRPC: function (route, args) {
                assert.step(args.model + ':' + route);
                return this._super.apply(this, arguments);
            },
        });

        assert.containsOnce(kanban, '.o_customer_sidebar .o_customer_search');
        assert.containsOnce(kanban, '.o_customer_sidebar .o_customer_list');
        assert.containsN(kanban, '.o_customer_list .o_customer', 2);
        assert.containsN(kanban, '.o_kanban_record:not(.o_kanban_ghost)', 3);

        assert.verifySteps([
            'awesome_tshirt.order:/web/dataset/search_read',
            'res.partner:/web/dataset/search_read'
        ]);

        kanban.destroy();
    });

    QUnit.test('filtering customer list', async function (assert) {
        assert.expect(6);

        const kanban = await createView({
            View: OrderKanbanView,
            model: 'awesome_tshirt.order',
            data: this.data,
            arch: this.arch,
            mockRPC: function (route, args) {
                assert.step(args.model + ':' + route);
                return this._super.apply(this, arguments);
            },
        });

        assert.containsN(kanban, '.o_customer_list .o_customer', 2);

        await testUtils.fields.editInput(kanban.$('.o_customer_search'), 'P1');

        assert.containsOnce(kanban, '.o_customer_list .o_customer');
        assert.strictEqual(kanban.$('.o_customer_list .o_customer').text().trim(), 'Partner 1');

        assert.verifySteps([
            'awesome_tshirt.order:/web/dataset/search_read',
            'res.partner:/web/dataset/search_read'
        ]);

        kanban.destroy();
    });

    QUnit.test('use customer list to refine search', async function (assert) {
        assert.expect(7);

        const kanban = await createView({
            View: OrderKanbanView,
            model: 'awesome_tshirt.order',
            data: this.data,
            arch: this.arch,
            mockRPC: function (route, args) {
                assert.step(args.model + ':' + route);
                return this._super.apply(this, arguments);
            },
        });

        assert.containsN(kanban, '.o_kanban_record:not(.o_kanban_ghost)', 3);

        await testUtils.dom.click(kanban.$('.o_customer_list .o_customer:first'));

        assert.containsN(kanban, '.o_kanban_record:not(.o_kanban_ghost)', 2);

        assert.verifySteps([
            'awesome_tshirt.order:/web/dataset/search_read',
            'res.partner:/web/dataset/search_read',
            'res.partner:/web/dataset/search_read',
            'awesome_tshirt.order:/web/dataset/search_read'
        ]);

        kanban.destroy();
    });
});

});
