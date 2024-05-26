

import mysql.connector
import FilterDialog
import ReportDialog
from product import Product, KitchenEquipment, HouseholdAppliances
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QMessageBox

from mysql.connector import Error

class Ui_Dialog(object):
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            
            )
            if self.connection.is_connected():
                print("Connected to the database")
            self.cursor = self.connection.cursor(buffered=True)
        except Error as e:
            print(f"Error: {e}")
            self.connection = None
            self.cursor = None
    
    def digital_changed(self):
        selected_type = self.comboBox_type.currentText()
        selected_category = self.comboBox_category.currentText()
        cursor = self.connection.cursor()
        query = """
        SELECT digital_name 
        FROM digital 
        JOIN name_type ON digital.type_id = name_type.id 
        WHERE name_type.category = %s"""
        cursor.execute(query, (selected_type,))  
        digitals = cursor.fetchall()  
        self.comboBox_digital.clear()
        for digital in digitals:
            self.comboBox_digital.addItem(digital[0])  
        cursor.close()   
    def category_changed(self):
        selected_type = self.comboBox_type.currentText()
        cursor = self.connection.cursor(buffered=True)  
        try:
            query = """SELECT category_name 
            FROM category 
            JOIN name_type on category.type_id = name_type.id 
            WHERE name_type.category = %s"""
            cursor.execute(query, (selected_type,))
            categories = cursor.fetchall()
            self.comboBox_category.clear()
            for category in categories:
                self.comboBox_category.addItem(category[0])
        finally:    
            cursor.close()
        self.product_changed()
        self.digital_changed()
        
    def product_changed(self):
        name = self.lineEdit_name.text()
        if name != '':
            self.lineEdit_price.setText('')
        self.spinBox_quantity.setValue(1)
        self.update_subtotal()

    def update_subtotal(self):
        try:
            price_text = self.lineEdit_price.text()
            qty = int(self.spinBox_quantity.text())

            if price_text:
                price = int(price_text)
            else:
                price = 0

            subtotal = str(price * qty)
            self.lineEdit.setText(subtotal)
        except ValueError:
            pass

    def view_product(self):
        id = self.lineEdit_id.text()
        if id == '':
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Information")
            msg.setText("Order ID is empty")
            msg.exec_()
        else:
            cursor = self.connection.cursor(buffered=True)
            query = """
            SELECT p.product_id, p.name, p.price, p.quantity, p.wattage, p.color, t.category, c.category_name
            FROM products AS p
            INNER JOIN name_type AS t ON p.type_id = t.id
            INNER JOIN category AS c ON p.category_id = c.category_id
            WHERE p.product_id = %s

            """
            cursor.execute(query, (id,))
            product = cursor.fetchone()
            if product:
                self.lineEdit_id.setText(f"{product[0]}")
                self.lineEdit_name.setText(f"{product[1]}")
                self.lineEdit_price.setText(f"{product[2]}")
                self.spinBox_quantity.setValue(int(product[3]))
                self.comboBox_type.setCurrentText(f"{product[6]}")
                self.comboBox_category.setCurrentText(f"{product[7]}")
                
                if product[6] == 'HouseholdAppliances':
                    self.lineEdit_thong_so.setText(f"{product[5]}")
                    self.lineEdit_price.setText(f"{product[2]}")
                    self.spinBox_quantity.setValue(int(product[3]))
                elif product[6] == 'KitchenEquipment':
                    self.lineEdit_thong_so.setText(f"{product[4]}")
                    self.lineEdit_price.setText(f"{product[2]}")
                    self.spinBox_quantity.setValue(int(product[3]))
                    
                    
                self.digital_changed()
                
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Information")
                msg.setText("Product ID doesn't exist")
                msg.exec_()
               
    def add_product(self, product):
        try:
            product_id = self.lineEdit_id.text()
            name = self.lineEdit_name.text()
            price = float(self.lineEdit_price.text()) if self.lineEdit_price.text() else 0.0
            quantity = self.spinBox_quantity.value()
            name_type = self.comboBox_type.currentText()
            name_category = self.comboBox_category.currentText()
            print(f"Selected name_type: {name_type}")
            print(f"Selected name_category{name_category}")
            if name_category == 'Washing machine':
                category_id = 2
            elif name_category == 'Fridge':
                category_id = 1
            elif name_category == 'Air conditioner':
                category_id = 3
            elif name_category == 'Microwave':
                category_id = 4
            elif name_category == 'Electronic stove':
                category_id = 5
            elif name_category == 'Vacuum cleaner':
                category_id = 6
            elif name_category == 'Fan':
                category_id = 7
            elif name_category == 'Electric kettle':
                category_id = 8
            elif name_category == 'Oven':
                category_id = 9
            else:
                category_id = 10

            if name_type == 'KitchenEquipment':
                wattage = int(self.lineEdit_thong_so.text()) if self.lineEdit_thong_so.text() else 0.0
                product = KitchenEquipment(product_id, name, price, quantity, wattage)
            elif name_type == 'HouseholdAppliances':
                color = self.lineEdit_thong_so.text()
                product = HouseholdAppliances(product_id, name, price, quantity, color)
            else:
                product = Product(product_id, name, price, quantity)

            cursor = self.connection.cursor()
            if isinstance(product, KitchenEquipment):
                sql = "INSERT INTO products (product_id, name, price, quantity, wattage, type_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (product.product_id, product.name, product.price, product.quantity, product.wattage, product.type_id, category_id)
            elif isinstance(product, HouseholdAppliances):
                sql = "INSERT INTO products (product_id, name, price, quantity, color, type_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (product.product_id, product.name, product.price, product.quantity, product.color, product.type_id, category_id)
            else:
                sql = "INSERT INTO products (product_id, name, price, quantity) VALUES (%s, %s, %s, %s)"
                values = (product.product_id, product.name, product.price, product.quantity)

            cursor.execute(sql, values)
            self.connection.commit()
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Information")
            msg.setText("Product added successfully")
            msg.exec_()
            print("Product added successfully")
            cursor.close()
            
        except Exception as e:
            print("Error adding product:", e)
    def delete_product(self):
        product_id = self.lineEdit_id.text()

        if product_id == '':
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Information")
            msg.setText("ID is empty")
            msg.exec_()
        else:
            cursor = self.connection.cursor()
            query = "SELECT * FROM products WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            product = cursor.fetchone()
           

            if product:
                confirmation = QtWidgets.QMessageBox.question(QtWidgets.QWidget(), "Confirmation", "Are you sure you want to delete this product?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if confirmation == QtWidgets.QMessageBox.Yes:
                    try:
                        query = "DELETE FROM products WHERE product_id = %s"
                        cursor.execute(query, (product_id,))
                        self.connection.commit()
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowTitle("Information")
                        msg.setText("Product deleted successfully")
                        msg.exec_()
                    except Exception as e:
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setText(f"Error deleting product: {e}")
                        msg.exec_()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Information")
                msg.setText("Product ID doesn't exist")
                msg.exec_()
                
    def update_product(self):
        try:
            product_id = self.lineEdit_id.text()
            name = self.lineEdit_name.text()
            price = float(self.lineEdit_price.text()) if self.lineEdit_price.text() else 0.0
            quantity = self.spinBox_quantity.value()
            name_type = self.comboBox_type.currentText()
            name_category = self.comboBox_category.currentText()
            
            if name_category == 'Washing machine':
                category_id = 2
            elif name_category == 'Fridge':
                category_id = 1
            elif name_category == 'Air conditioner':
                category_id = 3
            elif name_category == 'Microwave':
                category_id = 4
            elif name_category == 'Electronic stove':
                category_id = 5
            elif name_category == 'Vacuum cleaner':
                category_id = 6
            elif name_category == 'Fan':
                category_id = 7
            elif name_category == 'Electric kettle':
                category_id = 8
            elif name_category == 'Oven':
                category_id = 9
            else:
                category_id = 10

            cursor = self.connection.cursor()
            if name_type == 'KitchenEquipment':
                wattage = int(self.lineEdit_thong_so.text()) if self.lineEdit_thong_so.text() else 0.0
                sql = "UPDATE products SET name = %s, price = %s, quantity = %s, wattage = %s, category_id = %s WHERE product_id = %s"
                values = (name, price, quantity, wattage, category_id, product_id)
            elif name_type == 'HouseholdAppliances':
                color = self.lineEdit_thong_so.text()
                sql = "UPDATE products SET name = %s, price = %s, quantity = %s, color = %s, category_id = %s WHERE product_id = %s"
                values = (name, price, quantity, color, category_id, product_id)
            else:
                sql = "UPDATE products SET name = %s, price = %s, quantity = %s, category_id = %s WHERE product_id = %s"
                values = (name, price, quantity, category_id, product_id)

            cursor.execute(sql, values)
            self.connection.commit()
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Information")
            msg.setText("Product updated successfully")
            msg.exec_()
            print("Product updated successfully")
            cursor.close()
            
        except Exception as e:
            print("Error updating product:", e)
                
    def clear_product(self):
        self.lineEdit_id.setText('')
        self.lineEdit_name.setText('')
        self.lineEdit_price.setText('')
        self.spinBox_quantity.setValue(1)
        self.lineEdit.setText('0')
        self.comboBox_type.setCurrentText('KitchenEquipment')
        self.category_changed()
        self.digital_changed()
        
    def filter_callback(self):
        filter_Dialog = QtWidgets.QDialog()
        filterUi = FilterDialog.Ui_FilterDialog(self.host, self.user, self.password, self.database, self.port)
        filterUi.setupUi(filter_Dialog)
        filter_Dialog.show()
        filter_Dialog.exec_()
    def report_callback(self):
        report_Dialog = QtWidgets.QDialog()
        report_Ui = ReportDialog.Report_Dialog()
        report_Ui.setupUi(report_Dialog)
        report_Dialog.show()
        report_Dialog.exec_()
        
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(725, 300)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 90, 701, 141))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayoutWidget = QtWidgets.QWidget(self.frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 341, 131))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 5, 4, 1, 1)
        self.pushButton_find = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_find.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("modules\logo_find.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_find.setIcon(icon)
        self.pushButton_find.setObjectName("pushButton_find")
        self.gridLayout.addWidget(self.pushButton_find, 1, 6, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 2, 3, 1, 3)
        self.label_quantity = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_quantity.setObjectName("label_quantity")
        self.gridLayout.addWidget(self.label_quantity, 5, 1, 1, 1)
        self.label_name = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_name.setObjectName("label_name")
        self.gridLayout.addWidget(self.label_name, 2, 1, 1, 1)
        self.spinBox_quantity = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_quantity.setEnabled(True)
        self.spinBox_quantity.setMinimumSize(QtCore.QSize(40, 0))
        self.spinBox_quantity.setObjectName("spinBox_quantity")
        self.spinBox_quantity.valueChanged.connect(self.update_subtotal)
        self.gridLayout.addWidget(self.spinBox_quantity, 5, 3, 1, 1)
        self.label_id = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_id.setObjectName("label_id")
        self.gridLayout.addWidget(self.label_id, 1, 1, 1, 1)
        self.lineEdit_price = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_price.setEnabled(True)
        self.lineEdit_price.setObjectName("lineEdit_price")
        self.lineEdit_price.textChanged.connect(self.update_subtotal)
        self.gridLayout.addWidget(self.lineEdit_price, 4, 3, 1, 3)
        self.label_ = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_.setScaledContents(False)
        self.label_.setObjectName("label_")
        self.gridLayout.addWidget(self.label_, 4, 1, 1, 1)
        self.lineEdit_id = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.gridLayout.addWidget(self.lineEdit_id, 1, 3, 1, 3)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 5, 5, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.frame)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(410, 10, 271, 131))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.comboBox_category = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_category.setObjectName("comboBox_category")
        self.gridLayout_2.addWidget(self.comboBox_category, 1, 1, 1, 1)
        self.comboBox_type = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_type.addItem("KitchenEquipment")
        self.comboBox_type.addItem("HouseholdAppliances")
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.currentIndexChanged.connect(self.category_changed)
        self.gridLayout_2.addWidget(self.comboBox_type, 0, 1, 1, 1)
        self.lineEdit_thong_so = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_thong_so.setObjectName("lineEdit_thong_so")
        self.gridLayout_2.addWidget(self.lineEdit_thong_so, 3, 1, 1, 1)
        self.label_thong_so = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_thong_so.setObjectName("label_thong_so")
        self.gridLayout_2.addWidget(self.label_thong_so, 3, 0, 1, 1)
        self.comboBox_digital = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_digital.setObjectName("comboBox_digital")
        self.gridLayout_2.addWidget(self.comboBox_digital, 2, 1, 1, 1)
        self.label_category = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_category.setObjectName("label_category")
        self.gridLayout_2.addWidget(self.label_category, 1, 0, 1, 1)
        self.label_digital = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_digital.setObjectName("label_digital")
        self.gridLayout_2.addWidget(self.label_digital, 2, 0, 1, 1)
        self.label_type = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_type.setObjectName("label_type")
        self.gridLayout_2.addWidget(self.label_type, 0, 0, 1, 1)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 240, 701, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_add = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout.addWidget(self.pushButton_add)
        self.pushButton_update = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_update.setObjectName("pushButton_update")
        self.horizontalLayout.addWidget(self.pushButton_update)
        self.pushButton_delete = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.horizontalLayout.addWidget(self.pushButton_delete)
        self.pushButton_filter = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_filter.setObjectName("pushButton_filter")
        self.horizontalLayout.addWidget(self.pushButton_filter)
        self.pushButton_report = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_report.setObjectName("pushButton_report")
        self.horizontalLayout.addWidget(self.pushButton_report)
        self.pushButton_clear = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.horizontalLayout.addWidget(self.pushButton_clear)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(0, 30, 271, 41))
        self.label_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("modules\logo_toshiba.png"))
        self.label_2.setScaledContents(False)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(280, 20, 441, 61))
        self.label_3.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("VNI-Lithos")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        
        # Add_product
        self.pushButton_add.clicked.connect(self.add_product)
        #Update
        self.pushButton_update.clicked.connect(self.update_product)
        #Delete_product
        self.pushButton_delete.clicked.connect(self.delete_product)
        #View_product
        self.pushButton_find.clicked.connect(self.view_product)
        #Filter
        self.pushButton_filter.clicked.connect(self.filter_callback)
        #Clear
        self.pushButton_clear.clicked.connect(self.clear_product)
        #Report
        self.pushButton_report.clicked.connect(self.report_callback)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Subtotal:"))
        self.label_quantity.setText(_translate("Dialog", "Quantity:"))
        self.label_name.setText(_translate("Dialog", "Name:"))
        self.label_id.setText(_translate("Dialog", "ID:"))
        self.label_.setText(_translate("Dialog", "Price:"))
        self.label_thong_so.setText(_translate("Dialog", "Parameter:"))
        self.label_category.setText(_translate("Dialog", "Category:"))
        self.label_digital.setText(_translate("Dialog", "Digital:"))
        self.label_type.setText(_translate("Dialog", "Type:"))
        self.pushButton_add.setText(_translate("Dialog", "Add"))
        self.pushButton_update.setText(_translate("Dialog", "Update "))
        self.pushButton_delete.setText(_translate("Dialog", "Delete"))
        self.pushButton_filter.setText(_translate("Dialog", "Filter"))
        self.pushButton_report.setText(_translate("Dialog", "Report"))
        self.pushButton_clear.setText(_translate("Dialog", "Clear"))
        self.label_3.setText(_translate("Dialog", "Manager System"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog("monorail.proxy.rlwy.net", "root", "xIbazQgoTOmqlVFBFVpELtNnscUXRTfq", "railway", "45681")
    ui.setupUi(Dialog)
    ui.category_changed()
    Dialog.show()
    ret = app.exec_()
    if ui.connection and ui.connection.is_connected():
        ui.cursor.close()
        ui.connection.close()
    sys.exit(ret)
