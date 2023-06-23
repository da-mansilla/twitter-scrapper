from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from random import randint
from selenium.webdriver.firefox.options import Options as CustomFireFoxOptions
from fake_headers import Headers
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup




def scrape_twitter_profile():
    # Inicializar el driver de Selenium (asegúrate de tener el controlador adecuado para tu navegador instalado)
    # driver = webdriver.Firefox()

    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    
    # Abrir Twitter
    driver.get("https://twitter.com/elonmusk")

    # Esperar un momento para que la página cargue completamente
    # time.sleep(2)

    # Encontrar el campo de búsqueda y escribir el nombre de usuario
    # search_input = driver.find_element_by_xpath('//input[@placeholder="Buscar en Twitter"]')
    # search_input.send_keys(username)
    # search_input.send_keys(Keys.RETURN)

    # Esperar un momento para que se cargue la página de resultados de búsqueda
    time.sleep(2)

    # Encontrar el enlace del perfil y hacer clic
    # profile_link = driver.find_element_by_xpath('//a[contains(@href,"/{}")]'.format(username))
    # profile_link.click()

    # Esperar un momento para que se cargue el perfil
    # time.sleep(2)

    # Desplazarse por la página para cargar más publicaciones (ajusta el número de veces según tus necesidades)
    # for _ in range(3):
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(3)
        # driver.execute_script("window.scrollTo(0, 2500);")
    driver.execute_script("window.scrollTo(0, 2000);")
    publicaciones = driver.find_elements("xpath","//div[@data-testid='cellInnerDiv']")
    for publicacion in publicaciones:
        tweet = publicacion.find_element("xpath","//article[@data-testid='tweet']")
        print(tweet.text)
        print("-----------")


def main():
    browser_option = CustomFireFoxOptions()

    driver = webdriver.Firefox(service=FirefoxService(executable_path=GeckoDriverManager().install()), options=set_properties(browser_option))

    # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    
    # Abrir Twitter
    driver.get("https://twitter.com/elonmusk")
    # wait_until_tweets_appear(driver)
    time.sleep(20)
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.send_keys(Keys.ENTER)
    #
    all_ready_fetched_posts = []
    present_tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
    all_ready_fetched_posts.extend(present_tweets)
    twits_encontrados = {}
    # html = driver.find_element(By.TAG_NAME, 'body')
        # body = driver.find_element(By.CSS_SELECTOR, 'body')
    altura_anterior = 0
    altura = 400
    html_elementos = []
    while len(html_elementos) < 75:
        # actions.send_keys(Keys.ENTER)
        # body = driver.find_element(By.CSS_SELECTOR, 'body')
        # for _ in range(randint(1, 3)):
        # html.send_keys(Keys.ENTER)
        # html.location_once_scrolled_into_view
        # body = driver.find_element(By.CSS_SELECTOR, 'body')
        # body.send_keys(Keys.PAGE_DOWN)
        # html.send_keys(Keys.PAGE_DOWN)
        # time.sleep(1)
        # body.send_keys(Keys.ENTER)
        for tweet in present_tweets:
            try:
                elemento = tweet.get_attribute('innerHTML')
                html_elementos.append(elemento)
                # status, tweet_url = find_status(tweet)
                # username = tweet_url.split("/")[3]
                # anchor = tweet.find_element(By.CSS_SELECTOR, "a[aria-label][dir]")
                # status = status[-1]
                # content_element = tweet.find_element(By.CSS_SELECTOR, 'div[lang]').text
                # content_element = tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]').text
                # print("*************")
                # print(content_element)
                # twits_encontrados[status] = {
                #             "username": username,
                #             "content": content_element 
                # }
            except Exception as e:
                print(e)


        driver.execute_script(f"window.scrollTo(0, {altura});")
        altura += 400
        wait_until_completion(driver)
        wait_until_tweets_appear(driver)
        present_tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
        present_tweets = [post for post in present_tweets if post not in all_ready_fetched_posts]
        all_ready_fetched_posts.extend(present_tweets)
        print(f"Twets Encontrados: {len(html_elementos)}")


    for elemento in html_elementos:
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
                    nombre_usuario = etiquetas_a[0].find_all('span')
                    if len(nombre_usuario) > 0:
                        print(f"Nombre: {nombre_usuario[0].text.strip()}")

                    usuario = etiquetas_a[1].find_all('span')
                    if len(usuario) > 0:
                        print(f"Usuario: {usuario[-1].text.strip()}")

                    for etiqueta_a in etiquetas_a:
                        et_time = etiqueta_a.find_all('time')
                        if len(et_time) > 0:
                            tiempo = ""
                            for t in et_time:
                                tiempo += t.text
                            print(f"Fecha: {tiempo.strip()}")

            # Extraer contenido Tweet
            articulos_contenido = soup.find_all('div', attrs={'data-testid': 'tweetText'})
            for etiqueta in articulos_contenido:
                span = etiqueta.find_all('span')
                contenido_span = ""
                if span is not None:
                    for texto in span:
                        contenido_span += texto.text
                    print(f"Contenido: {contenido_span.strip()}")
            # Foto
            contenido_foto = soup.find_all('div', attrs={'data-testid': 'tweetPhoto'})
            if len(contenido_foto) > 0:
                for foto in contenido_foto:
                    img = foto.find('img')
                    if img is not None:
                        src = img.get('src')
                        print(f"Imagen: {src}")

            # Comentarios
            contenido_comentario = soup.find_all('div', attrs={'data-testid': 'reply'})
            for comentario in contenido_comentario:
                span = comentario.find('span')
                print(f"Numero Comentarios: {span.text}")
                # span = comentario.find_all('span')
                # numero_comentarios = ""
                # if len(span) > 0:
                #     for s in span:
                #         numero_comentarios += s.text
                # print(f"Numero Comentarios: {numero_comentarios}")

            # Retweets 
            contenido_retweet = soup.find_all('div', attrs={'data-testid': 'retweet'})
            for retweet in contenido_retweet:
                span = retweet.find('span')
                print(f"Numero Retweets: {span.text}")

                # span = retweet.find_all('span')
                # numero_retweet = ""
                # if len(span) > 0:
                #     for s in span:
                #         numero_retweet += s.text
                # print(f"Numero Retweets: {numero_retweet}")

            # Likes 
            contenido_like = soup.find_all('div', attrs={'data-testid': 'like'})
            for like in contenido_like:
                span = like.find('span')
                print(f"Numero Likes: {span.text}")
                # span = like.find_all('span')
                # numero_likes = ""
                # if len(span) > 0:
                #     for s in span:
                #         numero_likes += s.text
                # print(f"Numero Retweets: {numero_likes}")

            print("---------------------")

        # print(elemento)

