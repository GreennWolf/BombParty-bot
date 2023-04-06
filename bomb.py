import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from nltk.corpus import wordnet
import string
import time
from selenium.common.exceptions import NoSuchElementException
import nltk

import requests

import re
nltk.download('wordnet')

chromedriver_path = "C:\\Users\\juanm\\Desktop\\bomb\\chromedriver"
os.environ["PATH"] += os.pathsep + chromedriver_path

options = webdriver.ChromeOptions()
options.binary_location = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
driver = webdriver.Chrome(options=options)
driver.get("https://jklm.fun/")
driver.implicitly_wait(10)

room_code_input = driver.find_element(
    By.CSS_SELECTOR, ".home .joinRoom form input")
room_code_input.clear()
room_code_input.send_keys("UNRG")
room_code_input.send_keys(Keys.RETURN)
time.sleep(5)

username_input = driver.find_element(
    By.CSS_SELECTOR, ".setNickname.page input.nickname")
username_input.send_keys(Keys.BACK_SPACE)
username_input.send_keys("NadieMeGana")
username_input.send_keys(Keys.RETURN)
time.sleep(5)


def wait_for_element(selector, timeout=10):
    try:
        element_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, selector))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Tiempo de espera agotado para encontrar el elemento: " + selector)


def parse_page():
    letters_element = None

    while letters_element is None:
        try:
            driver.switch_to.default_content()
            print('buscando elemento')

            iframe_element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".game iframe"))
            )
            print(iframe_element)
            iframe_src = iframe_element.get_attribute("src")

            print("El atributo src del iframe es:", iframe_src)

            driver.switch_to.frame(iframe_element)
            letters_element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".middle .round .syllable"))
            )
            print(letters_element.text, 'syllable')
        except TimeoutException:
            print("No se encontró el elemento syllable. Intentando nuevamente...")

    letters_string = letters_element.text
    available_letters = letters_string
    print('final', available_letters)

    # Como no hay un elemento para palabras jugadas y puntajes,
    # simplemente utilizaremos conjuntos vacíos para representarlos
    played_words = set()
    scoreboard = set()

    return available_letters, played_words, scoreboard


def is_element_hidden(element):
    return element.get_attribute("hidden") is not None


def send_word(word):
    if not word:
        return

    inputContainer = None

    while inputContainer is None:
        css_container = ".selfTurn"

        try:
            inputContainer = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, css_container))
            )
        except TimeoutException:
            print("No se pudo encontrar el elemento de entrada anashe")

        is_visible = is_element_hidden(inputContainer)

        if is_visible:
            print('Input no está visible')
        else:
            textInput = driver.find_element(
                By.CSS_SELECTOR, ".selfTurn input")
            textInput.send_keys(word)
            textInput.send_keys(Keys.RETURN)


def join():
    joinBtn = None

    while joinBtn is None:
        css_container = ".join"

        try:
            joinBtn = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, css_container))
            )
        except TimeoutException:
            print("No se pudo encontrar el botón de unirse")

        is_visible = is_element_hidden(joinBtn)

        if is_visible:
            print('Botón de unirse no está visible')
        else:
            joinB = driver.find_element(
                By.CSS_SELECTOR, "button.styled")
            joinB.click()


def choose_word(game_info, used_words=[]):
    center_letters, played_words, scoreboard = game_info

    available_letters = "".join(center_letters)

    # Leer el archivo de texto del diccionario y cargar todas las palabras en una lista
    with open("C:\\Users\\juanm\\Desktop\\bomb\\diccionario.txt", encoding="utf-8") as f:
        all_words = [line.strip() for line in f]

    # Buscar palabras que contengan todas las letras disponibles en el orden correcto
    available_words = set()

    if center_letters != '':
        print(center_letters, ' avaible lettr')
        silaba = str(available_letters).lower()
        print(silaba)
        for word in all_words:
            if silaba in word:
                available_words.add(word)

    # Elegir la primera palabra de mayor longitud que no se haya jugado antes
    for word in available_words:
        if word not in used_words:
            chosen_word = word
            break
    else:
        chosen_word = ""

    used_words.append(chosen_word)

    print(chosen_word, 'choseeen')
    return chosen_word, used_words


used_words = []
while True:

    game_info = parse_page()
    # join()
    chosen_word, used_words = choose_word(game_info, used_words)
    send_word(chosen_word)
    time.sleep(3)
