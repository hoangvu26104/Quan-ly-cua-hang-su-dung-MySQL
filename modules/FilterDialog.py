import mysql.connector
from mysql.connector import Error
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FilterDialog(object):
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
        self.cursor = None
        self.connect_to_database()

    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if self.connection.is_connected():
                print("Connected to the database")
                self.cursor = self.connection.cursor(buffered=True)
        except Error as e:
            print(f"Error: {e}")
            self.connection = None
            self.cursor = None
            
    def un_check_all(self):
        self.checkBox_subtotal.setChecked(False)
        self.checkBox_quantity.setChecked(False)
        self.checkBox_type.setChecked(False)
        self.checkBox_custom.setChecked(False)
    
    def check_sub(self):
        self.checkBox_subtotal.setChecked(True)
        self.checkBox_noCriteria.setChecked(False)   
    def check_qty(self):
        self.checkBox_quantity.setChecked(True)
        self.checkBox_noCriteria.setChecked(False)

    def check_type(self):
        self.checkBox_type.setChecked(True)
        self.checkBox_noCriteria.setChecked(False)

    def check_ct(self):
        self.checkBox_custom.setChecked(True)
        self.checkBox_noCriteria.setChecked(False) 
        
    def noFilterCriteria(self):
        if self.connection is None or not self.connection.is_connected():
            self.connect_to_database()
        if self.connection is not None and self.connection.is_connected():
            cursor = self.connection.cursor(buffered=True)
            query = """
            SELECT DISTINCT p.product_id, p.name, p.price, p.quantity, t.category
            FROM products AS p
            INNER JOIN name_type AS t ON p.type_id = t.id
            INNER JOIN category AS c ON t.id = c.type_id
            ORDER BY p.product_id

            """
            cursor.execute(query)
            products = cursor.fetchall()
            
            
            self.tableWidget.setRowCount(0)  
            for row_number, row_data in enumerate(products):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                    
                price = row_data[2]
                quantity = row_data[3]
                subtotal = price * quantity
                self.tableWidget.setItem(row_number, len(row_data), QtWidgets.QTableWidgetItem(str(subtotal)))
            self.un_check_all()
            cursor.close()
        else:
            print("Failed to reconnect to the database.")  
            
        
    def OK_callback(self):
        def populate_table(data):
            self.tableWidget.setRowCount(0) 
            for row_number, row_data in enumerate(data):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                
                price = row_data[2]
                quantity = row_data[3]
                subtotal = price * quantity
                self.tableWidget.setItem(row_number, len(row_data), QtWidgets.QTableWidgetItem(str(subtotal)))

        if self.checkBox_noCriteria.isChecked():
            self.noFilterCriteria()
            return

        if self.connection is None or not self.connection.is_connected():
            self.connect_to_database()

        if self.connection is not None and self.connection.is_connected():
            query = """
            SELECT DISTINCT p.product_id, p.name, p.price, p.quantity, t.category
            FROM products AS p
            INNER JOIN name_type AS t ON p.type_id = t.id
            """
            
            conditions = []
            params = []

            if self.checkBox_type.isChecked():
                name_type = self.comboBox_type.currentText()
                conditions.append("t.category = %s")
                params.append(name_type)

            if self.checkBox_subtotal.isChecked():
                pr = ["< 5M", "5M -> < 10M", "10M -> 20M", "> 20M"]
                price_range = self.comboBox_subtotal.currentText()
                if price_range == pr[0]:
                    conditions.append("(p.price * p.quantity) < 5000000")
                elif price_range == pr[1]:
                    conditions.append("(p.price * p.quantity) >= 5000000 AND (p.price * p.quantity) < 10000000")
                elif price_range == pr[2]:
                    conditions.append("(p.price * p.quantity) >= 10000000 AND (p.price * p.quantity) < 20000000")
                elif price_range == pr[3]:
                    conditions.append("(p.price * p.quantity) >= 20000000")
            if self.checkBox_quantity.isChecked():
                qty_range = self.comboBox_quantity.currentText()
                if qty_range == "< 10":
                    conditions.append("p.quantity < 10")
                elif qty_range == "10 -> < 20":
                    conditions.append("p.quantity >= 10 AND p.quantity < 20")
                elif qty_range == "20 -> 50":
                    conditions.append("p.quantity >= 20 AND p.quantity <= 50")
                elif qty_range == "> 50":
                    conditions.append("p.quantity > 50")
            if self.checkBox_custom.isChecked():
                customer_id = self.lineEdit_custom.text()
                conditions.append("p.product_id = %s")
                params.append(customer_id)
                

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            cursor = self.connection.cursor(buffered=True)
            cursor.execute(query, tuple(params))
            products = cursor.fetchall()
            populate_table(products)
            cursor.close()
        else:
            print("Failed to reconnect to the database.")
    def setupUi(self, FilterDialog):
        FilterDialog.setObjectName("FilterDialog")
        FilterDialog.resize(588, 395)
        self.tableWidget = QtWidgets.QTableWidget(FilterDialog)
        self.tableWidget.setGeometry(QtCore.QRect(0, 100, 581, 291))
        self.tableWidget.setRowCount(30)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setObjectName("tableWidget")
        self.groupBox = QtWidgets.QGroupBox(FilterDialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 550, 91))
        self.groupBox.setObjectName("groupBox")
        self.checkBox_subtotal = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_subtotal.setGeometry(QtCore.QRect(10, 20, 220, 21))
        self.checkBox_subtotal.setObjectName("checkBox_subtotal")
        self.comboBox_subtotal = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_subtotal.setGeometry(QtCore.QRect(110, 20, 111, 21))
        self.comboBox_subtotal.setObjectName("comboBox_subtotal")
        self.checkBox_quantity = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_quantity.setGeometry(QtCore.QRect(10, 60, 220, 21))
        self.checkBox_quantity.setObjectName("checkBox_quantity")
        self.checkBox_type = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_type.setGeometry(QtCore.QRect(230, 20, 67, 21))
        self.checkBox_type.setObjectName("checkBox_type")
        self.checkBox_custom = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_custom.setGeometry(QtCore.QRect(230, 60, 100, 21))
        self.checkBox_custom.setObjectName("checkBox_custom")
        self.comboBox_quantity = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_quantity.setGeometry(QtCore.QRect(110, 60, 111, 22))
        self.comboBox_quantity.setObjectName("comboBox_quantity")
        self.comboBox_type = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_type.setGeometry(QtCore.QRect(320, 20, 111, 22))
        self.comboBox_type.setObjectName("comboBox_type")
        self.checkBox_noCriteria = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_noCriteria.setGeometry(QtCore.QRect(445, 20, 150, 21))
        self.checkBox_noCriteria.setObjectName("checkBox_noCriteria")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(445, 50, 41, 31))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_custom = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_custom.setGeometry(QtCore.QRect(320, 60, 113, 20))
        self.lineEdit_custom.setObjectName("lineEdit_custom")
        
        header = ["Product ID", "Name product", "Price", "Quantity", "Type", "Subtotal"]
        self.tableWidget.setHorizontalHeaderLabels(header)
        self.tableWidget.resizeColumnsToContents()
        
        
        type_ct = ["KitchenEquipment", "HouseholdAppliances" ]
        self.comboBox_type.addItems(type_ct)
        
        pr = ["< 5M", "5M -> < 10M", "10M -> 20M", "> 20M"]
        self.comboBox_subtotal.addItems(pr)
        
        qt = ["< 10", "10 -> < 20", "20 -> < 30", "> 30 "]
        self.comboBox_quantity.addItems(qt)
        
        
        self.checkBox_noCriteria.clicked.connect(self.un_check_all)
        self.checkBox_type.clicked.connect(self.check_type)
        self.checkBox_subtotal.clicked.connect(self.check_sub)
        self.checkBox_quantity.clicked.connect(self.check_qty)
        self.checkBox_custom.clicked.connect(self.check_ct)
        self.pushButton.clicked.connect(self.OK_callback)
        self.checkBox_noCriteria.clicked.connect(self.noFilterCriteria)


        self.retranslateUi(FilterDialog)
        QtCore.QMetaObject.connectSlotsByName(FilterDialog)

    def retranslateUi(self, FilterDialog):
        _translate = QtCore.QCoreApplication.translate
        FilterDialog.setWindowTitle(_translate("FilterDialog", "Dialog"))
        self.groupBox.setTitle(_translate("FilterDialog", "Filter By:"))
        self.checkBox_subtotal.setText(_translate("FilterDialog", "Subtotal"))
        self.checkBox_quantity.setText(_translate("FilterDialog", "Quantity"))
        self.checkBox_type.setText(_translate("FilterDialog", "Type"))
        self.checkBox_custom.setText(_translate("FilterDialog", "Custom"))
        self.checkBox_noCriteria.setText(_translate("FilterDialog", "No Citeria"))
        self.pushButton.setText(_translate("FilterDialog", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FilterDialog = QtWidgets.QDialog()
    ui = Ui_FilterDialog("monorail.proxy.rlwy.net", "root", "xIbazQgoTOmqlVFBFVpELtNnscUXRTfq", "railway", "45681")  # Điền thông tin kết nối
    ui.setupUi(FilterDialog)
    if ui.connection and ui.connection.is_connected():
        ui.cursor.close()
        ui.connection.close()
    FilterDialog.show()
    sys.exit(app.exec_())