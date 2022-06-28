import serial
import time
from io import BytesIO
import requests

import pandas as pd
def cal_calcurater(ingrad,g):
    re = requests.get('https://docs.google.com/spreadsheet/ccc?key=1TZQ7C9gXkZaXQbBAglAkYriqfX2KW8rHVzmdLgZ7wi4&output=csv')
    datar = re.content
    collec = pd.read_csv(BytesIO(datar))
    
    df_ingrad=collec.loc[collec['Ingredient'] == ingrad]

    g=float(g)
    

    cal_protien =((float(df_ingrad['Protein (g)'].values[0])/float(df_ingrad['g'].values[0]))*g) *4
    cal_carbo =((float(df_ingrad['Carbohydrate (g)'].values[0])/float(df_ingrad['g'].values[0]))*g) *4
    cal_fat =((float(df_ingrad['Fat (g)'].values[0])/float(df_ingrad['g'].values[0]))*g) *9

    cal=(float(df_ingrad['Calories'].values[0])/float(df_ingrad['g'].values[0]))*g
    all_cal ={'protein':cal_protien,'carbohydrate':cal_carbo,'fat':cal_fat,'cal':cal}
    
    return all_cal
    
def dayoftime(year,month,day):
    print(year,month,day)
    re = pd.read_csv('lock/collection.csv')
    if year =='All Year':
        pass
    else:
        re=re[re['Year']==int(year)]

    if month =='All Month':
        pass
    else:
        re=re[re['Month']==int(month)]


    if day =='All Day':
        pass
    else:
        re=re[re['Day']==int(day)]


    print(re)

    Total_A = re['Calories'].sum(axis=0)
    Total_P = re['Protein'].sum(axis=0)
    Total_C = re['Carbohydrate'].sum(axis=0)
    Total_F = re['Fat'].sum(axis=0)
    print(Total_A)
    
    DI ={'protein':Total_P,'carbohydrate':Total_C,'fat':Total_F,'cal':Total_A}
    return DI

   
