import psycopg2
from psycopg2.extras import NamedTupleCursor

source_connection = psycopg2.connect(user='postgres',
                                     password='odoo',
                                     host='localhost',
                                     port='5432',
                                     database='adrie_sourc_db')
print(source_connection)

dest_connection = psycopg2.connect(user='postgres',
                                   password='odoo',
                                   host='localhost',
                                   port='5432',
                                   database='adrie_dest_db2')
print(dest_connection)


sorce_cursor = source_connection.cursor(cursor_factory=NamedTupleCursor)
dest_cursor = dest_connection.cursor(cursor_factory=NamedTupleCursor)

company_dict = {
    3: 3,
    7: 7,
    8: 8,
    6: 6,
    9: 9,
    10: 10,
}


class ImportProductProduct:


    def fetch_record_from_dest_db(self, model_id, model_name):
        query = "select * from " + model_name + " where v12_old_id = %s" % model_id
        dest_cursor.execute(query)
        data = dest_cursor.fetchall()
        if data:
            return data[0].id
        return False

    def create_product(self, product_data, product_tmpl_id):
        if product_data.barcode:
            insert_query = """Insert into product_product (create_date, weight, default_code,
            product_tmpl_id,barcode, volume,write_date,active,
            mps_forecasted,mps_min_supply,mps_max_supply, v12_old_id) values (
            '%s',%s,'%s',%s,'%s','%s','%s','%s','%s','%s','%s',%s
            )""" % (
                product_data.create_date,
                product_data.weight or 'null',
                product_data.default_code or '',
                product_tmpl_id,
                product_data.barcode or '',
                product_data.volume or 0,
                product_data.write_date,
                product_data.active,
                product_data.mps_forecasted or 0,
                product_data.mps_min_supply or 0,
                product_data.mps_max_supply or 0,
                product_data.id
            )
            dest_cursor.execute(insert_query)
            dest_connection.commit()
        else:

            insert_query = """Insert into product_product (create_date, weight, default_code,
            product_tmpl_id, volume,write_date,active,
            mps_forecasted,mps_min_supply,mps_max_supply, v12_old_id) values (
            '%s',%s,'%s',%s,'%s','%s','%s','%s','%s','%s',%s
            )""" % (
                product_data.create_date,
                product_data.weight or 'null',
                product_data.default_code or '',
                product_tmpl_id,
                product_data.volume or 0,
                product_data.write_date,
                product_data.active,
                product_data.mps_forecasted or 0,
                product_data.mps_min_supply or 0,
                product_data.mps_max_supply or 0,
                product_data.id
            )
            dest_cursor.execute(insert_query)
            dest_connection.commit()


    def fetch_product(self):

        source_product_query = """select * from product_product where product_tmpl_id in (select id from product_template where company_id in (3,6,7,8,9,10) or company_id is null or 
        active in ('False','True'))"""
        sorce_cursor.execute(source_product_query)
        source_product_data = sorce_cursor.fetchall()

        print("source_product_data", len(source_product_data))

        for product in source_product_data:

            product_id = self.fetch_record_from_dest_db(
                product.id, "product_product")
            product_tmpl_id = self.fetch_record_from_dest_db(
                product.product_tmpl_id, "product_template")

            if not product_id:

                # Checks default code in destination db if exists then update
                # v12_old_id
                product_default_code_id = ''
                product_barcode_id = ''

                source_product_default_code_query = """select * from product_product where default_code = '%s'""" % product.default_code
                dest_cursor.execute(source_product_default_code_query)
                product_default_code = dest_cursor.fetchall()
                if product_default_code:
                    product_default_code_id = product_default_code[0].id

                if product_default_code_id:
                    print("writing default_code v12_old_id")

                    update_query = "update product_product set v12_old_id = %s where id = %s" % (
                        product.id, product_default_code_id)
                    dest_cursor.execute(update_query)
                    dest_connection.commit()

                source_product_barcode_query = """select * from product_product where barcode = '%s'""" % product.barcode
                dest_cursor.execute(source_product_barcode_query)
                product_barcode = dest_cursor.fetchall()
                if product_barcode:
                    print("writing v12_old_id")
                    product_barcode_id = product_barcode[0].id

                if product_barcode_id:

                    barcode_update_query = "update product_product set v12_old_id = %s where id = %s" % (
                        product.id, product_barcode_id)
                    dest_cursor.execute(barcode_update_query)
                    dest_connection.commit()

                if not product_barcode_id and not product_default_code_id and product_tmpl_id:

                    self.create_product(product, product_tmpl_id)


x = ImportProductProduct()
x.fetch_product()
print("finish")
