from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
import json
from datetime import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import random

# Descargar recursos de NLTK para análisis de sentimientos
nltk.download('vader_lexicon')

app = Flask(__name__)
app.secret_key = 'diario_emocional_secret_key'

# Asegurar que existe el directorio para guardar los datos
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_user_data_path(username):
    """Obtiene la ruta al archivo de datos del usuario"""
    return os.path.join(DATA_DIR, f"{username}.json")

def load_user_data(username):
    """Carga los datos del usuario desde el archivo JSON"""
    file_path = get_user_data_path(username)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"entries": []}

def save_user_data(username, data):
    """Guarda los datos del usuario en un archivo JSON"""
    file_path = get_user_data_path(username)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def analyze_sentiment(text):
    """Analiza el sentimiento del texto y devuelve una categoría emocional"""
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    
    # Determinar la emoción basada en el puntaje de sentimiento
    if sentiment_score['compound'] >= 0.5:
        return "feliz"
    elif sentiment_score['compound'] >= 0.05:
        return "positivo"
    elif sentiment_score['compound'] <= -0.5:
        return "triste"
    elif sentiment_score['compound'] <= -0.05:
        return "negativo"
    else:
        return "neutral"

def get_feedback(emotion):
    """Genera retroalimentación empática basada en la emoción detectada"""
    feedbacks = {
        "feliz": [
            "¡Me alegra mucho que te sientas así! Disfruta este momento.",
            "¡Qué bueno verte tan feliz! Recuerda este sentimiento.",
            "La felicidad es un regalo, ¡disfrútala al máximo!"
        ],
        "positivo": [
            "Estás en un buen camino. Sigue así.",
            "Es genial que mantengas una actitud positiva.",
            "Pequeños momentos positivos construyen días mejores."
        ],
        "neutral": [
            "A veces estar neutral es necesario para procesar lo que sentimos.",
            "Los días neutros también son importantes en nuestro equilibrio.",
            "Tómate un momento para reflexionar sobre qué te gustaría sentir."
        ],
        "negativo": [
            "Está bien no sentirse bien siempre. ¿Hay algo que pueda ayudarte?",
            "Los sentimientos negativos son temporales. Respira profundo.",
            "Recuerda que mañana es un nuevo día con nuevas oportunidades."
        ],
        "triste": [
            "Siento que estés pasando por un momento difícil. Recuerda que no estás solo/a.",
            "La tristeza es una emoción válida. Date permiso para sentirla y procesarla.",
            "¿Has intentado hablar con alguien de confianza sobre cómo te sientes?"
        ]
    }
    return random.choice(feedbacks[emotion])

def get_recommendations(entries):
    """Genera recomendaciones basadas en patrones emocionales"""
    if len(entries) < 3:
        return None
    
    # Verificar si hay 3 días consecutivos con la misma emoción negativa
    recent_emotions = [entry["emotion"] for entry in entries[-3:]]
    
    if all(emotion == "triste" for emotion in recent_emotions):
        recommendations = [
            "Has estado triste varios días. Considera hablar con alguien de confianza sobre cómo te sientes.",
            "El ejercicio físico puede ayudar a mejorar tu estado de ánimo. ¿Qué tal salir a caminar?",
            "La música puede cambiar nuestro estado de ánimo. Prueba escuchar canciones que te hagan sentir bien."
        ]
        return random.choice(recommendations)
    
    if all(emotion == "negativo" for emotion in recent_emotions):
        recommendations = [
            "Has tenido varios días con emociones negativas. Intenta practicar la gratitud escribiendo 3 cosas positivas de tu día.",
            "Prueba técnicas de respiración profunda cuando te sientas abrumado/a.",
            "A veces un cambio en la rutina puede ayudar. ¿Qué tal probar algo nuevo hoy?"
        ]
        return random.choice(recommendations)
    
    return None

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username.strip():
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash('Por favor ingresa un nombre de usuario válido')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = load_user_data(username)
    
    # Obtener recomendación si hay suficientes entradas
    recommendation = None
    if user_data["entries"]:
        recommendation = get_recommendations(user_data["entries"])
    
    return render_template('dashboard.html', 
                          entries=user_data["entries"], 
                          username=username,
                          recommendation=recommendation)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = session['username']
        text = request.form['entry_text']
        emoji = request.form['emoji']
        
        # Analizar el sentimiento del texto
        emotion = analyze_sentiment(text)
        feedback = get_feedback(emotion)
        
        # Crear nueva entrada
        new_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text": text,
            "emoji": emoji,
            "emotion": emotion,
            "feedback": feedback
        }
        
        # Cargar y actualizar datos del usuario
        user_data = load_user_data(username)
        user_data["entries"].append(new_entry)
        save_user_data(username, user_data)
        
        flash('Tu entrada ha sido guardada exitosamente')
        return redirect(url_for('dashboard'))
    
    return render_template('new_entry.html')

@app.route('/view_entry/<int:entry_id>')
def view_entry(entry_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = load_user_data(username)
    
    if 0 <= entry_id < len(user_data["entries"]):
        entry = user_data["entries"][entry_id]
        return render_template('view_entry.html', entry=entry, entry_id=entry_id)
    
    flash('Entrada no encontrada')
    return redirect(url_for('dashboard'))

@app.route('/stats')
def stats():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = load_user_data(username)
    
    # Preparar datos para gráficos
    emotions = [entry["emotion"] for entry in user_data["entries"]]
    emotion_counts = {
        "feliz": emotions.count("feliz"),
        "positivo": emotions.count("positivo"),
        "neutral": emotions.count("neutral"),
        "negativo": emotions.count("negativo"),
        "triste": emotions.count("triste")
    }
    
    # Obtener fechas para el gráfico de línea temporal
    dates = [entry["date"].split()[0] for entry in user_data["entries"]]
    emotion_values = {"feliz": 2, "positivo": 1, "neutral": 0, "negativo": -1, "triste": -2}
    emotion_scores = [emotion_values[emotion] for emotion in emotions]
    
    return render_template('stats.html', 
                          emotion_counts=emotion_counts,
                          dates=dates,
                          emotion_scores=emotion_scores)

if __name__ == '__main__':
    # Crear directorio de datos si no existe
    if not os.path.exists('data'):
        os.makedirs('data')
    app.run(debug=True)
