## Tiêu đề & mô tả ngắn

# Quản lý cửa hàng (MySQL + PyQt5)

Ứng dụng quản lý sản phẩm (GUI) viết bằng Python + PyQt5, sử dụng MySQL làm cơ sở dữ liệu. Ứng dụng hỗ trợ thêm / sửa / xóa / xem sản phẩm, lọc danh sách theo nhiều tiêu chí và xuất báo cáo (biểu đồ).

## Tóm tắt
- Giao diện chính: `modules/demo.py` (UI + logic)
- Lớp model sản phẩm: `modules/product.py`
- Hộp thoại lọc: `modules/FilterDialog.py`
- Hộp thoại báo cáo: `modules/ReportDialog.py` (dùng matplotlib)
- Hộp thoại lọc khách hàng (từ JSON): `modules/filter_customer.py`
- Một số file dữ liệu mẫu: `modules/category.csv`, `modules/product.csv`, `modules/name_type.csv`
- File hỗ trợ import lên SQL: `modules/to_sql.ipynb`


## Tính năng
- Thêm, cập nhật, xóa, xem sản phẩm
- Lọc sản phẩm theo: loại, khoảng subtotal (price * quantity), khoảng quantity, id tùy chỉnh
- Báo cáo: biểu đồ phân bố theo loại và theo khoảng giá, tổng kết
- Giao diện lọc khách hàng từ file JSON (mẫu)

---

## Yêu cầu
- Python 3.8+
- MySQL server
- Thư viện Python:
  - PyQt5
  - mysql-connector-python
  - python-dotenv
  - matplotlib

Cài các gói bằng pip:
```
pip install PyQt5 mysql-connector-python python-dotenv matplotlib
```

---

## Cấu trúc CSDL
Dựa theo các truy vấn trong mã nguồn, các bảng chính cần có:

Bảng `name_type` (loại sản phẩm)
```sql
CREATE TABLE name_type (
  id INT PRIMARY KEY AUTO_INCREMENT,
  category VARCHAR(255) NOT NULL
);
```

Bảng `category` (danh mục con theo type)
```sql
CREATE TABLE category (
  category_id INT PRIMARY KEY AUTO_INCREMENT,
  category_name VARCHAR(255) NOT NULL,
  type_id INT,
  FOREIGN KEY (type_id) REFERENCES name_type(id)
);
```

Bảng `products`
```sql
CREATE TABLE products (
  product_id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(255),
  price DECIMAL(15,2),
  quantity INT,
  wattage INT,          -- dùng cho KitchenEquipment
  color VARCHAR(100),   -- dùng cho HouseholdAppliances
  type_id INT,
  category_id INT,
  FOREIGN KEY (type_id) REFERENCES name_type(id),
  FOREIGN KEY (category_id) REFERENCES category(category_id)
);
```

Bảng `digital` (nếu cần, từ truy vấn trong demo)
```sql
CREATE TABLE digital (
  id INT PRIMARY KEY AUTO_INCREMENT,
  digital_name VARCHAR(255),
  type_id INT,
  FOREIGN KEY (type_id) REFERENCES name_type(id)
);
```

Lưu ý: Các kiểu dữ liệu và ràng buộc có thể chỉnh phù hợp với dữ liệu thực tế.

---

## Chuẩn bị môi trường
1. Tạo database MySQL và các bảng theo schema trên.
2. Import dữ liệu mẫu từ `modules/*.csv` hoặc dùng `modules/to_sql.ipynb` (Jupyter notebook) để đẩy dữ liệu vào MySQL.
3. Tạo file `.env` (ở thư mục gốc repo) với các biến kết nối (tên biến theo ví dụ trong demo.py):
```
host=your_mysql_host
user=your_user
password=your_password
database=your_database
port=3306
```
4. Hoặc chỉnh trực tiếp chuỗi kết nối trong `modules/demo.py`, `modules/FilterDialog.py`, `modules/ReportDialog.py`

## Chạy ứng dụng
Chạy ứng dụng GUI:
```
python -m modules.demo
```
Hoặc:
```
cd modules
python demo.py
```
