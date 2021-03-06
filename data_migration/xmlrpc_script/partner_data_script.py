url = 'http://127.0.0.1:8014'
db = 'v14_contacts_script'
username = 'admin'
password = 'admin'

import xmlrpc.client
import csv
from datetime import datetime

common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % url)
version = common.version()
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

start_time = datetime.now()
with open('/home/odoo/workspace/custom-addons/data_migration/xmlrpc_script/res.partner.csv', newline='') as csv_file:
    csv_file = csv.DictReader(csv_file)
    excel_row = 2
    for row in csv_file:
        rec = dict(row)
        if excel_row >= 2:
            partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search',
                                           [[['email', '=', rec['email'].strip()]]])
            vals = {
                'name': rec['name'].strip(),
                'phone': rec['phone'].strip(),
                'email': rec['email'].strip(),
                'city': rec['city'].strip(),
            }

            if partner_id:
                if rec['company_id'] == 'My Company (San Francisco)':
                    print("Country ::::::::", rec['country_id'].strip())
                    country_id = models.execute_kw(db, uid, password, 'res.country', 'search',
                                                   [[['name', '=', 'United State']]])
                    print("\n\n country_id ::::::::::", country_id)
                    if country_id:
                        vals.update({
                            'country_id':233
                        })

            if not partner_id:
                print("=====in if partner===",partner_id)
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [vals])
            else:
                print("=====in else partner===",partner_id)
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'write',
                                                [[partner_id[0]], vals])
            if rec['country_id'] == 'Berlin':
                models.execute_kw(db, uid, password, 'res.partner', 'unlink',[[partner_id[0]]])
            print("\n excel row:::::::", excel_row)
            print("vals ::::::::::::", vals)
            excel_row += 1

"""count of partners"""
count_partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search_count',[[]])
print("====count_partner_id==", count_partner_id)

print(":::::::::::::start::::::::::", start_time)
print("::::::End Time:::::::::", datetime.now())
