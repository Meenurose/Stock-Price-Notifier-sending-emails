from selenium import webdriver
import time
import smtplib
import os

def get_driver():
  options = webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_argument("disable-blink-features=AutomationControlled")

  driver = webdriver.Chrome(options=options)
  driver.get("https://zse.hr/en/indeks-366/365?isin=HRZB00ICBEX6")
  return driver

def splitting_elem(text):
  """Extracting numeric frm the text"""
  split_op = float(text.split(" ")[0])
  return split_op


def send_mail(num):
  """When percentage goes less than -0.10% sending an email to your email address."""

  my_email = os.getenv("MAIL_ID")
  receiver = os.getenv("RECEIVER")
  pswd = os.getenv("PASSWORD")

  connection = smtplib.SMTP("smtp.gmail.com")
  connection.starttls()
  connection.login(user=my_email, password=pswd)
  connection.sendmail(
    from_addr=my_email,
    to_addrs=receiver,
    msg=
    f"Subject: Percentage change of the stock goes below -0.10% \n\n The Stock percentage change is {num} %"
  )

def main():
  driver = get_driver()
  time.sleep(2)
  elem = driver.find_element(
    by='xpath', value="//*[@id='app_indeks']/section[1]/div/div/div[2]/span"
  )  #Scraping temperature value
  num = splitting_elem(elem.text)

  print(f"Stock Percentage Change now is {num}")

  if num < -0.10:
    send_mail(num)

main()
