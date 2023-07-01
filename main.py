from requests.auth import HTTPProxyAuth
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from random import randint
from selenium.webdriver.firefox.options import Options as CustomFireFoxOptions
from bs4 import BeautifulSoup
import json


def main():
    driver = iniciar_driver()

    html_elementos = extraer_tweets(driver)

    resultados = extraer_informacion_tweets(html_elementos)

    guardar_resultados(resultados)

def iniciar_driver():
    browser_option = CustomFireFoxOptions()
    browser_option.add_argument('--profile=/home/agustin/.mozilla/firefox/tgx4az00.default-release')

    driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()), options=browser_option)
    
    # Abrir Twitter
    driver.get("https://twitter.com/elonmusk")

    return driver

def extraer_tweets(driver):
    # Definir la distancia del scroll automatico
    altura = 400
    
    # Extraer los primeros tweets
    all_ready_fetched_posts = []
    present_tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
    all_ready_fetched_posts.extend(present_tweets)
    html_elementos = []
    while len(html_elementos) < 10:
        for tweet in present_tweets:
            try:
                # Almacenar el contenido HTML
                elemento = tweet.get_attribute('innerHTML')
                html_elementos.append(elemento)
            except Exception as e:
                print(e)

        # Scroll pagina
        driver.execute_script(f"window.scrollTo(0, {altura});")
        altura += 400

        # Realizar una espera
        wait_until_completion(driver)
        wait_until_tweets_appear(driver)

        # Seleccionar todos los twits que encuentra
        present_tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')

        # Guardar unicamente lo twits nuevos
        present_tweets = [post for post in present_tweets if post not in all_ready_fetched_posts]
        all_ready_fetched_posts.extend(present_tweets)
        print(f"Twets Encontrados: {len(html_elementos)}")
    return html_elementos

def extraer_informacion_tweets(html_elementos):
    resultados = []
    for elemento in html_elementos:
        resultado = {}
        with open("elemento.html","w") as archivo:
            archivo.write(elemento)
        with open("elemento.html") as archivo:
            soup = BeautifulSoup(archivo, "html.parser")
            # Cabecera Tweet
            print("Cabecera")
            cabeceras = soup.find_all('div', attrs={'data-testid': 'User-Name'})
            for cabecera in cabeceras:
                etiquetas_a = cabecera.find_all('a')
                if len(etiquetas_a) > 0:
                    # Extraer Nombre Perfil
                    nombre_usuario = etiquetas_a[0].find_all('span')
                    if len(nombre_usuario) > 0:
                        print(f"Nombre: {nombre_usuario[0].text.strip()}")
                        resultado['nombre'] = nombre_usuario[0].text.strip()
                    
                    # Extraer usuario
                    usuario = etiquetas_a[1].find_all('span')
                    if len(usuario) > 0:
                        print(f"Usuario: {usuario[-1].text.strip()}")
                        resultado['usuario'] = usuario[-1].text.strip()

                    # Extraer fecha publicacion
                    for etiqueta_a in etiquetas_a:
                        et_time = etiqueta_a.find_all('time')
                        if len(et_time) > 0:
                            tiempo = ""
                            for t in et_time:
                                tiempo += t.text
                            print(f"Fecha: {tiempo.strip()}")
                            resultado['fecha'] = tiempo.strip()

            # Extraer contenido Tweet
            articulos_contenido = soup.find_all('div', attrs={'data-testid': 'tweetText'})
            for etiqueta in articulos_contenido:
                span = etiqueta.find_all('span')
                contenido_span = ""
                if span is not None:
                    for texto in span:
                        contenido_span += texto.text
                    print(f"Contenido: {contenido_span.strip()}")
                    resultado['contenido'] = contenido_span.strip()
            # Foto
            contenido_foto = soup.find_all('div', attrs={'data-testid': 'tweetPhoto'})
            if len(contenido_foto) > 0:
                for foto in contenido_foto:
                    img = foto.find('img')
                    if img is not None:
                        src = img.get('src')
                        print(f"Imagen: {src}")
                        resultado['imagen'] = src

            # Comentarios
            contenido_comentario = soup.find_all('div', attrs={'data-testid': 'reply'})
            for comentario in contenido_comentario:
                span = comentario.find('span')
                print(f"Numero Comentarios: {span.text}")
                resultado['num_comentarios'] = span.text

            # Retweets 
            contenido_retweet = soup.find_all('div', attrs={'data-testid': 'retweet'})
            for retweet in contenido_retweet:
                span = retweet.find('span')
                print(f"Numero Retweets: {span.text}")
                resultado['num_retweets'] = span.text

            # Likes 
            contenido_like = soup.find_all('div', attrs={'data-testid': 'like'})
            for like in contenido_like:
                span = like.find('span')
                print(f"Numero Likes: {span.text}")
                resultado['num_likes'] = span.text

            print("---------------------")
        resultados.append(resultado)
    return resultados

def guardar_resultados(resultados):
    with open("resultados.json","w") as file:
        json.dump(resultados,file)

def wait_until_tweets_appear(driver) -> None:
    """Wait for tweet to appear. Helpful to work with the system facing
    slow internet connection issues
    """
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="tweet"]')))
    except WebDriverException:
        print("Tweets did not appear!, Try setting headless=False to see what is happening")

def wait_until_completion(driver) -> None:
    """waits until the page have completed loading"""
    try:
        state = ""
        while state != "complete":
            time.sleep(randint(3, 5))
            state = driver.execute_script("return document.readyState")
    except Exception as ex:
        print('Error at wait_until_completion: {}'.format(ex))


main()
