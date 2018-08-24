# -*- coding: utf-8 -*-
# Copyright 2018 Naglis Jonaitis
# License AGPL-3 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, api, http, registry
from werkzeug.exceptions import BadRequest, NotFound

from ..const import OP_WEBHOOK_EVENTS
from ..exceptions import OpenProjectWebhookDataError

_logger = logging.getLogger(__name__)


class WebhookController(http.Controller):

    @http.route([
        '/openproject/webhook/<string:db>/<int:backend_id>',
    ], type='json', auth='none', csrf=False)
    def webhook_endpoint(self, db, backend_id):
        if not http.db_filter([db]):
            raise NotFound()

        with registry(db).cursor() as cr:
            sudo_env = api.Environment(cr, SUPERUSER_ID, {})
            backend = sudo_env['openproject.backend'].browse(backend_id)

            if not (backend.exists() and backend.active):
                _logger.warning(
                    u'OpenProject backend with ID: %s does not exist or is '
                    u'deactivated', backend_id)
                raise NotFound()

            data = dict(http.request.jsonrequest)
            event = data.get('action')
            if not (event and event in OP_WEBHOOK_EVENTS):
                _logger.warning(
                    u'Webhook event action is missing or is not supported '
                    u'(value: %s)', event)
                raise BadRequest()

            try:
                backend._handle_webhook(event, data, delay=True)
            except OpenProjectWebhookDataError as e:
                _logger.warning(u'Invalid webhook data: %s', e)
                raise BadRequest()
            else:
                return 'OK'
