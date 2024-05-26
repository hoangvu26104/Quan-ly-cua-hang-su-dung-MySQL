import mysql.connector
from modules.product import KitchenEquipment
from modules.product import HouseholdAppliances
class Warehouse:
    def __init__(self):
        self.products = []
        self.connection = mysql.connector.connect(
            host="monorail.proxy.rlwy.net",
            user="root",
            password="xIbazQgoTOmqlVFBFVpELtNnscUXRTfq",
            database="railway",
            port="45681"
        )
        self.cursor = self.connection.cursor()

    def add_product(self, product):
        if isinstance(product, KitchenEquipment):
            sql = "INSERT INTO products (product_id, name, price, quantity, wattage) VALUES (%s, %s, %s, %s, %s)"
            values = (product.product_id, product.name, product.price, product.quantity, product.wattage)
        elif isinstance(product, HouseholdAppliances):
            sql = "INSERT INTO products (product_id, name, price, quantity, material) VALUES (%s, %s, %s, %s, %s)"
            values = (product.product_id, product.name, product.price, product.quantity, product.color)
        else:
            sql = "INSERT INTO products (product_id, name, price, quantity) VALUES (%s, %s, %s, %s)"
            values = (product.product_id, product.name, product.price, product.quantity)

        self.cursor.execute(sql, values)
        self.connection.commit()

    def __str__(self) -> str:
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()
        result = f"Danh sách các sản phẩm trong kho: \n"
        for product in products:
            result += f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, Quantity: {product[3]}, Wattage: {product[4]}, Color: {product[5]}\n"
        return result
    def display_info_by_type(self, loai) -> str:
        products = []
        if loai.upper() == "K":
            self.cursor.execute("SELECT * FROM products WHERE color IS NULL ")
            products = self.cursor.fetchall()
        elif loai.upper() == "H":
            self.cursor.execute("SELECT * FROM products WHERE wattage IS NULL ")
            products = self.cursor.fetchall()
        else:
            return "Loại sản phẩm không hợp lệ"
        
        result = f"Danh sách các sản phẩm trong kho: \n"
        for product_info in products:
            result += f"ID: {product_info[0]}, Name: {product_info[1]}, Price: {product_info[2]}, Quantity: {product_info[3]}, Wattage: {product_info[4]}, Color: {product_info[5]}\n"
        return result
    def search_product(self, keyword):
        sql = "SELECT * FROM products WHERE name LIKE %s"
        self.cursor.execute(sql, (f"%{keyword}%",))
        found_products = self.cursor.fetchall()
        result = " "
        for product in found_products:
            result += f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, Quantity: {product[3]}, Wattage: {product[4]}, Color: {product[5]}\n"
        return result
    def update_product(self, product_id, new_price, new_quantity):
        
        self.cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = self.cursor.fetchone()
        if not product:
            return False
        
        sql = "UPDATE products SET price = %s, quantity = %s WHERE product_id = %s"
        values = (new_price, new_quantity, product_id)
        self.cursor.execute(sql, values)
        self.connection.commit()
    def delete_product(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = self.cursor.fetchone()
        if not product:
            return False
        sql = "DELETE FROM products WHERE product_id = %s"
        self.cursor.execute(sql, (product_id,))
        self.connection.commit()