from cgitb import text
from http.client import ResponseNotReady
import this
from cv2 import CAP_PROP_XI_TEST_PATTERN_GENERATOR_SELECTOR
import speech_recognition as sr
import re
import pyttsx3
import speedtest
from ping3 import ping
from datetime import datetime
import subprocess
import wmi
import psutil
import random
import pathlib
from pathlib import Path
from os import path
import os
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from rembg import remove
from PIL import Image
import requests
import wikipedia
import GPUtil

nome = ""

def falar(engine, frase):
    engine.say(frase)
    engine.runAndWait()

def velocidade_internet():
    speed = speedtest.Speedtest()
    speed.get_servers()
    speed.get_best_server()
    velocidade_download = round(speed.download(threads=None)*(10**-6))
    velocidade_upload = round(speed.upload(threads=None)*(10**-6))
    return velocidade_download, velocidade_upload

def pingar_site(host):
    resposta = ping(host, unit='ms')
    if resposta == False:
        return False
    else:
        return resposta

def abrir_programa(programa):
    subprocess.run(programa, shell=True)


def pegar_cpu_temp():
    w = wmi.WMI(namespace="root\OpenHardwareMonitor")
    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
        if sensor.SensorType==u'Temperature':
            print(sensor.Name)
            print(sensor.Value)

def pegar_temperatura_gpu():
    return GPUtil.getGPUs()[0]

def uso_cpu():
    return psutil.cpu_percent(4)

def uso_ram():
    return psutil.virtual_memory()[2]

def cotar_moeda(moeda):
    cotacoes = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL')
    if cotacoes.status_code == 200:
        dolar = cotacoes.json()['USDBRL']['bid']
        euro = cotacoes.json()['EURBRL']['bid']
        bitcoin = cotacoes.json()['BTCBRL']['bid']
        if moeda == 'dolar':
            return f'O dolar americano está cotado em {dolar[:4]} reais'
        elif moeda == 'euro':
            return f'O euro equivale a {euro[:4]} reais'
        elif moeda == 'bitcoin':
            return f'O bitcoin esta cotado em {bitcoin[:4]} reais'
        else:
            return 'Desculpe. não entendi qual a moeda que você quer saber a cotação'
    else:
        return f'Desculpe, não conseguir verificar a cotação do {moeda}'

