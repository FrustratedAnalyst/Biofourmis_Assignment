from DataGen import DataGen
import numpy as np
import pandas as pd

input_data = DataGen()

user_name = input_data.USER_NAME

start_time = input_data.start_time

fifteen_minute = start_time +(15*60)

max_hr = 0
min_hr = 45 #i have taken min_hr is 45 otherwise if i take it as 0 then the if condition will not satisfy at all at any time
total_hr_count = 0
hr_count = 0
resp_rate_count = 0
total_resp_rate = 0
avg_hr = 0
avg_rr = 0 

frame_data = [[user_name , start_time , fifteen_minute , avg_hr, min_hr , max_hr , avg_rr]]

df = pd.DataFrame(frame_data , columns=['user_name' , 'seg_start' , 'seg_end' , 'avg_hr', 'min_hr' , 'max_hr', 'avg_rr'])

# df.iloc[start_time]['max_hr'] = 77
# df.loc[df[df['seg_start']==start_time]['min_hr'].index]['min_hr'] = 47


# df.at[df[df['seg_start']==start_time].index , 'min_hr'] = 47

# print(df)


for data in input_data.data_generation():
    
    
    # print(data)
    
    if data[input_data.USER_NAME]['timestamp'] >= fifteen_minute:
        start_time = data[input_data.USER_NAME]['timestamp']
        fifteen_minute = data[input_data.USER_NAME]['timestamp'] + (15*60)

        max_hr = 0
        min_hr = 45 
        total_hr_count = 0
        hr_count = 0
        resp_rate_count = 0
        total_resp_rate = 0
        avg_hr = 0
        avg_rr = 0

        new_data = [ user_name ,start_time , fifteen_minute , avg_hr , min_hr , max_hr , avg_rr]
        df.loc[len(df.index)] = new_data

        # # print(df)
        # break
        
    else:
        total_hr_count = total_hr_count + data[input_data.USER_NAME]['heart_beat']
        hr_count +=1

        df.at[df[df['seg_start']==start_time].index , 'avg_hr']  = total_hr_count//hr_count

        
        
        total_resp_rate = total_resp_rate + data[input_data.USER_NAME]['resp_rate']
        resp_rate_count +=1

        df.at[df[df['seg_start']==start_time].index , 'avg_rr']  = total_resp_rate//resp_rate_count


        
        if df[df['seg_start']==start_time]['max_hr'].values[0] < data[input_data.USER_NAME]['heart_beat']:
            df.at[df[df['seg_start']==start_time].index , 'max_hr']  = data[input_data.USER_NAME]['heart_beat']

        if df[df['seg_start']==start_time]['min_hr'].values[0] > data[input_data.USER_NAME]['heart_beat']:
            df.at[df[df['seg_start']==start_time].index , 'min_hr']  = data[input_data.USER_NAME]['heart_beat']

    
print(df)

df.to_csv('FinalData.csv' , index=False)


##############################################################################################################
#hourly dataframe
##############################################################################################################

chunck_size = len(df)//4

data = np.array_split(df ,chunck_size)



data_hourly = [[
    data[0].loc[0]['user_name'] , 
    data[0].loc[0]['seg_start'] , 
    data[0].loc[chunck_size+1]['seg_end'], 
    sum(data[0]['avg_hr'])//len(data[0]),
    min(data[0]['min_hr']),
    max(data[0]['max_hr']),
    sum(data[0]['avg_rr'])//len(data[0])

    ]]


hourly_df = pd.DataFrame( data_hourly , columns=['user_name' , 'seg_start' ,  'seg_end' ,  'avg_hr' , 'min_hr' , 'max_hr' , 'avg_rr'])

for i in range(len(data[1:])):

    first_indexs = pd.DataFrame(data[i+1]).first_valid_index()

    hourly_df.loc[len(hourly_df.index)] = [
                                            data[i+1].loc[first_indexs]['user_name'] , 
                                            data[i+1].loc[first_indexs]['seg_start'] , 
                                            data[i+1].loc[first_indexs+chunck_size+1]['seg_end'], 
                                            sum(data[i+1]['avg_hr'])//len(data[i+1]),
                                            min(data[i+1]['min_hr']),
                                            max(data[i+1]['max_hr']),
                                            sum(data[i+1]['avg_rr'])//len(data[i+1])
                                            ]






hourly_df.to_csv('hourly.csv' , index=False)

print(hourly_df)



        
        
        
    
    

    
