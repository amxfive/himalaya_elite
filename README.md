
# 🏔️ Himalaya Elite Analytics

Tablero interactivo desarrollado con **Streamlit** para el análisis estratégico de expediciones al Himalaya, orientado a la toma de decisiones de una agencia especializada en asesoramiento de alpinismo de alta montaña.

El proyecto utiliza datos históricos reales para recomendar **qué montaña escalar, en qué época y con qué agencia**, priorizando seguridad, éxito y experiencia.

---

## 🎯 Objetivo del proyecto

Simular el trabajo de una **agencia de asesoramiento en expediciones de alta montaña**, analizando una base de datos histórica del Himalaya para:

- Evaluar la **seguridad y evolución del riesgo** a lo largo del tiempo.
- Identificar **qué montañas** concentran mayor actividad y éxito.
- Analizar **cuándo es mejor escalar** según la temporada.
- Recomendar **las mejores agencias** en función de su experiencia y tasa de éxito.
- Ofrecer una herramienta visual e interactiva para apoyar la decisión del cliente.

---

## 📊 Storytelling y estructura del dashboard

El dashboard sigue una narrativa clara basada en preguntas clave:

### 1️⃣ ¿Por qué viajar al Himalaya hoy?
- Evolución histórica del número de alpinistas.
- Tasa de mortalidad a lo largo del tiempo.
- Comparación entre popularidad y riesgo.

### 2️⃣ ¿Quién escala el Himalaya?
- Distribución global de expedicionarios por país.
- Análisis específico del papel de España en el contexto internacional.

### 3️⃣ ¿Qué montaña escalar?
- Ranking de los picos más populares.
- Visualización de los ochomiles más demandados.

### 3.5️⃣ ¿Hasta dónde llegan realmente?
- Pirámide de ascenso por montaña.
- Comparación entre participantes, progresión en altura y cumbres alcanzadas.

### 4️⃣ ¿Cuándo es el mejor momento para ir?
- Distribución estacional de las expediciones.
- Análisis específico por montaña seleccionada.

### 5️⃣ ¿Con qué agencia ir?
- Ranking de agencias según:
  - Número de expediciones.
  - Tasa de éxito.
  - **Elite Score**, métrica propia que combina éxito y experiencia.

---

## 🛠️ Tecnologías utilizadas

- **Python**
- **Streamlit** – Framework para dashboards interactivos
- **Pandas** – Limpieza y transformación de datos
- **Plotly (Express y Graph Objects)** – Visualización avanzada
- **NumPy** – Cálculos auxiliares
- **CSS personalizado** – Estética premium y coherente con la temática

---

## 📂 Estructura del proyecto

```text
himalaya_elite/
├── app.py                  # Aplicación principal Streamlit
├── Himalayadataprep.xlsx   # Base de datos preprocesada
├── Logo.png                # Logo de la agencia
├── README.md               # Documentación del proyecto
└── requirements.txt / pyproject.toml
````

---

## ▶️ Cómo ejecutar la aplicación

### 1. Clonar el repositorio

```bash
git clone https://gitlab.com/amxfive/himalaya_elite.git
cd himalaya_elite
```

### 2. Crear y activar entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

*(Si se utiliza `pyproject.toml`, las dependencias pueden instalarse con `uv sync`)*

### 4. Ejecutar Streamlit

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en el navegador.

---

## 👥 Autores

* Marcos Ortiz Durán
* Álvaro Lorenzo Hidalgo
* Alberto Águila

---

## 📌 Conclusión

Este proyecto demuestra cómo la visualización interactiva con Streamlit permite transformar datos históricos complejos en información clara y accionable para la toma de decisiones en un contexto empresarial simulado como el asesoramiento en expediciones de alta montaña.

```
```
