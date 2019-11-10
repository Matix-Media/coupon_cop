import sqlite3
import sys
import re
from uuid import uuid4

software_info = {"name": "coupon_cop", "version_tag": "0.1.1",
                 "version": "0.11", "Developer": "Matix Media, Inc."}

database_info = {"connection": "coupon_cop.db", "tables": {
    "coupon_table": "coupons", "users_table": "users", "action_tables": "actions"}}


# *: Main App Starts
db = sqlite3.connect(database_info["connection"])
db_cursor = db.cursor()


def IsFloat(string):
    if re.match("^\d+?\.\d+?$", string) is None:
        return False
    else:
        return True


def Install(params=None):
    print("SUC|Installed")


def ProgramHelp(params=None):
    print()
    print("COUPON COP (v{}) HELP".format(software_info["version_tag"]))
    print()
    print("Create new coupon:        new_coupon <discount>")
    print("Check coupon:             check_coupon <data type (id/code)> <id/code>")
    print("Use coupon:               use_coupon <data type (id/code)> <id/code>")
    print("Reset coupon:             use_coupon <data type (id/code)> <id/code>")


class MessageHandler:
    def __init__(self):
        pass

    def error(self, code, message):
        print("ERR|[{}]{}".format(code, message))

    def success(self, message):
        print("SUC|{}".format(message))

    def debug(self, message):
        print("DBG|{}".format(message))


class Coupon:
    def __init__(self, cursor, msg):
        self.cursor = cursor
        self.msg = msg

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, code STRING, amount DOUBLE, active BOOLEAN);"
            .format(database_info["tables"]["coupon_table"]))

    def new_coupon(self, params):
        if len(params) == 1:
            if IsFloat(params[0]):
                amount = float(params[0])
                code = uuid4()

                try:
                    self.cursor.execute("INSERT INTO {} VALUES (NULL, '{}', {}, true)".format(
                        database_info["tables"]["coupon_table"], code, amount))
                except sqlite3.OperationalError:
                    self.msg.error(500, "Unable zo update database")
                    return

                self.msg.success("{}={}".format(code, amount))

            else:
                self.msg.error(400, "Parameter not float")

        else:
            self.msg.error(2, "Missing parameter")

    def check_coupon(self, params):
        if len(params) == 2:
            get_type = ""
            code = params[1]
            data = None
            if params[0] == "id" or "code":
                get_type = params[0]
            else:
                self.msg.error(400, "Unknown type")

            try:
                self.cursor.execute(
                    "SELECT * FROM {} WHERE {} = '{}'".format(database_info["tables"]["coupon_table"], get_type, code))
                data = self.cursor.fetchone()
            except sqlite3.OperationalError:
                self.msg.error(500, "Unable to get data from database")
                return

            self.msg.success("{}={}={}".format(data[1], data[2], data[3]))

        else:
            self.msg.error(2, "Missing parameters")

    def use_coupon(self, params):
        if len(params) == 2:
            get_type = ""
            code = params[1]
            if params[0] == "id" or "code":
                get_type = params[0]
            else:
                self.msg.error(400, "Unknown type")

            try:
                self.cursor.execute("UPDATE {} set active = false WHERE {} = {}".format(
                    database_info["tables"]["coupon_table"], get_type, code))
            except sqlite3.OperationalError:
                self.msg.error(500, "Unable to change data from database")
                return

            self.msg.success("{}={}=0".format(get_type, code))

        else:
            self.msg.error(2, "Missing parameters")

    def reset_coupon(self, params):
        if len(params) == 2:
            get_type = ""
            code = params[1]
            if params[0] == "id" or "code":
                get_type = params[0]
            else:
                self.msg.error(400, "Unknown type")

            try:
                self.cursor.execute("UPDATE {} set active = true WHERE {} = {}".format(
                    database_info["tables"]["coupon_table"], get_type, code))
            except sqlite3.OperationalError:
                self.msg.error(500, "Unable to change data from database")
                return

            self.msg.success("{}={}=1".format(get_type, code))

        else:
            self.msg.error(2, "Missing parameters")


msg_hdr = MessageHandler()
cpn = Coupon(db_cursor, msg_hdr)

commands = {"new_coupon": cpn.new_coupon, "check_coupon": cpn.check_coupon,
            "use_coupon": cpn.use_coupon, "reset_coupon": cpn.reset_coupon, "install": Install, "help": ProgramHelp}


input_data = sys.argv


# *: Routines


if len(input_data) > 1:
    if input_data[1] in commands:
        command = input_data[1]
        command_params = input_data[2:]
        commands[command](command_params)
    else:
        msg_hdr.error(1, "Unknown Command")
else:
    msg_hdr.error(0, "No Command")

db.commit()
db.close()
