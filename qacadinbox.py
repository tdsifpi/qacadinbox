#!/usr/bin/env python3
#coding: utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests

login = input("Login: ")
senha = input("Senha: ")

path_exe = '' # put here path to chromedriver binary file
if path_exe == '':
    path_exe = input("Path to chromedriver binary file: ")

print("Fazendo Login...")

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=chrome_options, executable_path = path_exe)
url = 'https://academico.ifpi.edu.br/qacademico/index.asp?t=1001'
browser.get(url)
username = browser.find_element_by_id("txtLogin")
password = browser.find_element_by_id("txtSenha")
username.send_keys(login)
password.send_keys(senha)
browser.find_element_by_name("Submit").click()
all_cookies = browser.get_cookies()
browser.close()
sess = requests.Session()
check_login = sess.get('https://academico.ifpi.edu.br/qacademico/index.asp?t=2000',
        cookies={all_cookies[0]['name']:all_cookies[0]['value']})
if not 'Login={}'.format(login) in check_login.text:
    print('Login Invalido')
else:
    message_req = sess.get('https://academico.ifpi.edu.br/qacademicodotnet/mensagens.aspx',
        cookies={all_cookies[0]['name']:all_cookies[0]['value']})
    file = open('inbox.txt', "w+")
    file.write(message_req.text)
    file.close
    for line in open('inbox.txt', "r"):
        if 'exibir_mensagem' in line:
            print(line)

