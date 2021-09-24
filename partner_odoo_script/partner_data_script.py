# if use https get error SSLError: [SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1131)
url = 'http://127.0.0.1:4545'
db = 'partner_script_test'
username = 'admin'
password = 'admin'

import xmlrpc.client  # import to user xmlrpc API
import csv  # Imported to read csv files
from datetime import datetime
import os

common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % url)  # for authentication
version = common.version()  # to check if connection is correct before authentication
uid = common.authenticate(db, username, password, {})  # Used as parameter while calling methods
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))  # Used as parameter while calling method

start_time = datetime.now()

with open('/home/admin123/Aarti/workspace/custom_addons/partner_odoo_script/res.partner.csv', newline='') as csv_file:
    csv_file = csv.DictReader(csv_file)
    print("===csv_filee", csv_file)

    '''We use this variable for us while executing csv or excel file in xmlrc
    to know how many records are updated or inserted or if
    scripts stops its execution due to any reasons at that time we can get the
    row number of xls or csv file at which row script stops its execution.'''

    excel_row = 2
    print('\n csv>>>>file>>>>>>>>', csv_file)

    partner_count = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[]])
    print("partner_count::::::::::::::", partner_count)

    for row in csv_file:
        rec = dict(row)
        print("Rec -------------------", rec)
        if excel_row >= 2:
            # We used strip() method to remove white spaces from the record.

            # partner
            partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search',
                                           [[['email', '=', rec['email'].strip()]]])
            print("====partner id brder val==", partner_id)

            # country_id
            country_id = models.execute_kw(db, uid, password, 'res.country', 'search',
                                           [[['name', '=', rec['country_id'].strip()]]])
            print("====country_id==", country_id)
            print("====country_id==", type(country_id))

            # company_id
            company_id = models.execute_kw(db, uid, password, 'res.company', 'search',
                                           [[['name', '=', rec['company_id'].strip()]]])
            print("====company_id==", company_id)
            print("====company_id==", type(company_id))

            vals = {
                'name': rec['name'].strip(),
                'phone': rec['phone'].strip(),
                'email': rec['email'].strip(),
                'city': rec['city'].strip(),
                'country_id':country_id[0],
                # 'company_id':company_id[0],
            }
            if not partner_id and not country_id:
                print("====in if partner===")
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [vals])
            else:
                print('==else== partner==')
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'write',
                                               [[partner_id[0],[country_id[0]]], vals])
                # if company_id[0]:
                #     print("=====in if compnay id===")
                #     partner_id = models.execute_kw(db, uid, password, 'res.partner', 'write',
                #                                    [[partner_id[0], [country_id[0], [company_id[0]]]], vals])
                # else:
                #     print("====in not compnay id===")
                #     partner_id = models.execute_kw(db, uid, password, 'res.partner', 'write',
                #                                    [[partner_id[0], [country_id[0]]], vals])

            if rec['city'] == 'Berlin':
                print("=Berlin=====")
                remove_partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search',
                                                      [[['city', '=', 'Berlin']]])
                print("====remove partner jhdhhfd==", remove_partner_id)

                models.execute_kw(db, uid, password, 'res.partner', 'unlink',
                                  [[partner for partner in remove_partner_id]])
                print(":::::::::remove::::::")
            print("\n\n:::::::::excel_row:::::::::::::::", excel_row)

            # Example of read method to fetch specific field like emails and name of partner
            # Read method default returns Id field.
            # partner_details = models.execute_kw(db, uid, password, 'res.partner', 'read',[partner_id[0]],{'fields':['name', 'email']})
            # print("partner_detail-------------", partner_details)

        excel_row += 1

# Below print statements are used to get the start and end timings of the script execution.
print(":::::::::::::start::::::::::", start_time)
print("::::::End Time:::::::::", datetime.now())
