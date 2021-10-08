import odoorpc
from datetime import datetime
import csv

odoo = odoorpc.ODOO('127.0.0.1', port=8080)
odoo.login('product_script', 'admin', 'admin')

start_time = datetime.now()

with open('/home/admin123/Downloads/Session_script_1/product_template.csv', newline='') as csv_file:
    csv_file = csv.DictReader(csv_file)

    '''We use this variable for us while executing csv or excel file in xmlrc
    to know how many records are updated or inserted or if
    scripts stops its execution due to any reasons at that time we can get the
    row number of xls or csv file at which row script stops its execution.'''

    excel_row = 2

    # To count existing product's count
    product_count = odoo.env['product.template'].search_count([])
    print("product_count::::::::::::::", product_count)

    for row in csv_file:
        rec = dict(row)
        print("Rec -------------------", rec)
        if excel_row >= 2:
            # We used strip() method to remove white spaces from the record.
            product_tmplate_id = odoo.env['product.template'].search([('default_code','=',rec['default_code'])])
            product_tmpl_id = odoo.env['product.template'].browse(product_tmplate_id)
            vals = {
                'name':rec['name'].strip(),
                'default_code':rec['default_code'].strip(),
                'list_price':rec['list_price'].strip(),
                'standard_price':rec['standard_price'].strip(),
            }
            if not product_tmpl_id:
                product_tmpl_id = odoo.env['product.template'].create([vals])
            else:
                product_tmpl_id.write(vals)
            print("\n\n:::::::::excel_row:::::::::::::::", excel_row)


        excel_row += 1

# Below print statements are used to get the start and end timings of the script execution.
print(":::::::::::::start::::::::::",start_time)
print("::::::End Time:::::::::", datetime.now())
