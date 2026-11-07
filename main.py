import json
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def ejecutar_scraping(paginas=5, nombre_salida="productos_falabella_bicicletas.csv"):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    todos_los_productos = []

    try:
        for pagina in range(1, paginas + 1):
            url = f"https://www.falabella.com.co/falabella-co/category/cat50516/Bicicletas?page={pagina}"
            print(f"Procesando página {pagina} de {paginas}... ", end="")
            driver.get(url)
            time.sleep(4)

            soup_pag = BeautifulSoup(driver.page_source, 'html.parser')
            conteo = 0

            next_data_script = soup_pag.find('script', id='__NEXT_DATA__')
            if next_data_script and next_data_script.string:
                try:
                    json_data = json.loads(next_data_script.string)
                    results = json_data.get('props', {}).get('pageProps', {}).get('results', [])

                    for item in results:
                        sku = item.get('productId') or item.get('skuId') or item.get('id', 'N/A')
                        nombre = item.get('displayName') or item.get('title', 'No disponible')
                        marca = item.get('brand') or item.get('brandName') or 'Falabella'
                        
                        precio_fmt = 'No disponible'
                        prices = item.get('prices', [])
                        if isinstance(prices, list) and len(prices) > 0:
                            p_list = prices[0].get('price', [])
                            if p_list:
                                raw_p = str(p_list[0]).replace('.', '').replace(',', '')
                                try:
                                    precio_fmt = f"${float(raw_p):,.0f}"
                                except ValueError:
                                    precio_fmt = f"${p_list[0]}"

                        todos_los_productos.append({
                            "Referencia (SKU)": sku,
                            "Nombre/Marca": f"[{marca}] {nombre}",
                            "Valor": precio_fmt,
                            "Características": f"Bicicletas - Falabella (Pág {pagina})"
                        })
                        conteo += 1
                except Exception:
                    pass

            print(f"¡Completada! ({conteo} productos)")

    finally:
        driver.quit()

    df = pd.DataFrame(todos_los_productos)
    if not df.empty:
        df = df.drop_duplicates(subset=['Nombre/Marca'])
        df.to_csv(nombre_salida, index=False, encoding='utf-8-sig', sep=';')
        print(f"\nExtracción finalizada: {nombre_salida} ({len(df)} registros)")
        return nombre_salida
    else:
        print("No se encontraron registros.")
        return None

if __name__ == "__main__":
    ejecutar_scraping()
