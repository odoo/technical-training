odoo.define('openacademy.portal_user_dashboard', function (require) {
    'use strict';

    var core = require('web.core');
    var Model = require('web.DataModel');
    var formats = require('web.formats');
    var Widget = require('web.Widget');

    var _t = core._t;
    var QWeb = core.qweb;

    var portal_user_dashboard = Widget.extend({
        'events': {
            'click .o_session_details_link': 'open_session',
            'keyup textarea': 'toggle_send_button',
            'click .o_send_feedback': 'send_feedback'
        },
        init: function (parent) {
            this._super(parent);
            this.academy_session = new Model('openacademy.session');
            this.session_feedback = new Model('openacademy.feedback');
        },
        start: function() {
            var self = this;
            return this._super().then(function() {
                self.render_dashboard();
            });
        },
        willStart: function () {
            var self = this;
            return this._super().then(function () {
                return $.when(self.fetch_data());
            });
        },
        fetch_data: function () {
            var self = this;
            return this.academy_session.query(
                [/** List of session's fields that are needed **/]
            )
            .filter(/** Domain **/)         // Note that all widgets are linked to a session object which contains
                                            // metadata like connected user and its partner ID, etc.
            .all()
            .done(function (sessions) {
                _(sessions).each(function (session) {
                    /**
                     * Check if there is already a feedback done, and mark session
                     * accordingly.
                     *
                     * Also, format start and end dates to be displayed as the user
                     * expects
                     */
                });
                self.sessions = sessions;
                self.waiting_feedback_sessions = _(sessions).filter(function (session) {
                    /**
                     * The widget should only display sessions that don't have
                     * feedback from the user
                     */
                });
            });
        },
        render_dashboard: function () {
            this.$el.empty();
            /**
             * Render widget's template and add it to the DOM. Once done, we can cache important
             * elements like the feedback textarea and the send button
             */
        },
        open_session: function (ev) {
            /**
             * Tell the widget to open session's form view
             */
        },
        toggle_send_button: function () {
            /**
             * Change send button's disabled property depending on textarea content,
             * if empty disallow clicking it
             */
        },
        send_feedback: function (ev) {
            var self = this;

            /**
             * Get session ID from the DOM element and textarea value, in order to create
             * a new session feedback record
             */

            this.session_feedback.call('create', [
                {
                    /**
                     * Pass a dictionary where keys are field names, and the values
                     * correspond to those fields values
                     */
                }
            ]).done(function (result) {
                /**
                 * We need to update the list of waiting feedback sessions, removing the
                 * current one.
                 */
                self.render_dashboard();
            });
        },
    });

    core.action_registry.add('openacademy.portal_user_dashboard', portal_user_dashboard);

});
