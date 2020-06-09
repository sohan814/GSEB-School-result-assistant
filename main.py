import pyautogui
from selenium import webdriver
import os
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor

def find(s,f="Name: "):
    index=s.find(f)
    index=index+len(f)
    return s[index:]

chromedriver = "D:/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

def goto(url):
    driver.get(url)
    time.sleep(1.5)

def get_gseb_results(seat_numbers,output_file_path,subjects):
    goto('http://www.gseb.org/')
    df=pd.DataFrame()
    for loop in numbers:
        detail={}
        username = driver.find_element_by_name("studentnumber")
        seat_no=loop
        detail['seat_no']=seat_no
        username.send_keys(seat_no)
        go = driver.find_element_by_name("go")
        go.click()
        time.sleep(1)
        driver.switch_to.frame("marksheet")
        soup = BeautifulSoup(driver.page_source)
        table = soup.find("table", attrs={"class":"maintbl"})
        extractor = Extractor(table)
        extractor.parse()
        l=extractor.return_list()
        detail['Name']=find(l[0][0],"Name: ")
        detail['result']=find(l[1][0],"Result: ").strip('School Index: 55.224')
        for i in range(len(subjects)):
            detail[subjects[i] + ' in external']=l[i+3][1]
            detail[subjects[i] + ' in internal'] = l[i + 3][2]
            detail[subjects[i] + ' in total'] = l[i + 3][3]
            detail[subjects[i] + ' grade'] = l[i + 3][4]
        detail['Total']=int(l[9][1].split()[0])
        detail['Overall Grade']=l[17][0]
        detail['Percentile Rank']=l[17][2]
        df=df.append(detail,ignore_index=True)
        driver.switch_to_default_content()
        driver.find_element_by_name("studentnumber").clear()
    print(df)
    df.to_csv(output_file_path,index=False)
    driver.close()

if(__name__=='__main__'):
    numbers=[7119985,7120017,7120018,7120072,7120175,7120199,7120220,7120289,7120337,7120355,7120404,7120429,7120435,7120440]
    subjects = ['Gujarati FL', 'Social Science', 'Science', 'Mathematics', 'English SL', 'Sanskrit SL']
    get_gseb_results(numbers,'result.csv',subjects)



