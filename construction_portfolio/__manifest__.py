# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
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
    'author':  'Dennis Boy Silva - (Agilis Enterprise Solutions Inc.)',
    'website': 'agilis.com.ph',
    'license': 'AGPL-3',
    'category': 'Project',
    'data': [
            # 'security/ir.model.access.csv',
            # 'wizard/do_purchase_requisition.xml',
            # 'wizard/do_create_po.xml',
            'views/project.xml',
            # 'views/invoice.xml',
            # 'views/purchase.xml',
            # 'views/stock.xml',
        ],
    'depends': [
            'project',
            'basic_construction_suite',
            'construction_project_management_base',
        ],
    'description': '''
Construction Project Porfolio Management''',
    'installable': True,
    'auto_install': False,
    'name': "Construction Porfolio",
    'summary': 'Construction Project Porfolio Management',
    'test': [],
    'version': '12.0.0'

}
