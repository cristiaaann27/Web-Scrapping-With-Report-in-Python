import requests
from bs4 import BeautifulSoup

def imprimir_temarios(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Asegúrate de que la solicitud fue exitosa

        soup = BeautifulSoup(response.text, 'html.parser')
        contenido_div = soup.find('div', class_='sixteen column contenido')

        if contenido_div:
            p_elements = contenido_div.find_all('p')
            for p in p_elements:
                print(p.get_text(strip=True))
                print("\n")
        else:
            print("No se encontró el div con la clase 'sixteen column contenido'.")
    except requests.RequestException as e:
        print(f"Error en la petición: {e}")
    except Exception as e:
        print(f"Error al procesar el contenido: {e}")

# URL de la página web
url = 'https://ujiapps.uji.es/upo/rest/publicacion/idioma/es?urlRedirect=http://ujiapps.uji.es/sia/rest/publicacion/2024/estudio/225&null'

try:
    response = requests.get(url)
    response.raise_for_status()  # Asegúrate de que la solicitud fue exitosa

    soup = BeautifulSoup(response.text, 'html.parser')
    asignaturas = soup.find_all('div', class_='asignatura')

    temarios = []

    for asignatura in asignaturas:
        titulo_element = asignatura.find('p', class_='titulo').find('a')
        titulo = titulo_element.get_text(strip=True) if titulo_element else "Sin título"

        secciones_list = asignatura.find('div', class_='secciones').find('ul')
        temario_link = None
        if secciones_list:
            for li in secciones_list.find_all('li'):
                link = li.find('a')
                if link and 'Temario' in link.get_text(strip=True):
                    temario_link = link['href']
                    break

        temarios.append({
            'titulo': titulo,
            'temario_link': temario_link
        })

    for temario in temarios:
        print(f"Asignatura: {temario['titulo']}")
        if temario['temario_link']:
            imprimir_temarios(f'https://ujiapps.uji.es/upo/rest/publicacion/idioma/es?urlRedirect=http://ujiapps.uji.es{temario["temario_link"]}')
        else:
            print("No se encontró enlace al temario.")
        print('-' * 40)
        print("\n")
        print("\n")

except requests.RequestException as e:
    print(f"Error en la petición principal: {e}")
except Exception as e:
    print(f"Error al procesar la página principal: {e}")
