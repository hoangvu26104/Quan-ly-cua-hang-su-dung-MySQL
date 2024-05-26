import mysql.connector

class UserManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="monorail.proxy.rlwy.net",
            user="root",
            password="xIbazQgoTOmqlVFBFVpELtNnscUXRTfq",
            database="railway",
            port="45681"
        )
        self.cursor = self.connection.cursor()

    def login(self, username, password):
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(sql, (username, password))
        user = self.cursor.fetchone()
        if user:
            return True
        else:
            return False