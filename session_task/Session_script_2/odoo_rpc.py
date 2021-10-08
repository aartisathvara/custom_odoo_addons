import odoorpc
from datetime import datetime

odoo = odoorpc.ODOO('127.0.0.1', port=8080)
odoo.login('partner_script', 'admin', 'admin')
print("odoo version--------", odoo.version)
# http://127.0.0.1:7014/web/login

product_id = odoo.env['product.product'].search([('type','=','product'),
    ('tracking','=','none')])
location_id = odoo.env['stock.location'].search([('name','=','Stock')])

# Module = odoo.env['ir.module.module']
# module_id = Module.search([('name', '=', 'purchase')])
# Module.button_immediate_install(module_id)

inventory_id = odoo.env['stock.inventory'].create([{'name':'NEW inventory'}])
inventory = odoo.env['stock.inventory'].browse(inventory_id)
print(':::::;inventory_id:::::::::', inventory.id)
print(':::::;product_id:::::::::', product_id)
print(':::::;location_id:::::::::', location_id)

inventory.action_start()

start_date = datetime.now()
for product in product_id:

    print('\n======product::', product)
    line_id = odoo.env['stock.inventory.line'].search([
        ('inventory_id','=',inventory.id),('product_id','=',product)])

    vals = {
        'product_qty':100,
        'location_id':location_id[1],
    }
    if line_id:
        inv_line_id = odoo.env['stock.inventory.line'].browse(line_id)
        print("::::inv_line_id::::", inv_line_id)
        inv_line_id.write(vals)
    else:
        print("\n\n\n\n Vals :::::::::::::::", vals)
        vals.update({
            'inventory_id':inventory_id[0],
            'product_id':product
            })
        line_id = odoo.env['stock.inventory.line'].create([vals])
        print("\n\n created line_id:::::::::::", line_id)
print("\n\n end of the script")
inventory.action_validate()
print(":::::::::::start_date:::::::::::", start_date)
print(":::::::::::end_date:::::::::::", datetime.now())

