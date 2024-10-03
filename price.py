from selenium import webdriver
import smtplib
import email
import email.mime.application
from selenium.webdriver.chrome.service import Service
import os
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from email.mime.text import MIMEText

chrome_install = ChromeDriverManager().install()
folder = os.path.dirname(chrome_install)
chromedriver_path = os.path.join(folder, "chromedriver.exe")
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service,options=options)

# Items dp codes and the price after discount you want ["example","2000"] in links
links=[]

products=[]
for i in links:
    link = f'https://www.amazon.com/dp/{i[0]}'
    driver.get(link)
    driver.implicitly_wait(5)
    html = driver.page_source
    soup = BeautifulSoup(html)
    try:
      price=soup.find("span",{"class":"a-price"}).find("span").text
    except:
      price=None
    try:
      title=soup.find('title').text
    except:
       title=None
    products.append([title,price])
driver.quit()
finallist=[]
for i in range(0,len(links)):
     if products[i][0] and products[i][1]:
           if products[i][1]<=links[i][1]:
              finallist.append([products[i],links[i][0]])

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.ehlo()
emailpswd="xyz"
emailid = "abc@example.com"
sendtoemail="def@example.com"
name=sendtoemail.split('@')[0]
s.login(emailid,emailpswd)

for i in finallist:
    text = f"""{name}, The product {i[0][0]} is on sale at only {i[0][1]}.\nCheck it out:\nhttps://www.amazon.com/dp/{i[1][0]}"""
    msg = email.message.EmailMessage()
    msg['from'] = emailid
    msg["to"] = sendtoemail
    msg["Subject"] = "Price Discount!!"
    msg.set_content(text)
    """
    res = s.send_message(msg)
    print('Email Sent!!')
s.quit()

