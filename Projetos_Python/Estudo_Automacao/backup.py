gimport os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from openpyxl import Workbook
import logging


# Recebe o nome do cargo e a cidade para preenchar na barra de pesquisa da pagina de vagas
def cargo_desejado():
    nome_vaga = 'Confeiteiro'
    cidade = 'Campinas'
    return nome_vaga, cidade

# Faz a leitura do arquivo que contém os dados de login
def ler_senha():
    # Recebe qual é o nome do usuário que está logado, que posteriormente é utilizado na variavel para preencer a localização do txt com o login e senha
    user = os.getlogin()
    arquivo_senha = fr'c:\Users\{user}\Desktop\credentials.txt'
    # Se não encontrar o arquivo, retorna informando
    if not os.path.exists(arquivo_senha):
        raise FileNotFoundError(f"Arquivo {arquivo_senha} não encontrado.")
    # Caso o arquivo seja encontrado, faz a leitura, e se não estiver preenchido, retorna com o erro
    with open(arquivo_senha, 'r') as arquivo:
        lines = arquivo.readlines()
        if len(lines) < 2:
            raise ValueError("Arquivo de credenciais deve conter pelo menos duas linhas (usuário e senha).")
        #Remove espaços em branco
        username = lines[0].strip()
        password = lines[1].strip()
    return username, password

def iniciar_sessao():
    #Inicia o navegador, redireciona para a pagina de login e maximiza a janela para garantir que o selenium vai ver todos os elementos
    navegador = webdriver.Chrome()
    navegador.get('https://www.linkedin.com/login/')
    navegador.maximize_window()
    return navegador

def login(navegador, username, password):
    # Localiza os campos de inserir login e senha pelo id - 
    username_field = navegador.find_element("id", "username")
    password_field = navegador.find_element("id", "password")
    # Preenche os campos utilizando o retorno da função ler_senha
    username_field.send_keys(username)
    password_field.send_keys(password)
    # Localiza e clica no botão entrar
    botao_entrar = navegador.find_element("xpath", "//button[contains(@class, 'btn__primary')]")
    botao_entrar.click()

def acessar_vaga(navegador):
    # Aguarda até 10 segundos para localizar o xpath do botão vagas no menu superior, e quando encontra, ele clica. Se não encontrar, o codigo quebra -

    btn_vaga_xpath = '//*[@id="global-nav"]/div/nav/ul/li[3]/a'
    btn_vaga = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, btn_vaga_xpath)) 
    )
    btn_vaga.click()

def inserir_cargo(navegador, nome_vaga):
    # Tenta localizar campo de input do nome da vaga e preenche caso ache com a variavel nome_vaga 
    input_vaga_xpath = '//header//input'
    input_vaga = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, input_vaga_xpath)) 
    )
    input_vaga.click()
    input_vaga.send_keys(f'{nome_vaga}')

def inserir_cidade(navegador, cidade):
    # Tenta localizar campo de input da cidade e preenche caso ache com a variavel cidade, aguarda abrir a barra com as cidades, aperta a seta pra baixo e seleciona a primeira delas 
    input_cidade = navegador.find_element("xpath", '//*[contains(@aria-label, "Cidade")]')
    input_cidade.clear()
    input_cidade.send_keys(cidade)
    sleep(2)
    input_cidade.send_keys(Keys.ARROW_DOWN)
    input_cidade.send_keys(Keys.RETURN)

def rolar_scroll(navegador, pixels):
    # Essa função tenta localizar a div das vagas onde está contida a barra de rolagem, e após encontrar, desce a quantidade de pixels estipuladas 
    ul_element = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[1]/div"))
    )
    navegador.execute_script(f"arguments[0].scrollTop += {pixels};", ul_element)

# Para cada link de vaga encontrado, rola o scroll do mouse e faz a captura
def salvar_links(navegador, nome_vaga):
    links_coletados = []
    for _ in range(25):
        rolar_scroll(navegador, 200)
        # Esse xpath é sobre a barra de rolagem 
        links = navegador.find_elements(By.XPATH, "//main//div/div//ul//li//a[@data-control-id]")
        # Aqui ele está fazendo apenas a leitura da quantiade de vagas encontradas na pagina para printar na tela
        if len(links) >= 25: 
            print(f'Coletadas {len(links)} vagas')
            break
    # Para cada link coletado, ele vai puxar o texto que está no parametro aria-label e o link e vai fazer um append na lista. No final do codigo ele retorna essa lista para ser utilizada        
    for link in links:
        text = text = link.find_element(By.XPATH, ".//span[not(@class='visually-hidden')]").text
        url_link = link.get_attribute("href")
        links_coletados.append((text, url_link))

    return links_coletados

def avancar_pagina(navegador, todas_vagas, nome_vaga):
    try:
        # Encontra o xpath do botão da proxima pagina e clica 
        pagina_atual = navegador.find_element(By.XPATH, "//button[@aria-current='page']").text
        proxima_pagina = int(pagina_atual) + 1
        xpath_proxima_pagina = f"//button[@aria-label='Página {proxima_pagina}']"

        botao_proxima_pagina = WebDriverWait(navegador, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpath_proxima_pagina))
        )
        # Enquanto estiver encontrando a proxima pagina, ele clica
        botao_proxima_pagina.click()
        print(f"Avançando para a página {proxima_pagina}...")
        return True
    except Exception as e:
        # Se ele não encontra proxima pagina, ele cai na clausula de erro, e nesse caso eu mando salvar os links
        print("Não foi possível avançar de página:", )
        salvar_excel(todas_vagas, nome_vaga)
        print("Extração finalizada")
        return False
    
def salvar_excel(todas_vagas, nome_vaga):
    # Essa função cria a planilha e pega todos os dados retornados na lista links_coletados e vai preenchendo
    spreadsheet = Workbook()
    sheet = spreadsheet.active
    sheet['A1'] = "NOME DA VAGA"
    sheet['B1'] = "LINK DA VAGA"
    next_line = sheet.max_row + 1

    for text, url_link in todas_vagas:
        sheet[f'A{next_line}'] = text
        sheet[f'B{next_line}'] = url_link
        next_line += 1

    spreadsheet.save(f"vagas_links-{nome_vaga}.xlsx")
    print("Planilha criada com sucesso!")

def iniciar_automacao():
    nome_vaga, cidade = cargo_desejado()
    navegador = iniciar_sessao()
    username, password = ler_senha()
    login(navegador, username, password)
    acessar_vaga(navegador)
    sleep(5)
    inserir_cargo(navegador, nome_vaga)
    inserir_cidade(navegador, cidade)
    sleep(5)

    todas_vagas = []

    while True:
        vagas = salvar_links(navegador, nome_vaga)
        if not vagas:
                break
        todas_vagas.extend(vagas)
        if avancar_pagina(navegador, todas_vagas, nome_vaga) == False:
                break