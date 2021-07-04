import time
from datetime import datetime as dt
import random
import json



class DataGen():
    def __init__(self):
        self.timestamp = round(time.time())
        self.USER_NAME = 'abc'
        
        self.start_time = self.timestamp
        

    def data_generation(self):

        #timestamp = round(time.time())

        end_time = self.timestamp + (2*60*60)

        #this below line will make the file clean again then again we can insert new data when we start simulating for new 2hour segment
        with open('RawInputData.json' , 'w') as file:
            json.dump([] , file , indent=4) 

        while self.timestamp < end_time:

            data_dict = {self.USER_NAME:{
            'user_id':self.USER_NAME,
            'timestamp':self.timestamp,
            'heart_beat': random.randint(40,120),
            'resp_rate' : random.randint(10 , 30),
            'activity' : random.randint(1,6)}}

            '''data_dict = {dt.strftime(dt.fromtimestamp(timestamp) , '%Y-%m-%d %H:%M:%S'):{
            'user_id':USER_NAME,
            'timestamp':timestamp,
            'heart_beat': random.randint(40,120),
            'resp_rate' : random.randint(10 , 30),
            'activity' : random.randint(1,6)}}'''
        


        #with open('RawInputData.json' , 'w') as file:
            #json.dump(data_dict , file , indent=4)


            with open('RawInputData.json' , 'r') as file:
                json_file = json.load(file)

            json_file.append(data_dict)

            with open('RawInputData.json' , 'w') as file:
                json.dump(json_file , file , indent=4)
            


         


            self.timestamp +=1

            yield data_dict



#for i in data_generation():
    #print(i)
