# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP S.A. <http://www.odoo.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import openerplib
import datetime

if __name__ == '__main__':
    connection = openerplib.get_connection(hostname="localhost",
                                               port=8069,
                                               database="10ex2",
                                               login="admin",
                                               password="admin",
                                               protocol="jsonrpc")
    connection.check_login(force=False)
    
    aj_model = connection.get_model('account.journal')
    aj = aj_model.search([('name', '=', 'Miscellaneous Operations')])
    
    acc_model = connection.get_model('account.account')
    acc = acc_model.search([('code', 'in', ['440000', '400000'])])
    
    am_model = connection.get_model('account.move')
    for i in range(1,1000):
        start_date = datetime.datetime.now()
        am_model.create({
            'journal_id': aj[0],
            'line_ids': [
                (0, 0, {
                    'account_id': acc[0],
                    'name': 'line 1',
                    'debit': 100,
                    'company_id': 1,
                }),
                (0, 0, {
                    'account_id': acc[1],
                    'name': 'line 1',
                    'credit': 100,
                    'company_id': 1,
                }),
            ],
        })
        diff = datetime.datetime.now()-start_date
        print "time taken : %s,%s" % (diff.seconds, diff.microseconds / 1000 )