def set_properties(browser_option):
    """adds capabilities to the driver"""
    header = Headers().generate()['User-Agent']
    browser_option.add_argument('--no-sandbox')
    browser_option.add_argument("--disable-dev-shm-usage")
    browser_option.add_argument('--ignore-certificate-errors')
    browser_option.add_argument('--disable-gpu')
    browser_option.add_argument('--log-level=3')
    browser_option.add_argument('--disable-notifications')
    browser_option.add_argument('--disable-popup-blocking')
    browser_option.add_argument('--user-agent={}'.format(header))
    return browser_option


def scroll_down(driver) -> None:
    """Helps to scroll down web page"""
    try:
        driver.execute_script("window.scrollTo(0, 500);")
        # body = driver.find_element(By.CSS_SELECTOR, 'body')
        # # for _ in range(randint(1, 3)):
        # for _ in range(2):
        #     body.send_keys(Keys.PAGE_DOWN)
        #     time.sleep(3)
    except Exception as ex:
        print("Error at scroll_down method {}".format(ex))

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

def find_status(tweet):
    """finds status and link from the tweet"""
    try:
        anchor = tweet.find_element(
            By.CSS_SELECTOR, "a[aria-label][dir]")
        return (anchor.get_attribute("href").split("/"), anchor.get_attribute("href"))
    except Exception as ex:
        print("Error at method find_status : {}".format(ex))
        return [0],""


main()
    # def __fetch_and_store_data(self):
    #     try:
    #         all_ready_fetched_posts = []
    #         # present_tweets = Finder.find_all_tweets(self.__driver)
    #         present_tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
    #
    #         self.__check_tweets_presence(present_tweets)
    #         all_ready_fetched_posts.extend(present_tweets)
    #
    #         while len(self.posts_data) < self.tweets_count:
    #             for tweet in present_tweets:
    #                 status, tweet_url = Finder.find_status(tweet)
    #                 replies = Finder.find_replies(tweet)
    #                 retweets = Finder.find_shares(tweet)
    #                 status = status[-1]
    #                 username = tweet_url.split("/")[3]
    #                 is_retweet = True if self.twitter_username.lower() != username.lower() else False
    #                 name = Finder.find_name_from_tweet(
    #                     tweet, is_retweet)
    #                 retweet_link = tweet_url if is_retweet is True else ""
    #                 posted_time = Finder.find_timestamp(tweet)
    #                 content = Finder.find_content(tweet)
    #                 likes = Finder.find_like(tweet)
    #                 images = Finder.find_images(tweet)
    #                 videos = Finder.find_videos(tweet)
    #                 hashtags = re.findall(r"#(\w+)", content)
    #                 mentions = re.findall(r"@(\w+)", content)
    #                 profile_picture = Finder.find_profile_image_link(tweet)
    #                 link = Finder.find_external_link(tweet)
    #                 self.posts_data[status] = {
    #                     "tweet_id": status,
    #                     "username": username,
    #                     "name": name,
    #                     "profile_picture": profile_picture,
    #                     "replies": replies,
    #                     "retweets": retweets,
    #                     "likes": likes,
    #                     "is_retweet": is_retweet,
    #                     "retweet_link": retweet_link,
    #                     "posted_time": posted_time,
    #                     "content": content,
    #                     "hashtags": hashtags,
    #                     "mentions": mentions,
    #                     "images": images,
    #                     "videos": videos,
    #                     "tweet_url": tweet_url,
    #                     "link": link
    #                 }
    #
    #             Utilities.scroll_down(self.__driver)
    #             Utilities.wait_until_completion(self.__driver)
    #             Utilities.wait_until_tweets_appear(self.__driver)
    #             present_tweets = Finder.find_all_tweets(
    #                 self.__driver)
    #             present_tweets = [
    #                 post for post in present_tweets if post not in all_ready_fetched_posts]
    #             self.__check_tweets_presence(present_tweets)
    #             all_ready_fetched_posts.extend(present_tweets)
    #             if self.__check_retry() is True:
    #                 break
    #
    #     except Exception as ex:
    #         logger.exception(
    #             "Error at method fetch_and_store_data : {}".format(ex))

    # texto = publicacion.
    # for text in texto:
    #     print(text.text)
    #     print("-----------")

    # Obtener todas las publicaciones
    # tweets = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    # tweet = driver.find_element("xpath","//article[@data-testid='tweet']")
    # tweet.click()
    # time.sleep(2)

    # Imprimir los textos de las publicaciones
    # for tweet in tweets:
    #     print(tweet.text)
    #     print("-" * 50)

    # Cerrar el driver de Selenium
    # driver.quit()

# Ejemplo de uso
# username = "NombreDeUsuario"
# scrape_twitter_profile()
