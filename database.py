from deta import Deta

DETA_KEY = "RFZS2KSz_pX5PDUACkTyCdPCFh1qgXd8oy9xbQLJz"

deta = Deta(DETA_KEY)

db = deta.Base("user_db")


def insert_user(username, name, password):
    return db.put({"Key": username, "name": name, "password": password})


insert_user("shresth_38","Shreth Deorari","13feb2004")
