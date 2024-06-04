class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        result = f"Mã sản phẩm: {self.product_id}"
        result += "\n"
        result += f"Tên sản phẩm: {self.name}"
        result += "\n"
        result += f"Giá sản phẩm: {self.price}"
        result += "\n"
        result += f"Số lượng sản phẩm: {self.quantity}"
        return result

    def calculate_total(self):
        return self.price * self.quantity

class KitchenEquipment(Product):
    def __init__(self, product_id, name, price, quantity, wattage ):
        super().__init__(product_id, name, price, quantity)
        self.wattage = wattage
        self.type_id = 1

    def display_info(self):
        super().__str__(self)
        result = "\n"
        result += f"Công suất(W): {self.wattage}"
        result += "\n"
        result += f"Type_id {self.type_id}"
        return result

class HouseholdAppliances(Product):
    def __init__(self, product_id, name, price, quantity, color):
        super().__init__(product_id, name, price, quantity)
        self.color = color
        self.type_id = 2

    def display_info(self):
        super().__str__(self)
        result = "\n"
        result += f"Màu sắc: {self.color}"
        result += "\n"
        result += f"Type_id {self.type_id}"
        return result