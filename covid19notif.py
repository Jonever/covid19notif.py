def Scrap():
    def notifyme(title, message):
        plyer.notification.notify(
            title=title,
            message=message,
            app_icon='vv.ico',
            timeout=20
        )

    url = 'https://www.worldometers.info/coronavirus/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table_body = soup.find('tbody')
    ttt = table_body.find_all('tr')
    notify_country = country_data.get()
    if notify_country == '':
        notify_country = 'Philippines'
    countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases = [], [], [], [], [], [], []
    serious, totalcases_permillion, totaldeaths_permillion, totaltests, totaltests_permillion = [], [], [], [], []
    headers = ['countries', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered', 'active_cases',
              'serious', 'totalcases_permillion', 'totaldeaths_permillion', 'totaltests', 'totaltests_permillion']

    for i in ttt:
        id = i.find_all('td')
        if id[1].text.strip().lower() == notify_country:
            totalcases1 = int(id[2].text.strip().replace(',', ''))
            newcases1 = id[3].text.strip()
            totaldeaths1 = id[4].text.strip()
            newdeaths1 = id[5].text.strip()
            notifyme('Corona Virus Details In {}'.format(notify_country),
                     'Total Cases : {}\nTotal Deaths : {}\nNew Cases : {}\nNew Deaths : {}'.format(totalcases1,
                                                                                                   totaldeaths1,
                                                                                                   newcases1,
                                                                                                   newdeaths1))
        countries.append(id[1].text.strip())
        total_cases.append(int(id[2].text.strip().replace(',', '')))
        new_cases.append(id[3].text.strip())
        total_deaths.append(id[4].text.strip())
        new_deaths.append(id[5].text.strip())
        total_recovered.append(id[6].text.strip())
        active_cases.append(id[7].text.strip())
        serious.append(id[8].text.strip())
        totalcases_permillion.append(id[9].text.strip())
        totaldeaths_permillion.append(id[10].text.strip())
        totaltests.append(id[11].text.strip())
        totaltests_permillion.append(id[12].text.strip())
    df = pd.DataFrame(
        list(zip(countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases, serious,
                 totalcases_permillion, totaldeaths_permillion, totaltests, totaltests_permillion)), columns=headers)
    sor = df.sort_values('total_cases', ascending=False)
    for k in format_list:
        if k == 'html':
            path2 = '{}/alldata.html'.format(path)
            sor.to_html(r'{}'.format(path2))
        if k == 'json':
            path2 = '{}/alldata.json'.format(path)
            sor.to_json(r'{}'.format(path2))
        if k == 'csv':
            path2 = '{}/alldata.csv'.format(path)
            sor.to_csv(r'{}'.format(path2))
    if len(format_list) != 0:
        messagebox.showinfo("Notification", 'Corona Record Is saved {}'.format(path2), parent=root)


def download():
    global path
    if len(format_list) != 0:
        path = filedialog.askdirectory()
    else:
        pass
    Scrap()
    format_list.clear()
    InHtml.configure(state='normal')
    InJson.configure(state='normal')
    InCsv.configure(state='normal')


def inhtml():
    format_list.append('html')
    InHtml.configure(state='disabled')


def incsv():
    format_list.append('csv')
    InCsv.configure(state='disabled')


def injson():
    format_list.append('json')
    InJson.configure(state='disabled')


import plyer
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *
from tkinter import messagebox, filedialog

root = Tk()
root.title("Covid19 Information")
root.geometry("530x300+200+30")
root.configure(bg="#239B56")
root.iconbitmap("vv.ico")
format_list = []
path = ''

# Labels
IntroLabel = Label(root, text='Covid19 Realtime Report', font=('new roman', 30, 'italic bold'), bg='#186A3B', width=22)
IntroLabel.place(x=0, y=0)

EntryLabel = Label(root, text='Enter Country : ', font=('arial', 20, 'italic bold'), bg='#239B56')
EntryLabel.place(x=10, y=70)

FormatLabel = Label(root, text='Download All Data: ', font=('arial', 15, 'italic bold'), bg='#239B56')
FormatLabel.place(x=10, y=150)

# Entry
country_data = StringVar()
ent1 = Entry(root, textvariable=country_data, font=('arial', 20, 'italic bold'), relief=RIDGE, bd=2, width=20)
ent1.place(x=220, y=70)

# Buttons
InHtml = Button(root, text='Html', bg='green', font=('arial', 12, 'italic bold'), relief=RIDGE, activebackground='blue',
                activeforeground='white',
                bd=2, width=5, command=inhtml)
InHtml.place(x=210, y=150)

InJson = Button(root, text='Json', bg='green', font=('arial', 12, 'italic bold'), relief=RIDGE, activebackground='blue',
                activeforeground='white',
                bd=2, width=5, command=injson)
InJson.place(x=320, y=150)

InCsv = Button(root, text='Csv', bg='green', font=('arial', 12, 'italic bold'), relief=RIDGE, activebackground='blue',
               activeforeground='white',
               bd=2, width=5, command=incsv)
InCsv.place(x=430, y=150)

Submit = Button(root, text='Notify/Submit', bg='red', font=('arial', 15, 'italic bold'), relief=RIDGE, activebackground='blue',
                activeforeground='white',
                bd=2, width=25, command=download)
Submit.place(x=110, y=250)
root.mainloop()
