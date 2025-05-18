# Diario Emocional Interactivo

Una aplicación web diseñada para ayudar a los adolescentes a registrar y comprender sus emociones diarias.

## Características principales

- **Registro de emociones**: Los usuarios pueden registrar sus emociones diariamente mediante texto y emojis.
- **Análisis de sentimientos**: La aplicación analiza el texto ingresado para detectar el estado emocional.
- **Retroalimentación empática**: Proporciona respuestas personalizadas basadas en las emociones detectadas.
- **Seguimiento emocional**: Visualización de patrones emocionales a lo largo del tiempo mediante gráficos.
- **Recomendaciones automáticas**: Sugerencias basadas en patrones emocionales detectados.

## Tecnologías utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Análisis de sentimientos**: NLTK (Natural Language Toolkit)
- **Visualización de datos**: Chart.js

## Instalación

1. Clona este repositorio:
```
git clone <url-del-repositorio>
```

2. Crea un entorno virtual e instala las dependencias:
```
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```
python app.py
```

4. Abre tu navegador y visita `http://localhost:5000`

## Estructura del proyecto

```
DiarioEmocional/
├── app.py                  # Aplicación principal Flask
├── requirements.txt        # Dependencias del proyecto
├── data/                   # Directorio para almacenar datos de usuarios
├── static/                 # Archivos estáticos
│   ├── css/                # Hojas de estilo
│   ├── js/                 # Scripts JavaScript
│   └── images/             # Imágenes
└── templates/              # Plantillas HTML
    ├── base.html           # Plantilla base
    ├── login.html          # Página de inicio de sesión
    ├── dashboard.html      # Panel principal
    ├── new_entry.html      # Formulario para nueva entrada
    ├── view_entry.html     # Vista detallada de una entrada
    └── stats.html          # Estadísticas y gráficos
```

## Uso

1. Inicia sesión con tu nombre de usuario
2. En el panel principal, haz clic en "Nueva Entrada"
3. Selecciona un emoji que represente tu estado de ánimo
4. Escribe sobre tu día y tus emociones
5. Guarda la entrada y recibe retroalimentación
6. Visualiza tus estadísticas emocionales en la sección "Estadísticas"

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios importantes antes de realizar un pull request.
