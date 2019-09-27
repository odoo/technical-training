odoo.define('awesome_tshirt.MyCounterTests', function (require) {
"use strict";

const MyCounter = require('awesome_tshirt.MyCounter');

const testUtils = require('web.test_utils');

QUnit.module('awesome_tshirt', function () {

    QUnit.module('MyCounter');

    QUnit.test('basic test', async function (assert) {
        assert.expect(3);

        const myCounter = new MyCounter();
        await myCounter.appendTo($('#qunit-fixture'));

        assert.strictEqual(myCounter.$el.text().trim(), '0');

        await testUtils.dom.click(myCounter.$('.o_increment'));
        await testUtils.dom.click(myCounter.$('.o_increment'));

        assert.strictEqual(myCounter.$el.text().trim(), '2');

        await testUtils.dom.click(myCounter.$('.o_decrement'));

        assert.strictEqual(myCounter.$el.text().trim(), '1');

        myCounter.destroy();
    });
});

});
