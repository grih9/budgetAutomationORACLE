import pyodbc
from cryptography.fernet import Fernet

import properties


class Sql:
    def __init__(self, server="localhost:1521/xe"):
        self.cnxn = pyodbc.connect("Driver={Oracle in instantclient_19_10};"
                                   "Dbq=" + server + ";"
                                                     "Uid=c##grih9;"
                                                     "Pwd=MyPass;")
        self.cursor = self.cnxn.cursor()

    def check_password(self, login, password):
        cipher = Fernet(properties.cipher_key)
        self.cursor.execute(f"SELECT u_id, u_password FROM accounts where u_login='{login}'")
        row = self.cursor.fetchone()
        if row is not None:
            pw = cipher.decrypt(str.encode(row[1])).decode('utf8')
            if pw == password:
                return True, row[0]
            else:
                return False, row[0]
        else:
            return False, 0

    def add_user(self, login, password):
        cipher = Fernet(properties.cipher_key)
        encrypted_password = password.encode('utf8')
        encrypted_password = cipher.encrypt(encrypted_password)
        try:
            self.cursor.execute(f"INSERT INTO accounts(u_login, u_password) "
                                f"VALUES ('{login}','{encrypted_password.decode('utf-8')}')")
            self.cnxn.commit()
            self.cursor.execute(f"SELECT u_id from accounts where u_login='{login}'")
            row = self.cursor.fetchone()
            return True, row[0]
        except:
            return False, 0

    # def updatePassword(self, login, password):
    #     cipher = Fernet(properties.cipher_key)
    #     encrypted_password = password.encode('utf8')
    #     encrypted_password = cipher.encrypt(encrypted_password)
    #     self.cursor.execute("UPDATE Пользователи SET Пароль='"+encrypted_password.decode("utf-8")+"' where Логин='"+login+"'")
    #     self.cnxn.commit()
    #
