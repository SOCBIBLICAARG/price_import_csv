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


class catalogo_import(osv.osv_memory):
    _name = 'catalogo.import'
    _description = 'Importa precios'

    _columns = {
	'filename_catalogo': fields.binary(string='Catalogo Filename'),
        'first_row_column': fields.boolean('1st Row Column Names'),
    }

    _defaults = {
	'first_row_column': True,
	}

    def catalogo_import(self, cr, uid, ids, context=None):

	res = self.read(cr,uid,ids,['filename_catalogo'])
	filename_catalogo = res[0]['filename_catalogo']
	res_first_row = self.read(cr,uid,ids,['first_row_column'])
	first_row = res_first_row[0]['first_row_column']

	if not filename_catalogo:
		raise osv.except_osv(_('Error!'), _("Debe ingresar un archivo a importar!!!"))
		return {'type': 'ir.actions.act_window_close'}

	file=base64.decodestring(filename_catalogo)
	lines=file.split('\n')

	index = 1
	list_products = []	
	for line in lines:
		if ((index > 1 and first_row) or (index > 0 and not first_row)):
			cadena = line.split(',')
			if len(cadena)==2:
				isbn = cadena[0]
				new_price = float(cadena[1])
		
				product_id = self.pool.get('product.product').search(cr,uid,[('sba_code','=',isbn)])	
				if not product_id:
					raise osv.except_osv(_('Error!'), _("Linea "+str(index)+" .No se encuentra el producto "+isbn))
				if isinstance(product_id,list):
					product_id = product_id[0]
				vals_product = {
					'list_price': new_price,
					}
				return_id = self.pool.get('product.product').write(cr,uid,product_id,vals_product)
		index += 1

		
        return {}

catalogo_import()

