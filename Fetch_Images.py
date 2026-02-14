import os
import time
import requests
from playwright.sync_api import sync_playwright

def download_pibbles():
    query_url = "https://mx.pinterest.com/search/pins/?q=Pibbles&rs=typed"
    save_folder = "mis_pibbles"
    
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(query_url)

        image_urls = set()
        print("Buscando pibbles hermosos...")

        while len(image_urls) < 100:
            # Scroll para cargar más contenido
            page.mouse.wheel(0, 2000) 
            time.sleep(2)
            
            # Buscamos los elementos img con el atributo específico que me mostraste
            images = page.query_selector_all('img[elementtiming="grid-non-story-pin-image-search"]')
            
            for img in images:
                # Intentamos sacar el srcset para obtener la de alta calidad
                srcset = img.get_attribute("srcset")
                if srcset:
                    # El srcset separa las URLs por comas; la última suele ser la mejor
                    links = [link.strip().split(' ')[0] for link in srcset.split(',')]
                    # Buscamos la que contenga 736x u originals
                    best_link = next((l for l in links if "736x" in l or "originals" in l), links[-1])
                    image_urls.add(best_link)
            
            print(f"Llevamos {len(image_urls)} enlaces encontrados...")
            if len(image_urls) > 120: break

        # Descarga efectiva
        for i, url in enumerate(list(image_urls)[:100]):
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    with open(f"{save_folder}/pibble_{i+1}.jpg", 'wb') as f:
                        f.write(response.content)
                    print(f"Guardado: pibble_{i+1}.jpg")
            except Exception as e:
                print(f"Error en {url}: {e}")

        browser.close()
        print(f"\n¡Listo! Revisa la carpeta '{save_folder}'")

if __name__ == "__main__":
    download_pibbles()