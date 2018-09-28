# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import random

from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        """
        Overrides to add the custom home menu message to the page source, to
        prevent from doing an extra RPC at webclient startup
        """
        result = super(IrHttp, self).session_info()
        if random.random() > 0.5:
            result['home_menu_message'] = "Bafien is watching you"
        else:
            result['home_menu_message'] = "Bafien is totally sane. Also, please work harder."
        return result