def comando_voz():
    respostas_padrao = ['Ok', 'Tudo bem', 'Certo', 'Sem problemas', 'Ãrrã', 'Um momento por favor.', 'Irei verificar']
    while(True):
        microfone = sr.Recognizer()

        with sr.Microphone() as source:
            engine = pyttsx3.init()

            engine.setProperty('voice', "com.apple.speech.synthesis.voice.luciana")
            microfone.adjust_for_ambient_noise(source)

            print("Vamos começar, diga um comando...")

            audio = microfone.listen(source)

            try:
                frase = mic.recognize_google(audio,language='pt-BR')
                frase = frase.lower()
                
                if (re.search(r'\b' + "ajuda" + r'\b',format(frase))):
                    falar(engine, "Você precisa de ajuda?")
                    print("Algo relacionado a ajuda.")

                elif (re.search(r'\b' + "meu nome é " + r'\b',format(frase))):
                    t = re.search('meu nome é (.*)',format(frase))
                    nome = t.group(1)
                    print("Seu nome é "+nome)
                    respostas = ["Legal. O seu nome é "+nome, nome+" É um nome bonito", nome + " é um nome muito chique", nome+"é um nome muito bonito"]
                    resposta = respostas[random.randint(0, len(respostas)-1)]
                    falar(engine, resposta)

                elif (re.search(r'\b' + "qual é o seu nome" + r'\b',format(frase))):
                    respostas = ["meu nome é Lorena", "Me chamo Lorena", "O nome mais bonito que tem. Lorena", "Lorena. Que por sinal é um nome maravilhoso"]

                    falar(engine, random.choice(resposta))

                elif (re.search(r'\b' + "tomar um cafezinho" + r'\b',format(frase)) or re.search(r'\b' + "vamos tomar um cafezinho" + r'\b',format(frase))):
                    respostas = ["Só se for para tomar um cafézinho e comer um queijo", "Só se for agora", "Vamos sim. Minha barriga esta roncando", "Boa ideia. Estou com fome"]
                    falar(engine, random.choice(resposta))

                elif (re.search(r'\b' + "o que você acha de um café com queijo" + r'\b',format(frase))):
                    respostas = ["Uai, esse trem é bom demais da conta, so", "Num tem trem mió que isso", "Uai, esse trem é muito bom. nó", "Uai, isso sim é um trem bão"]
                    falar(engine, random.choice(resposta))

                elif (re.search(r'\b' + "gosta de comer" + r'\b',format(frase))):
                    falar(engine, "Uai. Eu gosto de queijo com doce de leite, torresmo, uma pizza top")
                
                elif (re.search(r'\b' + "que dia é hoje" + r'\b',format(frase))):
                    dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira',
                    'Quinta-Feira', 'Sexta-feira', 'Sábado', 'Domingo']
                    data_atual = datetime.now().strftime('%d/%m/%Y')
                    data = datetime.now()
                    indice_da_semana = data.weekday()
                    dia_da_semana = dias[indice_da_semana]
                    falar(engine, f"Hoje é {dia_da_semana}, {data_atual}")

                elif (re.search(r'\b' + "que horas são" + r'\b',format(frase))) or (re.search(r'\b' + "horas" + r'\b',format(frase))):
                    hora_atual = datetime.now().strftime('%H:%M')
                    falar(engine, f"Agora são {hora_atual}")

                elif (re.search(r'\b' + "qual a velocidade da internet" + r'\b',format(frase))):
                    engine.say("Vou verificar para você. Por favor, aguarde alguns instantes. Isso pode demorar um pouco")
                    engine.runAndWait()
                    download, upload = velocidade_internet()
                    falar(engine, f"A velocidade do download é de {download} megas, e do upload é de {upload} megas")

                elif (re.search(r'\b' + "testar ping" + r'\b',format(frase))):
                    pings = []
                    for indice in range(4):
                        ping_atual = pingar_site("www.google.com.br")
                        pings.append(ping_atual)
                    media = int(sum(pings) / len(pings))
                    falar(engine, f"Temos conexão com a internet. A média do ping para o Google é de {media} mili segundos")

                elif (re.search(r'\b' + "abrir calculadora" + r'\b',format(frase))):
                    falar(engine, random.choice(respostas_padrao))
                    abrir_programa("calculadora.exe")

                elif (re.search(r'\b' + "abrir navegador" + r'\b',format(frase))):
                    falar(engine, random.choice(respostas_padrao))
                    abrir_programa("chrome.exe")

                elif (re.search(r'\b' + "Pesquise sobre " + r'\b',format(frase))):
                    t = re.search('pesquise sobre (.*)',format(frase))
                    item = t.group(1)
                    item.replace(' ', '+')
                    abrir_programa(f"chrome.exe https://www.google.com/search?q={item}&oq={item}")

                elif (re.search(r'\b' + "qual a temperatura da cpu" + r'\b',format(frase))) or (re.search(r'\b' + "qual a temperatura do processador" + r'\b',format(frase))):
                    temperatura = pegar_cpu_temp()
                    falar(engine, f"A temperatura do processador esta em {temperatura} graus")

                elif (re.search(r'\b' + "qual o uso da cpu" + r'\b',format(frase))) or (re.search(r'\b' + "qual o uso do processador" + r'\b',format(frase))):
                    utilizacao_cpu = uso_cpu()
                    falar(engine, f"A utilização do processador esta em {utilizacao_cpu} por cento")

                elif (re.search(r'\b' + "qual o uso da memória ram" + r'\b',format(frase))) or (re.search(r'\b' + "qual o uso da memória" + r'\b',format(frase))):
                    utilizacao_ram = uso_ram()
                    falar(engine, f"A utilização da memória ram é de {utilizacao_ram} por cento")

                elif (re.search(r'\b' + "criar pasta chamada (.*) em (.*)" + r'\b',format(frase))) or (re.search(r'\b' + "qual o uso da memória" + r'\b',format(frase))):
                    t = re.search('criar pasta chamada (.*) em (.*)',format(frase))
                    nova_pasta = t.group(1)
                    diretorio = t.group(2)
                    pasta_user = path.expanduser("~")
                    falar(engine, random.choice(respostas_padrao))

                    try:
                        path = Path(fr'{pasta_user}\{diretorio}\{nova_pasta}')
                        path.mkdir(parents=True, exist_ok=True)
                        falar(engine, f"Pasta {nova_pasta} criada")
                    except FileExistsError:
                        falar(engine, f"A pasta {nova_pasta} que você pediu para criar já existe no diretório {diretorio}")

                elif (re.search(r'\b' + "procurar pelo arquivo (.*)" + r'\b',format(frase))):
                    t = re.search('procurar pelo arquivo (.*)',format(frase))
                    arquivo_procurado = t.group(1)
                    diretorio = pathlib.Path(os.path.expanduser(fr"~\Documents"))
                    arquivos = diretorio.glob(f'**/{arquivo_procurado}.*')
                    for arquivo in arquivos:
                        print(arquivo)
                        falar(engine, f"Encontrei o arquivo {arquivo}")

                elif (re.search(r'\b' + "escreva o texto (.*)" + r'\b',format(frase))):
                    t = re.search('escreva o texto (.*)',format(frase))
                    texto = t.group(1)
                    abrir_programa("notpad.exe")
                    time.sleep(2)
                    pyautogui.write(texto)

                elif (re.search(r'\b' + "previsão do tempo" + r'\b',format(frase))):
                    options = webdriver.ChromeOptions()
                    options.add_argument("--headless")
                    driver = webdriver.Chrome(chrome_options=options)
                    driver.implicitly_wait(5)

                    driver.get("https://www.google.com/search?q=previs%C3%A3o+do+tempo+campinas&rlz=1C1GCEU_pt-BRUS1007US1007&oq=previs&aqs=chrome.0.69i59j69i57j0i512l8.4453j1j7&sourceid=chrome&ie=UTF-8")

                    temperatura_atual = driver.find_element(By.ID, "wob_tm").text

                    clima = driver.find_element(By.ID, 'wob_dc').text
                    porcent_chuva = driver.find_element(By.ID, 'wob_pp').text

                    porcent_umidade = driver.find_element(By.ID, 'wob_hm').text
                    vel_vento = driver.find_element(By.ID, 'wob_ws').text
                    driver.get('https://www.climatempo.com.br/previsao-do-tempo/cidade/418/campinas-sp')

                    temp_max = driver.find_element(By.ID, 'max-temp-1').text
                    temp_min = driver.find_element(By.ID, 'min-temp-1').text
                    qtde_porcent_chuva = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[4]/div[5]/div[1]/div[2]/div[2]/div[2]/div[1]/ul/li[2]/div/span').text
                    qtde_chuva = qtde_porcent_chuva[:4]
                    driver.quit()
                    falar(engine, f"A temperatura atual é de {temperatura_atual}, A previsão para hoje é de clima {clima}, a máxima para hoje é de {temp_max} e a minima é de {temp_min} e está previsto {porcent_chuva} de chuva")

                elif (re.search(r'\b' + "previsão do tempo para amanhã" + r'\b',format(frase))):
                    options = webdriver.ChromeOptions()
                    options.add_argument("--headless")
                    driver = webdriver.Chrome(chrome_options=options)
                    driver.implicitly_wait(5)

                    driver.get('https://www.climatempo.com.br/previsao-do-tempo/amanha/cidade/418/campinas-sp')

                    temp_max_amanha = driver.find_element(By.ID, 'max-temp-1').text
                    temp_min_amanha = driver.find_element(By.ID, 'min-temp-1').text
                    chuva_amanha = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[4]/div[5]/div[1]/div[2]/div[2]/div[2]/div[1]/ul/li[2]/div/span').text
                    driver.quit()
                    falar(engine, f"Para amanhã espere por {chuva_amanha}, com máxima prevista de {temp_max_amanha} e minima de {temp_min_amanha}")

                elif (re.search(r'\b' + "remova o fundo das imagens da pasta (.*)" + r'\b',format(frase))):
                    t = re.search('remover fundo das imagens da pasta (.*)',format(frase))
                    texto = t.group(1)
                    pasta_imagens = f'C:\\Users\\Lucas\\Pictures\\{texto}'
                    for diretorio, subpastas, arquivos in os.walk(pasta_imagens):
                        for arquivo in arquivos:
                            nome_arquivo_com_extencao = arquivo.split('.')
                            nome_arquivo = nome_arquivo_com_extencao[0]
                            print(nome_arquivo)
                            img = Image.open(f'C:\\Users\\Lucas\\Pictures\\Fotos\\{arquivo}')
                            img_sem_fundo = remove(img)
                            img_sem_fundo.save(f'C:\\Users\\Lucas\\Pictures\\Fotos\\sem_fundo_{nome_arquivo}.png')
                    falar(engine, 'Pronto, já removi os fundos das fotos que você me pediu.')

                elif (re.search(r'\b' + "quem é " + r'\b',format(frase))):
                    t = re.search('quem é (.*)',format(frase))
                    texto = t.group(1)
                    resultado = wikipedia.summary(text)
                    falar(engine, resultado)

                elif (re.search(r'\b' + "de um zoom" + r'\b',format(frase))):
                    pyautogui.hotkey('win', '+')

                elif (re.search(r'\b' + "tira o zoom" + r'\b',format(frase))):
                    pyautogui.hotkey('win', 'esc')

                elif (re.search(r'\b' + "sobe a tela" + r'\b',format(frase))):
                    pyautogui.scroll(-3)
                
                elif (re.search(r'\b' + "desce a tela" + r'\b',format(frase))):
                    pyautogui.scroll(-3)

                else:
                    falar(engine, 'Desculpe, não entendi o que você disse.')

                print("Voce falou: "+frase)

            except sr.UnknownValueError:
                print("Algo deu errado")


