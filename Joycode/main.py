
import tkinter as tk
from tkinter import PhotoImage
from tkinter.ttk import *
from tkinter import Tk, simpledialog, messagebox
import pandas as pd
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import requests
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import tkinter.font as font
import os
import sys
import datetime
from food import cal_calcurater,dayoftime
try:
    r = requests.get('https://docs.google.com/spreadsheet/ccc?key=1TZQ7C9gXkZaXQbBAglAkYriqfX2KW8rHVzmdLgZ7wi4&output=csv')
except :
    messagebox.showerror('error','You need to have internet connection')
        

data = r.content
df_f = pd.read_csv(BytesIO(data))
df_f =df_f.sort_values(by=['Ingredient'])


#https://docs.google.com/spreadsheets//ccc?key=1TZQ7C9gXkZaXQbBAglAkYriqfX2KW8rHVzmdLgZ7wi4&output=csv
root =tk.Tk()
root.title("Welcome")
root.geometry('700x500')
root.resizable(False, False)
h= pd.read_csv('collection.csv')

img = PhotoImage(file="back.png")
img = img.zoom(3)
label = Label(
    root,
    image=img
)
label.place(x=0, y=0)
print(h)

#bg = Image.open("back.png")
#resized_image= bg.resize((700,500), Image.ANTIALIAS)
#bg= ImageTk.PhotoImage(resized_image)
#bgl = Label( root, image = bg)

#bgl.place(x = 0, y = 0,relheight=1,relwidth=1)
def createnew(food,Calories,Protien,Carbohydrate,Fat,Day,Month,Year):
    
    asking = pd.read_csv('collection.csv')
    asking.loc[len(asking.index)] =[food,Calories,Protien,Carbohydrate,Fat,Day,Month,Year]   
    asking.to_csv('collection.csv',index = False)
def restart():
    
    python = sys.executable
    os.execl(python, python, * sys.argv)

def error():
    try:
        float(weight.get())
    except ValueError:
        messagebox.showerror('error','Weight must be number')
        
    else:
 
        clicked_choose()
def History():
    Y=histo_year.get()
    M=histo_month.get()
    D=histo_day.get()
    ti = dayoftime(Y,M,D)

    v = list(ti.values())
    l = list(ti.keys())
    l.append('Other')
    r=ti['cal'] - (ti['protein']+ti['carbohydrate']+ti['fat'])
    allc= ti['cal']
    print(r)
    if r >= 0:
        v.append(round(r,2))
    else:
        v.append(0)
    v.remove(v[3])
    l.remove('cal')
    varr =np.array(v)

    def absolute_value(val):
        a  = np.round(val/100.*varr.sum(), 2)
        return a
    try:   
        plt.pie(varr,labels = l,autopct=absolute_value)
        plt.savefig('pie.png', dpi=70)
       
    except:
         messagebox.showerror('error',' You do not have any consumption history yet')
    
    else:
       

        lb2.destroy()
        lbl.destroy()
        lb3.destroy()
       
        weight.destroy()
        combo.destroy()
        
        histo_day.destroy()
        histo_month.destroy()
        histo_year.destroy()
        lbh1=Label(root,text = 'Calories you gained in '+D+'/'+M+'/'+Y+'\n is about '+str(round(allc,2))+' calories',font =('Arial Bold',18))
        lbh1.place(x=350,y=90, anchor="center")


        
        
        plt.savefig('pie.png', dpi=70) 
        
        img = ImageTk.PhotoImage(Image.open("pie.png"))
        panel = Label(root, image = img)
        panel.place(x=350,y=300, anchor="center")


        

        btn2=Button(root,text='Go Back',command=restart)
        
        btn2.place(x=350,y=480, anchor="center")
    


