from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import smtplib
import time


def main():
    # Your max budget
    max_price = 70000
    url = "https://www.kijijiautos.ca/cars/#od=down&sb=ct"
    car_info = []

    driver = webdriver.Chrome()
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.CLASS_NAME, '_3u466m36pAjbJF3m4gZEwr')))
    except TimeoutException:
        print('Page timed out after 10 secs.')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.quit()

    car_elems = soup.findAll(
        "div", class_="_2HOXt4_JUGriV5QrKxi-Be _2pZK6skcaaZg4HoaZda9Rl")

    car_info = generate_car_info(car_elems, car_info)

    # Navigating through the search page accessing each car
    # for link in soup.find_all('a'):
    #    print(link.get('href'))

    for car in car_info:
        if(car[0] < max_price):
            email_ask(car)


def generate_car_info(car_elems, car_info):

    for car_elem in car_elems:
        price = car_elem.find(
            'span', class_='_2zkxeQN7m4FOG4I3VDi6Ue _2EdRVi2tLqR7VPkJ2yR6Zx QVJux59ueO-M7o0DZZ6Vx _14Nqyg9Gv-h-nJ_lZalHW_').get_text()
        try:
            price = int(price.replace('$', '').replace(',', ''))
        except:
            ValueError
        description = car_elem.find(
            'h2', class_='_3P8AQT5NHSjIV5w66Q182w _3okhtoMhqThVhoq94SeapG _38CFNcqLlJdgoyDxNk2Vcf _14Nqyg9Gv-h-nJ_lZalHW_').get_text()
        car_info.append([price, description])
    return car_info

# Asks users if they want email with car info sent to them


def email_ask(car_info):

    confirmation = input(
        "Match found! Would you like to have an email sent? (y/n)")
    while(confirmation != 'y' and confirmation != 'n'):
        confirmation = input(
            "Please enter a valid input (y/n)")
        confirmation = confirmation.lower()
    if(confirmation == 'y'):
        send_email(car_info)
        print("E-mail sent to " + user_email + "!")
    else:
        print("Got it, e-mail won't be sent!")


# Sends user the email
def send_email(car):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # enter your sender email and 2 step verification password (could be a bot acc)
    server.login('sampleemail@.com', 'samplepasswowrd')
    subject = 'Car: ' + str(car[0])
    body = 'The price is ' + car[1]

    message = f"Subject: {subject}\n\n{body}"

    # enter target receiver's email
    server.sendmail('sampleemail@.com', message)
    print("Match found! Email sent")
    server.quit()


if __name__ == '__main__':
    main()
