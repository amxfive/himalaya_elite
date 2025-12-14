import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA "PREMIUM" ---
st.set_page_config(
    page_title="Himalaya Elite Analytics",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS (MEJORADO) ---
st.markdown("""
<style>
    /* Fondo general oscuro estilo "Midnight Mountain" */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Headers con gradiente */
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        margin-top: 2rem;
    }
    
    /* Separadores */
    hr {
        border-color: #2b313e;
        margin-top: 3rem;
        margin-bottom: 3rem;
    }

    /* Métricas destacadas */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        color: #00d2ff;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.3);
    }
    
    /* Info box custom */
    .stAlert {
        border-radius: 10px;
        border: 1px solid #3a7bd5;
        background-color: rgba(58, 123, 213, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def get_data():
    df = pd.read_excel("Himalayadataprep.xlsx")
    
    # --- LIMPIEZA ROBUSATA ---
    
    # 1. Year
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df.dropna(subset=['year'])
    df['year'] = df['year'].astype(int)

    # 2. Métricas numéricas
    cols_to_numeric = ['mdeaths', 'totmembers']
    for col in cols_to_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # 3. Success Flag
    def clean_success(val):
        if pd.isna(val): return 0
        s = str(val).strip().upper()
        if s in ['TRUE', '1', '1.0', 'YES', 'T']:
            return 1
        return 0

    df['success_flag'] = df['success1'].apply(clean_success)
    
    # 4. Picos y Texto
    df['pkname'] = df['pkname'].astype(str).fillna("Unknown")
    
    # 5. FILTRO HISTÓRICO (>= 1950)
    # Ignoramos datos muy antiguos para centrar el análisis
    df = df[df['year'] >= 1950]
    
    return df

df = get_data()

# --- SIDEBAR GLOBAL ---
with st.sidebar:
    st.sidebar.image(
    "Logo.png", 
    width=200 )    
    
    # Filtro de Años
    min_year, max_year = int(df['year'].min()), int(df['year'].max())
    rango_year = st.slider("📅 Periodo de Análisis", min_year, max_year, (1990, max_year))

    st.markdown("---")
    st.markdown("### Himalaya Elite SL")
    st.caption("Marcos Ortiz Durán\n Álvaro Lorenzo Hidalgo\n Alberto Águila.")

# Filtrar datos globales
df_filtered = df[df['year'].between(rango_year[0], rango_year[1])]

if df_filtered.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

# --- HERO SECTION ---
st.title("Himalaya Elite: Estrategia de Altura")
st.markdown(f"""
Bienvenido al centro de inteligencia de expediciones. 
Analizamos datos históricos desde **{rango_year[0]} hasta {rango_year[1]}** para guiar tus pasos hacia la cima.
""")
st.markdown("---")
# ==============================================================================
# SECCIÓN 1: SEGURIDAD (WHY?)
# ==============================================================================
st.header("1. ¿Por qué viajar al Himalaya hoy?")
st.markdown("**La seguridad es nuestra premisa.** Analizamos la evolución histórica del riesgo.")

# Preparar datos agregados
yearly_stats = df.groupby('year').agg(
    total_climbers=('totmembers', 'sum'),
    total_deaths=('mdeaths', 'sum')
).reset_index()

yearly_stats['death_rate_percent'] = (yearly_stats['total_deaths'] / yearly_stats['total_climbers']) * 100
yearly_stats['death_rate_percent'] = yearly_stats['death_rate_percent'].fillna(0)

# Diseño: 2 Columnas para separar visualmente Volumen vs Riesgo
dash_col1, dash_col2 = st.columns(2)

with dash_col1:
    st.subheader("📈 Popularidad (Volumen)")
    fig_vol = px.area(
        yearly_stats, x='year', y='total_climbers',
        title="Escaladores por Año",
        color_discrete_sequence=['#3a7bd5'] # Azul
    )
    fig_vol.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title=None, yaxis_title="Total Alpinistas",
        height=300
    )
    st.plotly_chart(fig_vol, use_container_width=True)

with dash_col2:
    st.subheader("📉 Riesgo (Mortalidad)")
    fig_risk = px.line(
        yearly_stats, x='year', y='death_rate_percent',
        title="Tasa de Mortalidad (%)",
        color_discrete_sequence=['#ff4b1f'], # Rojo
        markers=True
    )
    fig_risk.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title=None, yaxis_title="Mortalidad (%)",
        height=300
    )
    st.plotly_chart(fig_risk, use_container_width=True)

# Métricas resumen abajo
metric_col1, metric_col2, metric_col3 = st.columns(3)
current_dr = yearly_stats['death_rate_percent'].iloc[-1]
avg_dr_recent = yearly_stats['death_rate_percent'].tail(5).mean()
total_cl = yearly_stats['total_climbers'].sum()

metric_col1.metric("Total Alpinistas (Periodo)", f"{int(total_cl):,}")
metric_col2.metric("Tasa Mortalidad Actual", f"{current_dr:.2f}%", f"Promedio reciente: {avg_dr_recent:.1f}%", delta_color="inverse")
metric_col3.success("✅ **Conclusión:** Aunque hay más gente que nunca, la mortalidad se mantiene baja y controlada.")

st.markdown("---")

# ==============================================================================
# SECCIÓN 2: NACIONALIDADES (WHO?) - FOCO ESPAÑA
# ==============================================================================
st.header("2. Alcance Global: ¿Quién escala el Himalaya?")
st.markdown("España y el mundo en el techo del planeta.")

# Preparar datos mapa
all_nations = []
nations_series = df_filtered['nation'].dropna().astype(str)
for item in nations_series: all_nations.extend([p.strip() for p in item.split(',')])

countries_series = df_filtered['countries'].dropna().astype(str)
for item in countries_series: all_nations.extend([p.strip() for p in item.split(',')])

nation_counts = pd.Series(all_nations).value_counts().reset_index()
nation_counts.columns = ['Country', 'Climbers']

# Mapping básico y limpieza
country_map = {'W Germany': 'Germany', 'UK': 'United Kingdom', 'USA': 'United States', 'USSR': 'Russia'}
nation_counts['Country'] = nation_counts['Country'].replace(country_map)
nation_counts = nation_counts.groupby('Country').sum().reset_index()

c1, c2 = st.columns([2, 1])

with c1:
    fig_map = px.choropleth(
        nation_counts,
        locations="Country", locationmode='country names', color="Climbers",
        color_continuous_scale='Plasma', title="Distribución Mundial de Expedicionarios",
        projection="natural earth"
    )
    fig_map.update_layout(
        template="plotly_dark",
        geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#0e1117', landcolor='#1a1c24'),
        margin=dict(l=0,r=0,t=30,b=0)
    )
    st.plotly_chart(fig_map, use_container_width=True)

with c2:
    # --- ANÁLISIS ESPAÑA (CORREGIDO) ---
    st.subheader("🇪🇸 Foco en España")
    
    # Calcular con exactitud conteo de 'Spain' en nation y countries
    # La lógica de nation_counts ya lo hizo arriba (desglosando por comas)
    spain_row = nation_counts[nation_counts['Country'] == 'Spain']
    
    if not spain_row.empty:
        total_spain = int(spain_row['Climbers'].iloc[0])
        st.metric("Total Escaladores Españoles", f"{total_spain:,}", help="Conteo exacto de ciudadanos españoles en el periodo.")
        
        # Ranking global
        rank = nation_counts.sort_values('Climbers', ascending=False).reset_index(drop=True)
        spain_rank = rank[rank['Country'] == 'Spain'].index[0] + 1
        st.metric("Ranking Mundial", f"#{spain_rank}", f"Top {int((spain_rank/len(rank))*100)}%")
    else:
        st.info("No hay registros de España en este periodo.")

st.markdown("---")

# ==============================================================================
# SECCIÓN 3: Picos (WHERE?)
# ==============================================================================
st.header("3. El Mapa de la Fama: ¿Qué Pico Escalar?")
st.markdown("Los 'Ochomiles' más codiciados por la comunidad internacional.")

peak_stats = df_filtered['pkname'].value_counts().reset_index()
peak_stats.columns = ['Montaña', 'Expediciones']
top_peaks = peak_stats.head(10)

fig_peaks = px.bar(
    top_peaks, x='Expediciones', y='Montaña', orientation='h',
    title="Top 10 Picos por Popularidad"
)
fig_peaks.update_layout(
    template="plotly_dark",
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    yaxis={'categoryorder':'total ascending'}, height=400
)
st.plotly_chart(fig_peaks, use_container_width=True)

st.markdown("---")

# ==============================================================================
# SECCIÓN 3.5: PROGRESO DE ASCENSO (PIRÁMIDE DE LA VERDAD)
# ==============================================================================
st.header("3.5. La Realidad de la Montaña: ¿Hasta dónde llegan?")
st.markdown("Visualiza la **pirámide de ascenso**. Muchos lo intentan, pocos tocan el cielo.")

# Selector específico para este gráfico
# 1. Creamos la lista de opciones (igual que la pasas al selectbox)
lista_picos = sorted(df_filtered['pkname'].astype(str).unique())

# 2. Buscamos el índice de "Everest" dentro de esa lista específica
# Usamos un try/except por seguridad: si "Everest" no está (por los filtros previos), usamos 0
try:
    indice_default = lista_picos.index("Everest")
except ValueError:
    indice_default = 0 # Si no existe, selecciona el primero de la lista

# 3. Creamos el selectbox usando ese índice
peak_funnel = st.selectbox(
    "Selecciona Pico para ver la Pirámide:", 
    lista_picos, 
    index=indice_default
)
df_funnel = df_filtered[df_filtered['pkname'] == peak_funnel].copy()

if not df_funnel.empty:
    # 1. Altura del Pico
    peak_height = df_funnel['heightm'].max()
    if pd.isna(peak_height) or peak_height == 0:
        st.error("No hay datos de altura para este pico.")
    else:
        # 2. Limpieza de 'highpoint'
        df_funnel['highpoint'] = pd.to_numeric(df_funnel['highpoint'], errors='coerce').fillna(0)
        
        # 3. Cálculo de Niveles (Acumulativo)
        # Base: Todos los miembros (totmembers)
        total_climbers = df_funnel['totmembers'].sum()
        
        # Para saber cuántos llegaron a X altura, necesito saber 'totmembers' de expediciones que llegaron a X altura?
        # NO. 'highpoint' es por expedición. Asumimos que si la expedición llegó a 7000m, 
        # sus miembros (totmembers) "potencialmente" llegaron ahí o es el punto máx del equipo.
        # Si queremos contar PERSONAS, 'totmembers' es la mejor proxy de la expedición.
        
        # Filtros acumulativos
        # Nivel 1: Campo Base (>0%) -> Total
        count_base = total_climbers
        
        # Nivel 2: > 30% Altura
        count_30 = df_funnel[df_funnel['highpoint'] >= (peak_height * 0.30)]['totmembers'].sum()
        
        # Nivel 3: > 50% Altura
        count_50 = df_funnel[df_funnel['highpoint'] >= (peak_height * 0.50)]['totmembers'].sum()
        
        # Nivel 4: > 80% Altura (Zona de la Muerte aprox en 8000s, o ataque a cima)
        count_80 = df_funnel[df_funnel['highpoint'] >= (peak_height * 0.80)]['totmembers'].sum()
        
        # Nivel 5: Cima (Success)
        # Usamos smtmembers si existe (muy preciso), o success_flag * miembros si no.
        if 'smtmembers' in df_funnel.columns:
            # sum() de smtmembers a veces tiene NaNs -> fillna
            count_summit = df_funnel['smtmembers'].fillna(0).sum()
        else:
            # Fallback
            count_summit = df_funnel[df_funnel['success_flag'] == 1]['totmembers'].sum()

        # Validación lógica (para que el gráfico no se rompa si datos sucios)
        # Cima no puede ser mayor que 80%, etc.
        count_summit = min(count_summit, count_80)
        count_80 = min(count_80, count_50)
        count_50 = min(count_50, count_30)

        # Preparar datos para Funnel
        # Queremos forma de "Montaña" (Pirámide), base ancha abajo.
        # Plotly Funnel Area o Funnel standard. Funnel standard dibuja de arriba a abajo.
        # Si ponemos el dato más pequeño primero?
        
        pyramid_data = pd.DataFrame({
            'Etapa': ["CIMA 🚩", f">80% Altura ({int(peak_height*0.8)}m)", f">50% Altura ({int(peak_height*0.5)}m)", "Campo Base (Inicio)"],
            'Alpinistas': [count_summit, count_80, count_50, count_base],
            'Color': ['#FFD700', '#C0C0C0', '#cd7f32', '#0e1117'] # Oro, Plata, Bronce, Azul, Oscuro
        })

        fig_pyramid = px.funnel(
            pyramid_data, 
            y='Etapa', 
            x='Alpinistas',
            title=f"Pirámide de Ascenso: {peak_funnel} ({int(peak_height)}m)",
            color_discrete_sequence=['#00d2ff']
        )
        
        fig_pyramid.update_traces(marker=dict(color=pyramid_data['Color']))
        fig_pyramid.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis={'categoryorder':'array', 'categoryarray': pyramid_data['Etapa'].tolist()} # Forzar orden Cima -> Base
        )
        
        c_chart, c_text = st.columns([3, 1])
        with c_chart:
            st.plotly_chart(fig_pyramid, use_container_width=True)
        with c_text:
            st.metric("Tasa Cima Real", f"{(count_summit/count_base)*100:.1f}%", "de los que llegan al CB")
            st.caption("Muchos llegan al campo base, pero la altitud extrema filtra a la mayoría.")

else:
    st.warning("Datos insuficientes para la pirámide.")

st.markdown("---")

# ==============================================================================
# SECCIÓN 4: TEMPORADA (WHEN?)
# ==============================================================================
st.header("4. Estrategia Ganadora: ¿Cuándo Ir?")
st.markdown("Analizamos la distribución estacional para elegir el momento perfecto.")

# --- FILTRO DE MONTAÑA COMPARTIDO (Sección 4 y 5) ---
st.info("🎯 **Selecciona una montaña** para analizar su temporada ideal y las mejores agencias.")

available_peaks = sorted(df_filtered['pkname'].astype(str).unique().tolist())
available_peaks.insert(0, "TODAS LAS MONTAÑAS")
target_peak_shared = st.selectbox("Selecciona Montaña de Interés:", available_peaks)

# Filtrar datos según selección
if target_peak_shared != "TODAS LAS MONTAÑAS":
    df_peak_context = df_filtered[df_filtered['pkname'] == target_peak_shared]
    title_suffix = f"en {target_peak_shared}"
else:
    df_peak_context = df_filtered
    title_suffix = "Global"

col_season_1, col_season_2 = st.columns([2, 1])

with col_season_1:
    # Agrupación simple: Total por temporada (sin años)
    season_dist = df_peak_context.groupby('season')['totmembers'].sum().reset_index()
    total_climbers_peak = season_dist['totmembers'].sum()
    season_dist['percentage'] = (season_dist['totmembers'] / total_climbers_peak) * 100
    # Definimos el diccionario de traducción
    traduccion_estaciones = {
        'Spring': 'Primavera',
        'Autumn': 'Otoño',
        'Winter': 'Invierno',
        'Summer': 'Verano',
        'Unknown': 'Desconocido' # Por si acaso hay datos sucios
    }
    
    # Aplicamos la traducción
    season_dist['season'] = season_dist['season'].astype(str).replace(traduccion_estaciones)

    # Gráfico de Barras Simple o Pastel. 
    # Barras es mejor para comparar magnitudes claras.
    fig_season = px.bar(
        season_dist, x="season", y="percentage",
        title=f"Distribución Estacional {title_suffix} (%)",
        text_auto='.1f'
    )
    fig_season.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Temporada",
        yaxis_title="% de Alpinistas",
        showlegend=False
    )
    st.plotly_chart(fig_season, use_container_width=True)

with col_season_2:
    st.markdown("### 💡 Nota")
    if not season_dist.empty:
        top_season = season_dist.sort_values('totmembers', ascending=False).iloc[0]
        st.write(f"Para **{target_peak_shared if target_peak_shared != 'TODAS LAS MONTAÑAS' else 'el Himalaya en general'}**, la temporada predominante es **{top_season['season']}**.")
        st.write(f"Concentra el **{top_season['percentage']:.1f}%** de todos los escaladores.")
    else:
        st.warning("Sin datos.")

st.markdown("---")

# ==============================================================================
# SECCIÓN 5: AGENCIAS (WITH WHOM?) - THE SELL
# ==============================================================================
# Ranking Agencias
min_exp = 3 
agency_stats = df_peak_context.groupby('agency').agg(
    Expediciones=('expid', 'count'),
    Exitos=('success_flag', 'sum')
).reset_index()

# 1. Tasa de Éxito Pura
agency_stats['Tasa Exito'] = (agency_stats['Exitos'] / agency_stats['Expediciones']) * 100

# 2. Elite Score
agency_stats['Elite Score'] = agency_stats['Tasa Exito'] * np.log10(agency_stats['Expediciones'] + 1)

# Filtramos y ordenamos, tomamos el Top 3 para el podio
top_agencies = agency_stats[agency_stats['Expediciones'] >= min_exp].sort_values('Elite Score', ascending=False)
podium = top_agencies.head(3).reset_index(drop=True)

if podium.empty:
    st.warning(f"No hay suficientes datos (min. {min_exp} exp.) para generar un ranking fiable.")
else:
    st.markdown("### 🏆 Podio: Mejores Agencias (Elite Score)")
    
    # Creamos columnas dinámicas según cuántas agencias tengamos (por si hay menos de 3)
    cols = st.columns(len(podium))
    medals = ["🥇 Oro", "🥈 Plata", "🥉 Bronce"]
    
    for index, row in podium.iterrows():
        with cols[index]:
            # Usamos st.metric para mostrar el dato de forma elegante y textual
            st.metric(
                label=f"{medals[index]}",
                value=row['agency'],
                delta=f"{row['Tasa Exito']:.1f}% Éxito ({row['Expediciones']} Exp.)",
                delta_color="off" # 'off' pone el delta en gris/neutro
            )
            st.caption(f"Score: {row['Elite Score']:.2f}")

    st.markdown("---")
    
    # Mantenemos la tabla completa (Top 10) en el expander por si quieren ver más detalles
    with st.expander("🔍 Ver Ranking Completo (Top 10)"):
        top_10 = top_agencies.head(10)
        st.dataframe(
            top_10[['agency', 'Expediciones', 'Tasa Exito', 'Elite Score']].style.format({
                'Tasa Exito': "{:.1f}%", 
                'Elite Score': "{:.2f}"
            }),
            use_container_width=True
        )

st.markdown("---")
st.markdown("**Himalaya Elite Analytics** - *Llevándote a lo más alto.*")
