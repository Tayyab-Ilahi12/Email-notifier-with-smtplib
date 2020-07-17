import pandas as pd 
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import time
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders

hdr = {'User-Agent': 'chrome/5.0'}

#GLOBAL VARIABLES
TOTAL_DATA = []  #Holds the records of previous data scraped
LIVE_DATA = [] #Current Data 
def data_collect():
    name_and_app_num = active_ingredient = dosage_form = submission = company = submission_classification = submission_status = "N/A"
    try:
        site = 'https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=report.page'  # REQUEST WEB PAGE FOR DATA
        req = Request(site,headers=hdr) 
        page = urlopen(req) 
        soup = BeautifulSoup(page,"html.parser")
        rows = soup.tbody.findAll('tr') # GETTING THE ROWS OF FIRST (LATEST) TABLE
    except:
        pass

    for row in rows:
        try:
            #Name
            name_and_app_num = row.findAll('td')[0].text.strip().split()
            name_and_app_num = ','.join(name_and_app_num)
        except:
            pass

        try:
            #active ingredient
            active_ingredient = row.findAll('td')[1].text
        except:
            pass

        try:
            #Dosage form/Route
            dosage_form = row.findAll('td')[2].text.strip()
        except:
            pass

        try:
            #submission
            submission = row.findAll('td')[3].text.strip()
        except:
            pass

        try:
            #company
            company = row.findAll('td')[4].text.strip()
        except:
            pass

        try:
            #Submission classification
            submission_classification = row.findAll('td')[5].text.strip()
        except:
            pass

        try:
            #Submission status
            submission_status =  row.findAll('td')[6].text.strip()
        except:
            pass

        
        LIVE_DATA.append((name_and_app_num,active_ingredient,dosage_form,submission,company,submission_classification,submission_status))


### COMPARE DATA
def compare_data(new_entry):
    if new_entry in TOTAL_DATA: #IF ITS ALREADY PRESENT RETURN FALSE SO PROGRAM WILL NOT SEND IT
        return False
    else:
        return True #IF ITS NEW THEN SEND IT



### SEND email
def send_email(entry):
    toad = ['receiver_1_@gmail.com','receiver_2_@gmail.com',]  ## HERE YOU HAVE TO PUT ALL THE RECEIVERS ADDRESSES SAME AS THE EXAMPLE
    fromaddr = "SENDER ADDRESS" ## PUT THE SENDER ADDRESS HERE
    for toaddr in toad:
        print("sending email to "+toaddr)
        # instance of MIMEMultipart 
        msg = MIMEMultipart() 

        # storing the senders email address   
        msg['From'] = fromaddr 

        # storing the receivers email address  
        msg['To'] = toaddr

        # storing the subject  
        msg['Subject'] = "EMAIL SUBJECT"  ## ENTER THE SUBJECT OF THE MSG HERE
        s1 = entry[0]
        s2 = entry[1]
        s3 = entry[2]
        s4 = entry[3]
        s5 = entry[4]
        s6 = entry[5]
        s7 = entry[6]
        # string to store the body of the mail 
        body1 = "Business Name:  "+s1
        body2 = "\nActive Ingredient:  " +s2
        body3 = "\nDosage Form:  "+s3
        body4 = "\nSubmission:  "+s4
        body5 = "\nCompany:  "+s5
        body6 = "\nSubmission Classification:  "+s6
        body7 = "\nSubmission Status:  "+s7

        
        # MERGE ALL THE INFO
        message = body1 + '\n' + body2 + '\n' + body3 + '\n' + body4 + '\n' + body5 + '\n' + body6 + '\n' + body7
        
        # attach the body with the msg instance 
        msg.attach(MIMEText(message, 'plain'))
        
        ##########################################
        # creates SMTP session 
        s = smtplib.SMTP('smtp.gmail.com', 587) 

        # start TLS for security 
        s.starttls() 

        # Authentication 
        s.login(fromaddr, "PASSWORD")  ## ENTER YOUR PASSWORD HERE

        # Converts the Multipart msg into a string 
        text = msg.as_string() 

        # sending the mail 
        s.sendmail(fromaddr, toaddr, text) 

        # terminating the session 
        s.quit()




### START FUNCTION
def start():
    del LIVE_DATA[:]
    data_collect()
    if LIVE_DATA is not None:
        for entry in LIVE_DATA:
            cmp_res = compare_data(entry)
            if cmp_res:
                # APPEND TO EXISTING RECORD
                TOTAL_DATA.append(entry)
                #GET FINANCIALS
                #SEND EMAIL
                send_email(entry)
            else:
                print("Entry already present!")
    else:
        print("No Entires Found Yet")
    

if __name__ == '__main__':
    while 1:
        
        #CHECK FOR THE NEW ENTRY IF YES SEND EMAIL WITH FINANCIAL DATA ATTACHED
        print("CHECKING FOR DATA")
        start()
    
        print("On wait")
        #SLEEP FOR 30mint
        time.sleep(1800) ### CHANGE THE TIME IN SECONDS
    