def clicked_choose():
    try:
        cal=cal_calcurater(combo.get(),weight.get())
    except:
        messagebox.showerror('error',combo.get()+' is not defined')
    else:    
        histo_day.destroy()
        histo_month.destroy()
        histo_year.destroy()
    
        lb2.destroy()
        lbl.destroy()
        lb3.destroy()
        btn.destroy()



        d = datetime.datetime.now()
        createnew(combo.get(),str(round(cal['cal'], 2)),str(round(cal['protein'], 2)),str(round(cal['carbohydrate'], 2)),str(round(cal['fat'], 2)),d.day,d.month,d.year)
        
        #l=[]
        #for i in  range(len(cal)):
        # v.append(cal.values)
            #l.append(cal.keys)
        #print(v,l)
        c=combo.get()
        lbc2=Label(root,text = 'Calories of '+c+ ' is about '+str(round(cal['cal'], 2))+' calories',font =('Arial Bold',23))
        lbc2.place(x=350,y=90, anchor="center")
        weight.destroy()
        combo.destroy()
        btn.destroy()

        v = list(cal.values())
        l = list(cal.keys())
        l.append('Other')
        r=float(cal['cal']) - (float(cal['protein'])+float(cal['carbohydrate'])+float(cal['fat']))
        print(r)
        if r >= 0:
            v.append(round(r,2))
        else:
            v.append(0)
        v.remove(v[3])
        l.remove('cal')
        varr =np.array(v)

        def absolute_value(val):
            a  = np.round(val/100.*varr.sum(), 2)
            return a
        
        
        plt.title(c+' '+str(round(cal['cal'], 2)))
        plt.pie(varr,labels = l,autopct=absolute_value)
        plt.savefig('pie.png', dpi=70)  

        img = ImageTk.PhotoImage(Image.open("pie.png"))
        panel = Label(root, image = img)
        panel.place(x=350,y=300, anchor="center")


    

        btn2=Button(root,text='Go Back',command=restart)
        btn2.place(x=350,y=480, anchor="center")


  


def main():
    global lbl,lb2,combo,btn,weight,histo_year,histo_month,histo_day,lb3
    
  

    lbl =Label(root,text = 'Choose your Ingredient',font =('Comic Sans MS',30))
    lbl.place(x=350,y=40, anchor="center")
  
    combo = Combobox(root)
    cm =list(set(df_f['Ingredient']))
    cm.sort()
    combo['values'] =cm
    
    combo.current(0)
    combo.config(font=('Comic Sans MS',20))
    combo.place(x=350,y=120, anchor="center")

    #ing=combo.get()
    #ingr = Combobox(root)
    #ingr =list(set(df_f['Ingredient'][df_f['Type']==ing]))
   # ingr.sort()
    #print(ingr)
    #ingr['values'] = int(ingr)
        
   # ingr.current(0)
    #ingr.config(font=('Arial Bold',20))
   # ingr.place(x=350,y=120, anchor="center")

    lb2 =Label(root,text = 'Enter the weight',font =('Comic Sans MS',23))
    lb2.place(x=350,y=180, anchor="center")

    weight =tk.Entry(root)
    weight.config(font=('Comic Sans MS',20))
    weight.place(x=350,y=230, anchor="center")

 
    
    btn = Button(root,text='Ok',command=error, width=10)
    btn.place(x=350,y=270, anchor="center")

    lb3 =Label(root,text = 'Consumption History',font =('Comic Sans MS',16))
    lb3.place(x=120,y=300, anchor="center")
    
    
    histo_year = Combobox(root)
    ny=list(set(h['Year']))
    ny.sort()
    ny.insert(0,'All Year')
    histo_year['values'] =ny
    histo_year.current(0)
    histo_year.config(font=('Comic Sans MS',13),width=10)
    histo_year.place(x=110,y=340, anchor="center")


    histo_month = Combobox(root)
    nm=list(set(h['Month']))
    nm.sort()
    nm.insert(0,'All Month')
    histo_month['values'] =nm
    histo_month.current(0)
    histo_month.config(font=('Comic Sans MS',13),width=10)
    histo_month.place(x=240,y=340, anchor="center")

    
    histo_day = Combobox(root)
    nd=list(set(h['Day']))
    nd.sort()
    nd.insert(0,'All Day')
    histo_day['values'] =nd
    histo_day.current(0)
    histo_day.config(font=('Comic Sans MS',13),width=10)
    histo_day.place(x=370,y=340, anchor="center")

    btn2 = Button(root,text='Check',command=History, width=30,)
    
    btn2.place(x=240,y=370, anchor="center")


    


main()
root.mainloop()