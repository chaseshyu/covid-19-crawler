#!/usr/bin/python
######-*- coding: utf-8 -*-
import os, datetime, requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQuDj0R6K85sdtI8I-Tc7RCx8CnIxKUQue0TCUdrFOKDw9G3JRtGhl64laDd3apApEvIJTdPFJ9fEUL/pubhtml?gid=0&single=true'

work_path = '/path/to/working/dir'

def get_table():
    req = requests.session()
    response = req.get(url,headers={'Accept-Language': 'zh-TW'})
    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find('table', {'class': 'waffle'})
    trs = table.find_all('tr')[1:]

    rows = list()
    for tr in trs:
        rows.append([td.text.replace('\n', '') for td in tr.find_all('td')])

    columns = rows[0][:]
    columns[0] = columns[0][4:]
    columns[2:5] = [columns[0],columns[0],columns[0]]
    rows = [r[1:] for r in rows]
    df = pd.DataFrame(data=rows, columns=columns[1:])
    return df

def biuld_nation():
    df = get_table()
    df_nation = df.drop(columns=columns[2])
    df_nation.to_csv('nation.csv',index=False)
    
def biuld_database():
    database = pd.read_csv('nation.csv')
    df_nation.to_csv('database.csv',index=False)

def update_database():
    database = pd.read_csv('database.csv')
    df = get_table()
    new = pd.merge(database,df,on='Nation')
    new.to_csv('database.csv',index=False)
    new

def main():
    os.chdir(work_path)

    if not os.path.isfile('nation.csv'):
        biuld_nation()

    if not os.path.isfile('database.csv'):
        biuld_database()

    update_database()

if __name__ == '__main__':
    main()

