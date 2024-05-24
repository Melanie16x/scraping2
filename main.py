import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://www.mercadolibre.com.ar/c/autos-motos-y-otros#menu=categories'

# Función para crear la carpeta si no existe
def crear_directorio(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

# Función para descargar una imagen desde una URL
def descargar_imagen(image_url, directory_name):
    try:
        response = requests.get(image_url, stream=True)
        image_format = image_url.split('.')[-1].lower()
        if image_format in ['png', 'jpg', 'webp']:
            image_name = os.path.join(directory_name, image_url.split('/')[-1])
            with open(image_name, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Imagen descargada: {image_name}")
    except requests.exceptions.RequestException as e:
        print(f"No se pudo descargar la imagen {image_url}: {e}")

# Función para extraer las etiquetas <img> y sus src de una página web
def extraer_imagen(url, directory_name):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        for img in images:
            src = img.get('src')
            if src:
                image_url = urljoin(url, src)
                descargar_imagen(image_url, directory_name)
    except requests.exceptions.RequestException as e:
        print(f"No se pudo acceder a la página: {url}, error: {e}")

# Función para obtener los enlaces de la página principal
def obtener_links(soup):
    return [a['href'] for a in soup.find_all('a', href=True)]

# Función principal
def main(url):
    crear_directorio('imagenes')
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = obtener_links(soup)

        for link in links:
            print(f"Procesando {link}")
            extraer_imagen(link, 'imagenes')
    except requests.exceptions.RequestException as e:
        print(f"No se puede acceder a {url}: {e}")

if __name__ == '__main__':
    main(url)
