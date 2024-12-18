import sys
import os
import json
import traceback
class Dir_Path:
    @staticmethod
    def get_base_path():
        if getattr(sys, 'frozen', False): # executable
            return sys._MEIPASS
        else:
            return os.path.dirname(__file__)
        
class Save_Database:
    @staticmethod
    def save_data(instance):
        try:
            with open(instance.DATA_PATH,'w') as f:
                json.dump(instance.LOCAL_DATA, f, indent=2)
        except Exception as e:
            print("Error:",e)
            print(traceback.format_exc())
            return False
    
class Load_Database:
    @staticmethod
    def load_data(instance):
        try:
            if os.path.exists(instance.DATA_PATH):
                with open(instance.DATA_PATH, 'r') as f:
                    instance.LOCAL_DATA = json.load(f)
            else:
                instance.LOCAL_DATA = {}
        except Exception as e:
            print("Error:",e)
            print(traceback.format_exc())
            return False

class Account(Load_Database,Save_Database): # Session Only Account Storage
    """
    not an actual account but a Save Data to be precise
    user_data=[
        {
            "username":"admin",
            "score":0,
            "level":1,
            "difficulty":"easy",
            "current_level_data":{},
        },
        {
            "username":"admin",
            "score":0,
            "level":1,
            "difficulty":"easy",
            "current_level_data":{},
        }
    ]
    """
    def __init__(self):
        self.LOCAL_DATA={}
        self.DATA_PATH=os.path.join(Dir_Path.get_base_path(),'..','..','data','account.json')
    
    def update(self,username,score,level,difficulty,data):
        self.LOCAL_DATA[username]['score']+=score
        self.LOCAL_DATA[username]['level']=level
        self.LOCAL_DATA[username]['difficulty']=difficulty
        self.LOCAL_DATA[username]['current_level_data']=data
        print(f"Updated {username}")
        
    def register(self,username,level, difficulty,data):
        self.LOCAL_DATA[username]={}
        self.LOCAL_DATA[username]['level']=level
        self.LOCAL_DATA[username]['score']=0
        self.LOCAL_DATA[username]['difficulty']=difficulty
        self.LOCAL_DATA[username]['current_level_data']=data
        print(f"Registered {username}")
    
    def load(self,username):
        return self.LOCAL_DATA.get(username)
    
    def delete(self, username):
        if username in self.LOCAL_DATA:
            self.LOCAL_DATA[username].clear()
            del self.LOCAL_DATA[username]      
        print(f"Deleting {username}")
    
    def get_account_data(self):
        return self.LOCAL_DATA
    
class Scoreboard(Load_Database,Save_Database):
    """
    "User":{
        "level":1,
        "score":0,
    },
    "User2":{
        "level":3,
        "score":4044,
    }
    """
    def __init__(self):
        self.LOCAL_DATA={}
        self.DATA_PATH=os.path.join(Dir_Path.get_base_path(),'..','..','data','scoreboard.json')
        
    def get_scoreboard(self):
        ranking=[]
        for user in self.LOCAL_DATA:
            # print(f"User: {user} Level: {self.LOCAL_DATA[user]['level']} Score: {self.LOCAL_DATA[user]['score']}")
            ranking.append((str(user),self.LOCAL_DATA[user]['level'],self.LOCAL_DATA[user]['score']))
        ranking.sort(key=lambda x: x[2], reverse=True)
        return ranking[:5]
    
    def insert_score(self, username, score, level):
        if username in self.LOCAL_DATA:
            self.LOCAL_DATA[username]['score']+=score
            self.LOCAL_DATA[username]['level']=level
        else:
            self.LOCAL_DATA[username]={}
            self.LOCAL_DATA[username]['level']=level
            self.LOCAL_DATA[username]['score']=score
    
    def get_scoreboard_data(self):
        return self.local_data
    
class Achievement(Load_Database,Save_Database):
    def __init__(self):
        self.LOCAL_DATA={}
        self.DATA_PATH=os.path.join(Dir_Path.get_base_path(),'..','..','data','achievement.json')

    def unlock_achievement(self, achievement_key):
        if achievement_key in self.LOCAL_DATA:
            self.LOCAL_DATA[achievement_key]['unlocked'] = True
            print(f"Achievement unlocked: {achievement_key}")

    def is_achievement_unlocked(self, achievement_key):
        return self.LOCAL_DATA.get(achievement_key, {}).get('unlocked', False)

    def register_achievement(self, achievement_key, description):
        if achievement_key not in self.LOCAL_DATA:
            self.LOCAL_DATA[achievement_key] = {'description': description, 'unlocked': False}
            print(f"Achievement registered: {achievement_key}")

    def get_all_achievements(self):
        return self.LOCAL_DATA
