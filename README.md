# 🚲 Falabella Colombia - Web Scraper & CI/CD Pipeline (Categoría Bicicletas)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.10%2B-green?style=for-the-badge&logo=selenium&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-7.4%2B-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

Este repositorio contiene una solución integral de **Ingeniería de Datos y DevOps** para la extracción, validación, pruebas automatizadas y despliegue continuo de información comercial de la categoría de **Bicicletas** en la plataforma e-commerce de **Falabella Colombia** (`www.falabella.com.co`).

El proyecto está diseñado bajo arquitectura **Headless**, supera cortafuegos de aplicaciones web (WAF) mediante un esquema de *dual-parsing*, integra suite de pruebas unitarias continuas con **Pytest** y despliega automáticamente el conjunto de datos limpio (`productos_falabella_bicicletas.csv`) a través de un flujo **CI/CD con GitHub Actions**.

---

## 📌 Características del Proyecto

* **Automatización Headless Anti-Bot:** Configuración de Chromium y Selenium WebDriver en modo silencioso (`--headless=new`), emulando User-Agent y viewport de escritorio para evitar respuestas de bloqueo `HTTP 403 Forbidden`.
* **Estrategia de Extracción Dual (Dual-Parsing):**
  * **Primaria:** Parseo directo del estado global JSON en React/Next.js (`script#__NEXT_DATA__`).
  * **Respaldo:** Análisis sintáctico de metadatos de datos estructurados Schema.org (`application/ld+json`).
* **Integración Continua (CI):** Ejecución automática de pruebas unitarias (`pytest`) en cada `push` o `pull_request` para verificar la conectividad de la plataforma objetivo y la integridad del objeto de datos.
* **Despliegue Continuo (CD):** Empaquetado y almacenamiento del dataset resultante como artefacto de flujo de trabajo (`actions/upload-artifact`) descargable en GitHub.
* **Programación Recurrente (Cron Job):** Disparador programado para ejecutar el pipeline de recolección de precios de forma autónoma diariamente a las 12:00 UTC.

---

## 📁 Estructura del Repositorio

```text
falabella-bicicletas-devops/
│
├── .github/
│   └── workflows/
│       └── scraper_ci_cd.yml        # Configuración del pipeline CI/CD en GitHub Actions
│
├── main.py                          # Script ejecutable principal del Web Scraper
├── test_scraper.py                  # Pruebas unitarias para Integración Continua (Pytest)
├── requirements.txt                 # Dependencias del entorno Python
├── .gitignore                       # Filtro de exclusión de binarios y cachés
├── README.md                        # Documentación técnica del repositorio
└── productos_falabella_bicicletas.csv # Dataset generado y desplegado por el pipeline

⚙️ Arquitectura del Pipeline CI/CD (scraper_ci_cd.yml)

graph TD
    A[Evento Push / PR / Cron Daily] --> B[Runner Ubuntu Latest]
    B --> C[Setup Python 3.10 & Install Google Chrome]
    C --> D[Install Dependencies requirements.txt]
    D --> E[Ejecutar Pytest test_scraper.py - CI]
    E -- Success --> F[Ejecutar Scraper main.py]
    E -- Failure --> G[Cancel Workflow & Alert]
    F --> H[Generar CSV productos_falabella_bicicletas.csv]
    H --> I[Publicar Artefacto en GitHub Actions - CD]

🚀 Instalación y Ejecución

Clonar el repositorio:

git clone [https://github.com/jaraiudigital/falabella-bicicletas-devops.git](https://github.com/jaraiudigital/falabella-bicicletas-devops.git)
cd falabella-bicicletas-devops

Crear e inicializar un entorno virtual:

python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

Instalar dependencias:

pip install -r requirements.txt

Ejecutar la suite de pruebas (CI):

pytest test_scraper.py -v

Ejecutar la extracción de datos:

python main.py

🧪 Pruebas Automatizadas (Pytest)
Las pruebas verifican los siguientes criterios antes de la generación del dataset:

test_falabella_bicycles_page_status: Confirma conectividad y respuesta del servidor objetivo.

test_next_data_structure_exists: Evalúa que el script de estado __NEXT_DATA__ se encuentre presente y contenga la clave props.

⚠️ Descargo de Responsabilidad (Disclaimer)
Este proyecto ha sido desarrollado exclusivamente con fines académicos, científicos y de demostración de arquitectura DevOps/Ingeniería de Datos. El script respeta las pausas de retardo (time.sleep) para evitar sobrecargar los servidores de la plataforma consultada.

