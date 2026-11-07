import pytest
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0')
    driver_instance = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver_instance
    driver_instance.quit()

def test_falabella_bicycles_page_status(driver):
    url = "https://www.falabella.com.co/falabella-co/category/cat50516/Bicicletas?page=1"
    driver.get(url)
    assert "falabella" in driver.current_url.lower(), "La URL cargada no coincide con el sitio objetivo."

def test_next_data_structure_exists(driver):
    url = "https://www.falabella.com.co/falabella-co/category/cat50516/Bicicletas?page=1"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    next_data_script = soup.find('script', id='__NEXT_DATA__')
    assert next_data_script is not None, "No se encontró el script __NEXT_DATA__ en la página."
    json_data = json.loads(next_data_script.string)
    assert 'props' in json_data, "El objeto JSON no posee la propiedad 'props'."
