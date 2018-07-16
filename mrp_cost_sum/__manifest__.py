# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2017 Marlon Falcón Hernandez
#    (<http://www.falconsolutions.cl>).
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

{
    'name': 'Sumatoria de Costos en Producción MFH',
    'version': '10.0.0.1.0',
    'author': "Falcon Solutions SpA",
    'maintainer': 'Falcon Solutions SpA',
    'website': 'http://www.falconsolutions.cl',
    'license': 'AGPL-3',
    'category': 'MRP',
    'summary': 'Sumatoria de Costos en Producción',
    'description': """
Sumatoria de Costos en Producción MFH
======================================================================================
1-. Sumar costos de insumos de producto terminado \n
2-. Modificar el asiento contable del movimiento de inventario de producto terminado
""",
    'depends': ['mrp','stock_account'],
    'data': [
        #~ 'security/ir.model.access.csv',
        'views/mrp_workcenter_view.xml',
        'views/mrp_production_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'demo': [],
    'test': [],
}
