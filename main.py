from modules.user_manager import UserManager
from modules.warehouse import Warehouse
from modules.product import KitchenEquipment
from modules.product import HouseholdAppliances
from modules.product import Product

user_manager = UserManager()
while True:
    username = input("Nhập tài khoản của bạn: ")
    password = input("Nhập mật khẩu của bạn: ")

    result = user_manager.login(username, password)

    if result:
        print("Đăng nhập thành công!")
        warehouse = Warehouse()
        while True:
            print("Menu")
            print("Option 1: Thêm sản phẩm mới ")
            print("Option 2: Xuất thông tin theo loại sản phẩm")
            print("Option 3: Thông tin của toàn bộ sản phẩm có trong kho")
            print("Option 4: Tìm sản phẩm")
            print("Option 5: Cập nhật thông tin theo ID sản phẩm")
            print("Option 6: Xóa thông tin theo ID sản phẩm")
            print("Option 7: Thoát")

            nhap_thao_tac = int(input("Nhập lựa chọn của bạn: "))
            if nhap_thao_tac == 1:
                product_id = input("Nhập mã sản phẩm: ")
                name = input("Nhập tên sản phẩm: ")
                price = int(input("Nhập giá sản phẩm: "))
                quantity = int(input("Nhập số lượng sản phẩm: "))
                product_type = input("Nhập loại sản phẩm (K là thiết bị bếp, H là thiết bị gia dụng, O là khác): ")
                if product_type.upper() == "K":
                    wattage = input("Nhập công suất(W): ")
                    product = KitchenEquipment(product_id, name, price, quantity, wattage)
                elif product_type.upper() == "H":
                    powersource = input("Nhập nguồn điện: ")
                    product = HouseholdAppliances(product_id, name, price, quantity, powersource)
                else:
                    product = Product(product_id, name, price, quantity)
                warehouse.add_product(product)
                print("Thêm sản phẩm thành công!")
            elif nhap_thao_tac == 2:
                loai = input("Nhập loại sản phẩm (K là thiết bị bếp, H là thiết bị gia dụng): ")
                if loai.upper() in ["K", "H"]:
                    print(warehouse.display_info_by_type(loai))
                else:
                    print("Loại sản phẩm không hợp lệ")
            elif nhap_thao_tac == 3:
                print(warehouse.__str__())
            elif nhap_thao_tac == 4:
                    keyword = input("Nhập từ khóa tìm kiếm: ")
                    found_products = warehouse.search_product(keyword)
                    if found_products:
                        print(f"\nCác sản phẩm chứa từ khóa '{keyword}':")
                        print(found_products)
                    else:
                        print(f"Không tìm thấy sản phẩm nào chứa từ khóa '{keyword}'.")    
            elif nhap_thao_tac == 5:
                    product_id = int(input("Nhập ID sản phẩm muốn cập nhật: "))
                    new_price = float(input("Nhập giá mới: "))
                    new_quantity = int(input("Nhập số lượng mới: "))
                    
                    status = warehouse.update_product(product_id, new_price, new_quantity)
                    if status == False:
                        print("Không tìm thấy sản phẩm nào chứa ID này.")
                    else:
                        print("Sản phẩm cập nhập thành công!")
            elif nhap_thao_tac == 6:
                product_id = int(input("Nhập ID sản phẩm muốn xóa: "))
                status = warehouse.delete_product(product_id)
                if status == False:
                    print("Không tìm thấy sản phẩm nào chứa ID này")
                else:
                    print("Sản phẩm cập nhật thành công!")
            elif nhap_thao_tac == 7:
                print("Hẹn gặp lại!")
                break

            else:
                print("Lỗi")
                break
        break   