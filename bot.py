import string
import random
import re
from random import randrange
from datetime import timedelta
from datetime import datetime
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
import undetected_chromedriver.v2 as uc
from config import api_key_for_2captcha
import os
from selenium.common.exceptions import NoSuchElementException


class DiscordBot:

    # simple chromedriver
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_extension('extension_3_0_8_0.crx')
        options.set_capability('unhandledPromptBehavior', 'accept')
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        self.driver.maximize_window()
        time.sleep(1)
        self.login_2captcha_extension()

    # undetected selenium, with him login to 2captcha not working, i don't no why
    """
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument('--load-extension=' + os.path.abspath("extension_3_0_8_0"))
        options.set_capability('unhandledPromptBehavior', 'accept')
        self.driver = uc.Chrome(executable_path="chromedriver.exe", options=options)
        self.driver.maximize_window()
        time.sleep(1)
        self.login_2captcha_extension()
    """

    def close_all_tabs_without_first(self):
        first = True
        first_handle = self.driver.window_handles[0]
        for handle in self.driver.window_handles:
            if first is True:
                first = False
                continue
            self.driver.switch_to.window(handle)
            self.driver.close()
        self.driver.switch_to.window(first_handle)

    def login_2captcha_extension(self):
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(2)
        self.driver.find_element(By.XPATH, value="//*[@id=\"autoSolveHCaptcha\"]").click()
        self.driver.find_element(by=By.XPATH, value="/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input").send_keys(
            api_key_for_2captcha)
        self.driver.find_element(by=By.ID, value="connect").click()
        time.sleep(5)

    @staticmethod
    def generate_password(len_password: int) -> str:
        lowercase = list(string.ascii_lowercase)
        uppercase = list(string.ascii_uppercase)
        letters = list(string.digits)
        password = ""
        for i in range(len_password):
            random_number_for_type_symbol = random.randint(1, 3)
            if random_number_for_type_symbol == 1:
                random_symbol = lowercase[random.randint(0, len(lowercase) - 1)]
            elif random_number_for_type_symbol == 2:
                random_symbol = uppercase[random.randint(0, len(uppercase) - 1)]
            else:
                random_symbol = letters[random.randint(0, len(letters) - 1)]
            password = password + random_symbol
        return password

    @staticmethod
    def validate_email(email: str) -> bool:
        if type(email) is not str:
            return False
        if len(email) < 7 or len(email) > 100:
            return False
        if re.search("^[a-zA-Z0-9]+@[a-zA-Z0-9]{4,}\.[a-zA-Z0-9]{2,}$", email) is None:
            return False
        return True

    @staticmethod
    def validate_nickname(nickname: str) -> bool:
        if type(nickname) is not str:
            return False
        if len(nickname) < 3 or len(nickname) > 50:
            return False
        if re.search("^[a-zA-Z0-9]+$", nickname) is None:
            return False
        return True

    @staticmethod
    def random_datetime(start: datetime, end: datetime) -> datetime:
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    def get_cookies_from_selenium(self) -> dict:
        all_cookies = self.driver.get_cookies()
        cookies_dict = {}
        for cookie in all_cookies:
            cookies_dict[cookie['name']] = cookie['value']
        return cookies_dict

    def click_on_month_in_register(self, number_month: int):
        number_month = number_month - 1
        months_in_english = ["january", "february", "march", "april", "may", "june", "july", "august",
                             "september", "october", "november", "december"]
        months_in_russian = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь",
                             "октябрь", "ноябрь", "декабрь"]
        months_in_ukranian = ["січень", "лютий", "березень", "квітень", "травень", "червень", "липень",
                              "серпень", "вересень", "жовтень", "листопад", "грудень"]

        label = self.driver.find_element(by=By.CLASS_NAME,
                                         value="heading-xl-medium-_XBxHT.defaultColor-HXu-5n.title-3FQ39e").text
        if "Создать" in label:
            month = months_in_russian[number_month]
        elif "Створити" in label:
            month = months_in_ukranian[number_month]
        else:
            month = months_in_english[number_month]
        self.driver.find_element(by=By.CLASS_NAME, value="month-1Z2bRu").click()
        time.sleep(3)
        self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), '{month}')]").click()

    """
    def try_solve_captcha(self):

        time.sleep(1)
        captcha = self.driver.find_element(
            by=By.XPATH, value="//*[@id=\"app-mount\"]/div[2]/div/div[1]/div/div/div/section/div/div[2]/div/iframe")
        src_captcha = captcha.get_attribute("src")
        sitekey = re.search("sitekey=.+&", src_captcha).group(0)[8:-1]
        print("sitekey=", sitekey)
        time.sleep(4)


        g_recaptcha = self.driver.find_element(by=By.XPATH, value='//textarea[@name="g-recaptcha-response"]')
        h_recaptcha = self.driver.find_element(by=By.XPATH, value='//textarea[@name="h-captcha-response"]')
        self.driver.execute_script("arguments[0].setAttribute('style',arguments[1])", g_recaptcha, "")
        self.driver.execute_script("arguments[0].setAttribute('style',arguments[1])", h_recaptcha, "")
        time.sleep(5)


        frame_with_captcha = self.driver.find_element(
            By.XPATH, '//iframe[@title="widget containing checkbox for hCaptcha security challenge"]')
        self.driver.switch_to.frame(frame_with_captcha)
        self.driver.switch_to.default_content()

    """

    def create_account(self, email: str, nickname: str):

        d1 = datetime.strptime('1/1/1940 1:30 PM', '%m/%d/%Y %I:%M %p')
        d2 = datetime.strptime('1/1/2005 4:50 AM', '%m/%d/%Y %I:%M %p')

        date_of_birth = self.random_datetime(d1, d2).date()
        password = self.generate_password(8)

        self.driver.get("https://discord.com/register")
        time.sleep(3)
        self.driver.find_element(by=By.NAME, value="email").send_keys(email)
        self.driver.find_element(by=By.NAME, value="username").send_keys(nickname)
        self.driver.find_element(by=By.NAME, value="password").send_keys(password)
        self.driver.find_element(by=By.XPATH, value="//*[@id=\"react-select-2-input\"]").send_keys(date_of_birth.day)
        self.click_on_month_in_register(date_of_birth.month)
        self.driver.find_element(by=By.XPATH, value="//*[@id=\"react-select-4-input\"]").send_keys(date_of_birth.year)
        time.sleep(5)
        self.driver.find_element(by=By.XPATH, value="//button[@type=\"submit\"]").click()
        time.sleep(5)

        if self.check_error_with_data():
            self.driver.close()
            self.driver.quit()
            return
        if self.check_error_if_already_captcha():
            self.driver.close()
            self.driver.quit()
            return
        print("captcha start solving by extension")
        time.sleep(100)

    def check_error_with_data(self):
        try:
            error = self.driver.find_element(by=By.CLASS_NAME, value="errorMessage-1kMqS5")
            print("error=", error.text)
            return True
        except NoSuchElementException:
            return False

    def check_error_if_already_captcha(self):
        try:
            self.driver.find_element(by=By.XPATH, value='//textarea[@name="g-recaptcha-response"]')
            return False
        except NoSuchElementException:
            print("error = maybe error with input data, button submit not clicked")
            return True


