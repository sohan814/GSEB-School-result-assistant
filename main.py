import pyautogui
from selenium import webdriver
import os
import re
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

def get_gseb_results_10(numbers,output_file_path,subjects):
    goto('http://gseb.org/indexssc.html')
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


def get_gseb_results_12(f,seat_numbers,output_file_path,subjects):
    """

    :param f: The category of student in which he belongs which is metioned as first letter of seat number like='A' for std.10
    :param seat_numbers: The list of seat numbers of all stuents e.g.: [3513611,3136144,7724523]
    :param output_file_path: file address where the output result sheet is to be stored e.g. "D:/10_results/result.csv"
    :param subjects: the list of subjects e.g. ['English','Maths',...]
    :return: Nothing but csv is saved in the same folder
    """
    goto('http://www.gseb.org/')
    df=pd.DataFrame()
    temp=[]
    for loop in seat_numbers:
        detail={}
        driver.find_element_by_xpath("//select[@name='drpInitChar']/option[text()='" + f + "']").click()
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
        detail['result']=find(l[2][0],"Result: ").strip('School Index: 27.109')
        for i in range(len(subjects)):
            ttt=5-int(l[4+i][0][-5:].find(re.findall(r"[A-Z]", l[4+i][0][-5:])[0]))
            detail[subjects[i] + ' in total'] = l[4+i][0][-5:-ttt]
            detail[subjects[i] + ' grade'] = l[4+i][0][-ttt:]
        detail['Total']=int(l[11][0][-3:])
        detail['Overall Grade']=find(l[1][0],'Grade: ')
        detail['Percentile Rank']=find(l[1][0],'Percentile: ').split()[0].strip('Grade:')
        temp.append(detail)
        driver.switch_to_default_content()
        driver.find_element_by_name("studentnumber").clear()
    df=df.append(temp,ignore_index=True)
    print(df)
    df.to_csv(output_file_path,index=False)
    driver.close()

def test_tune_parameter(f,numbers):
    """
    :param f: the category like 10th has 'A' while 'B' is for science etc. given as first letter of the seat number
    :param numbers:  the remaining 7 letters of the  seat numbers all provided in a list e.g:[3413535,1355151,3153153..]
    :return: None . This function is just used to tune the values in the main function so we can get indexes of marks
    etc as table structure may change.
    """
    goto('http://www.gseb.org/')
    for loop in numbers:
        driver.find_element_by_xpath("//select[@name='drpInitChar']/option[text()='" + f + "']").click()
        username = driver.find_element_by_name("studentnumber")
        seat_no = loop
        username.send_keys(seat_no)
        go = driver.find_element_by_name("go")
        go.click()
        time.sleep(1)
        driver.switch_to.frame("marksheet")
        soup = BeautifulSoup(driver.page_source)
        table = soup.find("table", attrs={"class": "maintbl"})
        extractor = Extractor(table)
        extractor.parse()
        l = extractor.return_list()
        print(l)


if(__name__=='__main__'):
    f='A'
    # commerce=[275843,275405,275357,275746,275806,
    #     275386,275779,275913,275819,275619,
    #     275748,275896,276133,275856,275567,
    #     276024,275547,275544,275637,275691,
    #     275998,276126]
    # p2=[276476,276488,276481,276442,276423,
    #     276424,276458,276487,276431,276327,
    #     276470,276402,276411,276447,276371,
    #     276428,276406,276387,276374,276412,
    #     276464,276372,276489,276413,276328,
    #     276479,276426]
    # p3=[276438,276490,276425,
    #     276301,276432,276493,276469,276482,
    #     276555,276461,276455,276460,276397,
    #     276451,276499,276502,276434,276459,
    #     276478,276422,276330,276498,276544,
    #     276515,276527,276389,276394
    #     ]
    # p4=[
    #     276539,
    #     276548,276403,276534,276359,276537,
    #     276552,276341,276503,276421,276418,
    #     276420,276536,276505,276556,276417,
    #     276511,276405,276345,276379,276353,
    #     276512,276550,276528,276546,276508,
    #     276355
    # ]
    #
    # subjects_12 = ['Gujarati FL','English','Sanskrit','Philosophy','Sociology','Psychology','Geography','samajik vigyan']

    tenth = [7118781
        , 7118467
        , 7119286
        , 7119260
        , 7120072
        , 7118621
        , 7118656
        , 7121155
        , 7121908
        , 7118547
        , 7121026
        , 7120018
        , 7119717
        , 7118375
        , 7118984
        , 7120199
        , 7119250
        , 7119702
        , 7118812
        , 7121395
        , 7119766
        , 7120001
        , 7120457
        , 7118744
        , 7118293
        , 7119376
        , 7119670
        , 7119929
        , 7118948
        , 7120591
        , 7118308
        , 7118278
        , 7120337
        , 7119172
        , 7118322
        , 7119457
        , 7118242
        , 7119042
        , 7120017
        , 7118277
        , 7119579
        , 7119857
        , 7118759
        , 7119536
        , 7118959
        , 7119312
        , 7118998
        , 7119428
        , 7118578
        , 7120784
        , 7120289
        , 7119825
        , 7118955
        , 7121008
        , 7121082
        , 7120585
        , 7121201
        , 7119480
        , 7120508
        , 7120874
        , 7121019
        , 7120722
        , 7120490
        , 7119540
        , 7119948
        , 7120440
        , 7119632
        , 7120418
        , 7121253
        , 7121289
        , 7120719
        , 7119987
        , 7120836
        , 7119850
        , 7120429
        , 7120220
        , 7120966
        , 7119029
        , 7119985
        , 7118811
        , 7118856
        , 7120699
        , 7120487
        , 7118807
        , 7118806
        , 7119322
        , 7119306
        , 7118650
        , 7118882
        , 7118351
        , 7120702
        , 7119019
        , 7118502
        , 7118994
        , 7118747
        , 7118946
        , 7119488
        , 7119486
        , 7121059
        , 7118769
        , 7118836
        , 7118921
        , 7119395
        , 7121377
        , 7121391
        , 7120749
        , 7118336
        , 7119028
        , 7121383
        , 7118634
        , 7119332
        , 7118932
        , 7118919
        , 7119168
        , 7118465
        , 7120435
        , 7118317
        , 7118428
        , 7118925
        , 7119132
        , 7118962
        , 7119001
        , 7120492
        , 7119279
        , 7118667
        , 7120479
        , 7120175
        , 7118887
        , 7120404
        , 7121392
        , 7119541
        , 7119033
        , 7118851
        , 7118861
        , 7118888
        , 7119740
        , 7118915
        , 7118392
        , 7118850
        , 7119301
        , 7118689
        , 7118869
        , 7119361
        , 7119267
        , 7119268
        , 7119642
        , 7120355
        , 7120851]
    subjects_10 = ['Gujarati FL', 'Social Science', 'Science', 'Mathematics', 'English SL', 'Sanskrit SL']
    get_gseb_results_10(tenth,'10_result.csv',subjects_10)
    #test_tune_parameter('G',['276355'])


