import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from difflib import SequenceMatcher

url_list = []
out_put_case_number = []
out_put_case_name = []
out_put_patent = []
out_put_cited_by = []
out_put_party_type = []
out_put_assignee = []
out_put_assignee_Type = []
out_put_pb_num = []
out_put_pb_num_match = []
checker_name = []

#checker
all_pub_number = []

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def fetchDataCreateCSv(tb_cited_by,case_name,case_number,patent,party_type):
    assignee_original = tb_cited_by.find_all("span", {"itemprop": "assigneeOriginal"})
    publication_number = tb_cited_by.find_all("span", {"itemprop": "publicationNumber"})
                                        
        
    for i in range(len(assignee_original)):
        assignee_names = assignee_original[i].getText()
        pb_num = publication_number[i].getText()
        if pb_num not in all_pub_number:
            print("Cited By: "+assignee_names+" ----- "+pb_num+" -------- "+patent+" ---- ")
            out_put_case_name.append(case_name)
            out_put_case_number.append(case_number)
            out_put_patent.append(patent)
            out_put_party_type.append(party_type)
            out_put_assignee.append(assignee_names)
            out_put_cited_by.append("False")
            out_put_pb_num.append(pb_num)

            df = pd.DataFrame(data={"case_name": out_put_case_name,
                                    "case number": out_put_case_number,
                                    "patent": out_put_patent,
                                    "party_type":out_put_party_type,
                                    "assignee":out_put_assignee,
                                    "Boolean": out_put_cited_by,
                                    "publicationNumber": out_put_pb_num})

            df.to_csv("output.csv", sep=',',index=True)


def readPatentCsv(input_df):
    all_pub_number = input_df['publicationNumber']
    
    for i in range(len(input_df['case number'])):
        case_name = input_df['case_name'][i]
        case_number = input_df['case number'][i]
        patent = input_df['patent'][i]
        party_type = input_df['party_type'][i]

        url = "https://patents.google.com/patent/US"+patent
        print("------------------------------------------------------------------------")
        print("case number: "+case_number+" --- case name:"+case_name+" --- patent: "+patent)
        print("fetching data URL: ( "+url+" )")
        r = requests.get(url)
        soup = BeautifulSoup(r.content,"html.parser")
        all_table = soup.find_all("table")
        tb_len = len(all_table)

        try:
            if tb_len > 11:
                tb_cited_by = all_table[7]
                fetchDataCreateCSv(tb_cited_by,case_name,case_number,patent,party_type)
            else:
                tb_cited_by = all_table[8]
                fetchDataCreateCSv(tb_cited_by,case_name,case_number,patent,party_type)
        except Exception as e:
            print("--SKIP--")
            print(e)
     
try:
    input("Press Enter to Execute the scrript.")
    input_df = pd.read_csv('TrainingSet.csv')
    readPatentCsv(input_df)
except Exception as e:
    print(e)
    input("Could not find TrainingSet.csv and names.csv.")
