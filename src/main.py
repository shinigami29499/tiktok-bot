import random
import threading
import time
from io import TextIOWrapper
from os.path import exists
from random import randint
from threading import Thread
from typing import NoReturn

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth

chat: list[str] = ["1", "2", "3", "4", "6"]
timers: list[str] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
variables: list[str] = [
    "https://www.tiktok.com/login/phone-or-email/email",
    "//input[@placeholder='Email or username']",
    "//input[@placeholder='Password']",
    "//button[@type='submit']",
]


default_time_out = 1
default_wait_gap = 0
default_sleep_gap = 0.01

with open("live_stream_link.txt") as f:
    live_stream_link: str = f.readlines()[0]


options = webdriver.ChromeOptions()

options.add_argument("--no-sandbox")
options.add_argument("--no-default-browser-check")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-default-apps")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)


class Bot:
    # with open("user.txt") as f:
    #     line: list[str] = f.readlines()
    # username: str = line[0][10:-1]
    # password: str = line[1][10:-1]

    def __init__(self, user_name_v: str, user_password_v: str) -> None:
        super().__init__()
        self.username: str = user_name_v
        self.password: str = user_password_v
        self.balancer = 9

        self.create_driver()
        self.field_form: WebElement
        self.button: WebElement
        self.chat_box: WebElement

    def sleeper(self) -> None:
        time.sleep(
            float(
                "0."
                + random.choice(timers[0:3])
                + random.choice(timers[0:4])
                + random.choice(timers[0:9])
            )
        )

    def logging_in(self) -> None:
        self.driver.get(variables[0])

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, variables[1]))
            )
            self.field_form: WebElement = self.driver.find_element(
                "xpath", variables[1]
            )
        except:
            self.driver.quit()
        finally:
            for i in self.username:
                self.field_form.send_keys(i)
                self.sleeper()

        self.field_form = self.driver.find_element("xpath", variables[2])
        for i in self.password:
            self.field_form.send_keys(i)
            self.sleeper()

        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, variables[3]))
            )
        except:
            self.driver.quit()
        finally:
            self.button: WebElement = self.driver.find_element("xpath", variables[3])
            self.button.click()

    def is_logged_in(self) -> None:
        return self.driver.current_url != variables[0]

    def login(self) -> None:
        self.logging_in()
        while not self.is_logged_in():
            continue

    def create_driver(self) -> None:
        self.driver = uc.Chrome(use_subprocess=True, headless=False)

        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

    def run(self) -> NoReturn:
        self.driver.get(live_stream_link)

        self.chat_box: WebElement | None = self.find_element_by_xpath(
            "/html/body/div[1]/main/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div[3]/div[1]/div/div[1]/div"
        )
        while self.chat_box == None:
            self.chat_box: WebElement | None = self.find_element_by_xpath(
                "/html/body/div[1]/main/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[3]/div/div[3]/div[1]/div/div[1]/div"
            )

        while True:
            self.bot_chat()
            self.bot_sleep()

    def find_element_by_xpath(self, xpath: str) -> WebElement | None:
        self.time_run = 0
        while self.time_run < default_time_out:
            try:
                self.web_element: WebElement = self.driver.find_element(By.XPATH, xpath)
                if self.web_element == None:
                    continue
                time.sleep(default_wait_gap)
                return self.web_element
            except:
                self.time_run += default_sleep_gap
                time.sleep(default_sleep_gap)
        return None

    def bot_sleep(self) -> None:
        time.sleep(randint(2, 5))

    def bot_chat(self) -> None:
        self.random_choice: int = randint(0, 9)
        self.random_choice -= self.balancer
        if self.random_choice > 1:
            self.chat_content: str = "6"
            self.balancer += 1
        else:
            self.chat_content: str = random.choice(chat[0:3])
            self.balancer = 0

        self.chat_box.send_keys(self.chat_content)
        self.chat_box.send_keys(Keys.ENTER)


class Account:
    user_email: str
    user_password: str


def read_txt_file(file_name: str) -> list[Account]:
    file_exists: bool = exists(file_name)
    if not file_exists:
        open(file_name, "w")

    file: TextIOWrapper = open(file_name, "r")
    lines: list[str] = file.readlines()

    accounts: list[Account] = []
    for line in lines:
        account_info: list[str] = line.split("|")
        nAccount = Account()
        nAccount.user_email = account_info[2]
        nAccount.user_password = account_info[1]
        accounts.append(nAccount)
    return accounts


def main() -> None:
    # Get list accounts
    accounts: list[Account] = read_txt_file("Accounts.txt")
    # Create bot
    threads: list[Thread] = []
    for account in accounts:
        nThread = CreateBot(account)
        nThread.start()
        time.sleep(0.5)
        threads.append(nThread)

    for thread in threads:
        thread.join()


class CreateBot(Thread):
    def __init__(self, account: Account) -> None:
        super().__init__()
        self.username: str = account.user_email
        self.password: str = account.user_password
        self.bot = Bot(self.username, self.password)

    def run(self) -> None:
        self.bot.login()
        self.bot.run()


main()
