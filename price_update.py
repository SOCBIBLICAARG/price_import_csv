# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import date
from openerp import netsvc
import base64


class price_update(osv.osv_memory):
    _name = 'price.update'
    _description = 'Actualiza precios'

    _columns = {
        'familia': fields.many2one('product.familia','Familia'),
        'categoria': fields.many2one('product.categoria','Categoria'),
        'porcentual': fields.float('Porcentual'),
    }

    def price_update(self, cr, uid, ids, context=None):

	res = self.read(cr,uid,ids,['familia','categoria','porcentual'])
	porcentual = float(res[0]['porcentual'])
	familia = categoria = False
	if res[0].has_key('familia'):
		if res[0]['familia']:
			familia = res[0]['familia'][0]
	if res[0].has_key('categoria'):
		if res[0]['categoria']:
			categoria = res[0]['categoria'][0]

	if not porcentual:
		raise osv.except_osv(_('Error!'), _("Debe ingresar un archivo a importar!!!"))
		return {'type': 'ir.actions.act_window_close'}

	product_ids = []
	if familia and not categoria:
		product_ids = self.pool.get('product.product').search(cr,uid,[('familia','=',familia)])
	else:
		if categoria and not familia:
			product_ids = self.pool.get('product.product').search(cr,uid,[('categoria','=',categoria)])
		else:
			if familia and categoria:
				product_ids = self.pool.get('product.product').search(cr,uid,[('categoria','=',categoria),('familia','=',familia)])

	for product in self.pool.get('product.product').browse(cr,uid,product_ids):
		new_price = product.list_price * (1+(porcentual/100))
		vals_product = {
			'list_price': new_price
			}
		return_id = self.pool.get('product.product').write(cr,uid,product.id,vals_product)
		
        return {}

price_update()

