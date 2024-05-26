

from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
import demo
from mysql.connector import Error



class Ui_Login_Dialog(object):
    
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
        
    def check_login(self):
        username = self.lineEdit_us.text()
        password = self.lineEdit_pw.text()
        
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        
        if result:
            self.open_main_window()
        else:
            QtWidgets.QMessageBox.warning(None, "Login Failed", "Invalid username or password")

    def open_main_window(self):
        ui_Dialog = QtWidgets.QDialog()
        filterUi = demo.Ui_Dialog(self.host, self.user, self.password, self.database, self.port)
        filterUi.setupUi(ui_Dialog)
        filterUi.category_changed()
        ui_Dialog.show()
        Dialog.close()  

        ui_Dialog.exec_()
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 200)
        self.label_logo_us = QtWidgets.QLabel(Dialog)
        self.label_logo_us.setGeometry(QtCore.QRect(10, 80, 31, 21))
        self.label_logo_us.setText("")
        self.label_logo_us.setPixmap(QtGui.QPixmap("modules\login.jpg"))
        self.label_logo_us.setScaledContents(True)
        self.label_logo_us.setObjectName("label_logo_us")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 130, 71, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_us = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_us.setGeometry(QtCore.QRect(135, 80, 151, 20))
        self.lineEdit_us.setObjectName("lineEdit")
        self.lineEdit_pw = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_pw.setGeometry(QtCore.QRect(135, 130, 151, 20))
        self.lineEdit_pw.setObjectName("lineEdit_2")
        self.lineEdit_pw.setEchoMode(QtWidgets.QLineEdit.Password)  
        self.label_logo = QtWidgets.QLabel(Dialog)
        self.label_logo.setGeometry(QtCore.QRect(25, 20, 251, 41))
        self.label_logo.setText("")
        self.label_logo.setPixmap(QtGui.QPixmap("modules\logo_toshiba.png"))
        self.label_logo.setObjectName("label_logo")
        self.pushButton_login = QtWidgets.QPushButton(Dialog)
        self.pushButton_login.setGeometry(QtCore.QRect(130, 160, 61, 23))
        self.pushButton_login.setObjectName("pushButton")
        self.label_logo_pw = QtWidgets.QLabel(Dialog)
        self.label_logo_pw.setGeometry(QtCore.QRect(10, 130, 31, 21))
        self.label_logo_pw.setText("")
        self.label_logo_pw.setPixmap(QtGui.QPixmap("modules\password.png"))
        self.label_logo_pw.setScaledContents(True)
        self.label_logo_pw.setObjectName("label_4")
        self.label_us = QtWidgets.QLabel(Dialog)
        self.label_us.setGeometry(QtCore.QRect(50, 80, 81, 16))
        self.label_us.setObjectName("label_us")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        self.pushButton_login.clicked.connect(self.check_login)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Password:"))
        self.pushButton_login.setText(_translate("Dialog", "Login"))
        self.label_us.setText(_translate("Dialog", "User name:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Login_Dialog("monorail.proxy.rlwy.net", "root", "xIbazQgoTOmqlVFBFVpELtNnscUXRTfq", "railway", "45681")
    ui.setupUi(Dialog)
    Dialog.show()
    ret = app.exec_()
    if ui.connection and ui.connection.is_connected():
        ui.cursor.close()
        ui.connection.close()
    sys.exit(ret)