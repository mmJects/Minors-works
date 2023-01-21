from . import db,json_data_filepath
from werkzeug.security import generate_password_hash,check_password_hash
import json
from .support_for_todos import sorting_time,give_the_month

class User():      
    def __init__(self,**args):
        self.datas = args
        if "password" in self.datas:
            self.pass_hash = generate_password_hash(self.datas["password"],method="sha256")


    def insert_into_table(self):
        duplicate_check = db.execute("select * from user_signup_data where email = ?",self.datas["email"])
        if duplicate_check == []:
            query = "insert into user_signup_data(Uid,name,email,pw) values(?,?,?,?)"
            db.execute(query,self.datas["uid"],self.datas["name"],self.datas["email"],self.pass_hash)
            return True
        else:
            return False

    def get_user_datas(self):
        name = db.execute("select name from user_signup_data where name = ?",self.datas["Uid"])
        return name

    def check_email(self):
        query = "select * from user_signup_data where email = ?"
        self.db_datas = db.execute(query,self.datas["email"])
        if self.db_datas == []:
            return "Invalid Email!!!!"
        elif not check_password_hash(self.db_datas[0]["pw"],self.datas["password"]):
            return "Incorrect password for your account!!!"
        else:
            return True

class Notes():     
    def __init__(self,**args):
        self.datas = args

    def insert_into_table(self):
        query = "insert into users_notes(note,Uid) values(?,?)"
        db.execute(query,self.datas["note"],self.datas["uid"])

    def get_notes(self,forr="display"):
        search_query = "select id,note from users_notes where Uid = ?"
        results = db.execute(search_query,self.datas["uid"])
        if forr == "display":
            return results
        else:
            csv = "No,Notes"
            for idx,item in enumerate(results,start=1):
                csv += "\n" + str(idx) + "," + item['note']
            return csv


    def delete_note(self,all=False):
        if not all:
            delete_note_query = "delete from users_notes where id = ?"
            db.execute(delete_note_query,self.datas["id"])
        else:
            delete_all_note_query = "delete from users_notes where Uid = ?"
            db.execute(delete_all_note_query,self.datas["uid"])



class ToDos():
    def __init__(self,uid):
        self.uid = uid
        self.create_json_file()

    def create_json_file(self):
        json_object = json.dumps({},indent=4)
        with open(json_data_filepath,"r+") as file:
            try:
                json.load(file)
            except:
                file.write(json_object)

    def get_todos(self):
        with open(json_data_filepath,"r+") as file:
            x = json.load(file)
            todos = x.get(self.uid,{})
        return todos

    def add_todos(self,acti,timestamp):
        Uid = self.uid
        with open(json_data_filepath,"r+") as file:
            data = json.load(file)
            if Uid in data and data[Uid] != {}:
                id_count = int(list(data[Uid].keys())[-1]) + 1
                dct = data[Uid]
                dct[id_count] = [acti.lower(),timestamp]
                data[Uid] = sorting_time(dct)
            else:
                id_count = 1
                dct = {}
                dct[id_count] = [acti.lower(),timestamp]
                data[Uid] = dct
            file.seek(0)
            json.dump(data, file,indent=4)

    def delete_todos(self,id:int=0,all_todos:bool=False):
        Uid = self.uid
        with open(json_data_filepath,"r+") as file:
            x = json.load(file)
            if not all_todos:
                data = x[Uid]
                try:
                    del data[id]
                except:
                    pass
                x[Uid] = sorting_time(data)
            else:
                x[Uid] = {}
            file.seek(0)
            json.dump(x,file,indent=4)
            file.truncate()

    def search(self,q,uid):
        with open(json_data_filepath,"r+") as file:
            datas = json.load(file)
            data = datas[uid]
            result_dct = {}
            for key,value in data.items():
                todo = value[0]
                if q in todo:
                    result_dct[key] = value
        return result_dct

    def process_file(self,uid):
        csv = "No,ToDo,Time,Date"
        with open(json_data_filepath,"r+") as file:
            datas = json.load(file)
            data = datas[uid]
            for no,todo_data in data.items():
                date_time = todo_data[1].rsplit(":",1)
                date = give_the_month(int(date_time[1]))
                csv += "\n" + no + "," + todo_data[0] + ","  + date_time[0] + "," + date
        return csv
            