while(True):
    mic = sr.Recognizer()

    with sr.Microphone() as source:

        engine = pyttsx3.init()

        engine.setProperty('voice', "com.apple.speech.synthesis.voice.luciana")
        mic.adjust_for_ambient_noise(source)

        print("Vamos começar, fale alguma coisa...")

        audio = mic.listen(source)

        try:

            frase = mic.recognize_google(audio,language='pt-BR')
            frase = frase.lower()
            
            if (re.search(r'\b' + "lorena" + r'\b',format(frase))):
                t = re.search('lorena (.*)',format(frase))
                respostas = ["Olá", "Oi", "Pode falar", 'Em que posso lhe ajudar?', 'Estou aqui senhor']
                resposta = random.choice(respostas)
                falar(engine, resposta)

                comando_voz()
            print("Voce falou: "+frase)

        except sr.UnknownValueError:

            print("ops, algo deu errado.")


#Velocidade da internet
#https://dadosaocubo.com/velocidade-da-internet-com-a-biblioteca-speedtest-python/

#Velocidade do PING
#https://www.delftstack.com/pt/howto/python/python-ping/

#Abrir programas
#https://www.delftstack.com/pt/howto/python/call-external-programs-python/

#Verificar temperatura CPU e GPU
#https://www.programcreek.com/python/?CodeExample=get+cpu+temp
#https://stackoverflow.com/questions/62617789/get-cpu-and-gpu-temp-using-python-windows

#Previsão do tempo
#Selenium

#Uso de CPU, memoria RAM e Disco
#https://acervolima.com/como-obter-o-uso-atual-de-cpu-e-ram-em-python/#:~:text=O%20uso%20ou%20utiliza%C3%A7%C3%A3o%20da,podem%20ser%20recuperados%20usando%20python.

#Dizer o horario atual

#Fazer pesquisas na internet

#Manipular arquivos do computador (Copiar arquivos, criar pastas)

#Fazer pesquisa na Wikpedia

#Remover fundo de fotos

#Cotação do Real e moedas estrangeirasw