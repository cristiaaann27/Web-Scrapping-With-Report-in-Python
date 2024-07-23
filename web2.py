
from reportlab.lib.units import inch
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors

def extraer_temarios(url):
    temarios = []
    try:
        response = requests.get(url)
        response.raise_for_status()  # Asegúrate de que la solicitud fue exitosa

        soup = BeautifulSoup(response.text, 'html.parser')
        asignaturas = soup.find_all('div', class_='asignatura')

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
    except requests.RequestException as e:
        print(f"Error en la petición: {e}")
    except Exception as e:
        print(f"Error al procesar el contenido: {e}")
    return temarios

def extraer_contenido_temario(temario_url):
    contenido = ""
    try:
        response = requests.get(temario_url)
        response.raise_for_status()  # Asegúrate de que la solicitud fue exitosa

        soup = BeautifulSoup(response.text, 'html.parser')
        contenido_div = soup.find('div', class_='sixteen column contenido')

        if contenido_div:
            p_elements = contenido_div.find_all('p')
            for p in p_elements:
                contenido += p.get_text(strip=True) + "\n\n"
        else:
            contenido = "No se encontró el div con la clase 'sixteen column contenido'."
    except requests.RequestException as e:
        contenido = f"Error en la petición: {e}"
    except Exception as e:
        contenido = f"Error al procesar el contenido: {e}"
    return contenido

def generar_reporte_pdf(temarios, archivo_pdf):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(archivo_pdf, pagesize=letter, rightMargin=inch, leftMargin=inch, topMargin=inch, bottomMargin=inch)
    
    content = []

    for temario in temarios:
        titulo = f"Asignatura: {temario['titulo']}"
        content.append(Paragraph(titulo, styles['Title']))
        
        if temario['temario_link']:
            contenido = extraer_contenido_temario(f'https://ujiapps.uji.es/upo/rest/publicacion/idioma/es?urlRedirect=http://ujiapps.uji.es{temario["temario_link"]}')
            if contenido:
                content.append(Paragraph(contenido, styles['Normal']))
        else:
            content.append(Paragraph("No se encontró enlace al temario.", styles['BodyText']))
        
        content.append(Spacer(1, 12))  # Espaciado entre temarios
        content.append(Paragraph('-' * 80, styles['BodyText']))  # Línea separadora
        content.append(Spacer(1, 12))  # Espaciado adicional

    doc.build(content)

# URL de la página web
url = 'https://ujiapps.uji.es/upo/rest/publicacion/idioma/es?urlRedirect=http://ujiapps.uji.es/sia/rest/publicacion/2023/estudio/225&null'

temarios = extraer_temarios(url)
generar_reporte_pdf(temarios, "reporte_temarios1.pdf")
