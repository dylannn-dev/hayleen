"""
Smart Balance - App para estudiantes trabajadores
Ayuda a organizar tiempo, tareas y bienestar personal.
Ejecutar con: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURACIÓN GENERAL DE LA APP
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Balance",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# ESTILOS CSS PERSONALIZADOS (lila, celeste, blanco)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Importar fuente suave */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    /* Fondo principal */
    .stApp {
        background: linear-gradient(135deg, #f0eaff 0%, #e8f4fd 50%, #fdf0ff 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #c9b8f0 0%, #a8d8ea 100%);
        border-right: none;
    }
    [data-testid="stSidebar"] * {
        color: #3a2d5c !important;
        font-weight: 600;
    }

    /* Títulos principales */
    h1 { color: #6a4c93 !important; font-weight: 800 !important; }
    h2 { color: #5b8db8 !important; font-weight: 700 !important; }
    h3 { color: #7a5fa0 !important; font-weight: 700 !important; }

    /* Tarjetas de contenido */
    .card {
        background: white;
        border-radius: 20px;
        padding: 24px;
        margin: 12px 0;
        box-shadow: 0 4px 20px rgba(106, 76, 147, 0.12);
        border-left: 5px solid #c9b8f0;
    }

    /* Tarjeta azul */
    .card-blue {
        background: white;
        border-radius: 20px;
        padding: 24px;
        margin: 12px 0;
        box-shadow: 0 4px 20px rgba(91, 141, 184, 0.12);
        border-left: 5px solid #a8d8ea;
    }

    /* Score circular */
    .score-container {
        text-align: center;
        background: linear-gradient(135deg, #c9b8f0, #a8d8ea);
        border-radius: 24px;
        padding: 32px;
        color: white;
        box-shadow: 0 8px 30px rgba(106, 76, 147, 0.25);
    }
    .score-number {
        font-size: 72px;
        font-weight: 800;
        line-height: 1;
        text-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .score-label {
        font-size: 18px;
        font-weight: 600;
        opacity: 0.9;
        margin-top: 8px;
    }

    /* Barra de progreso personalizada */
    .progress-bar-outer {
        background: #e8e0f5;
        border-radius: 50px;
        height: 20px;
        margin: 12px 0;
        overflow: hidden;
    }
    .progress-bar-inner {
        height: 100%;
        border-radius: 50px;
        background: linear-gradient(90deg, #c9b8f0, #a8d8ea);
        transition: width 0.5s ease;
    }

    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #c9b8f0, #a8d8ea) !important;
        color: #3a2d5c !important;
        border: none !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        padding: 10px 28px !important;
        font-family: 'Nunito', sans-serif !important;
        box-shadow: 0 4px 15px rgba(106, 76, 147, 0.2) !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(106, 76, 147, 0.3) !important;
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #e0d5f5 !important;
        font-family: 'Nunito', sans-serif !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: #c9b8f0 !important;
        box-shadow: 0 0 0 3px rgba(201, 184, 240, 0.2) !important;
    }

    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #6a4c93 !important;
        font-weight: 800 !important;
    }

    /* Mensajes de chat */
    .chat-user {
        background: linear-gradient(135deg, #c9b8f0, #b8a8e8);
        color: #2d1f4a;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        margin-left: 20%;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(106,76,147,0.15);
    }
    .chat-bot {
        background: linear-gradient(135deg, #e8f4fd, #d0ecfb);
        color: #1a3a5c;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        margin-right: 20%;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(91,141,184,0.15);
    }
    .chat-avatar {
        font-size: 20px;
        margin-right: 8px;
    }

    /* Tags de actividad */
    .tag-trabajo {
        background: #ffd6e0; color: #8b1a4a;
        padding: 3px 12px; border-radius: 50px; font-size: 12px; font-weight: 700;
    }
    .tag-estudio {
        background: #d0e8ff; color: #1a3a8b;
        padding: 3px 12px; border-radius: 50px; font-size: 12px; font-weight: 700;
    }
    .tag-descanso {
        background: #d8f5d0; color: #1a6b2a;
        padding: 3px 12px; border-radius: 50px; font-size: 12px; font-weight: 700;
    }
    .tag-tarea {
        background: #f5e8d0; color: #8b5a1a;
        padding: 3px 12px; border-radius: 50px; font-size: 12px; font-weight: 700;
    }

    /* Respiración */
    .breath-box {
        background: linear-gradient(135deg, #e8f4fd, #f0eaff);
        border-radius: 20px;
        padding: 28px;
        text-align: center;
        border: 2px solid #c9b8f0;
    }

    /* Ocultar footer de Streamlit */
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INICIALIZAR SESSION STATE (memoria temporal)
# ─────────────────────────────────────────────
if "agenda" not in st.session_state:
    # Datos de ejemplo iniciales
    st.session_state.agenda = pd.DataFrame([
        {"Día": "Lunes",     "Hora": "08:00",  "Tipo": "Trabajo",   "Descripción": "Turno mañana"},
        {"Día": "Lunes",     "Hora": "18:00",  "Tipo": "Estudio",   "Descripción": "Clases virtuales"},
        {"Día": "Martes",    "Hora": "09:00",  "Tipo": "Trabajo",   "Descripción": "Reunión equipo"},
        {"Día": "Miércoles", "Hora": "14:00",  "Tipo": "Estudio",   "Descripción": "Preparar prueba Cálculo"},
        {"Día": "Jueves",    "Hora": "20:00",  "Tipo": "Descanso",  "Descripción": "Tiempo libre / deporte"},
        {"Día": "Viernes",   "Hora": "08:00",  "Tipo": "Trabajo",   "Descripción": "Turno completo"},
        {"Día": "Sábado",    "Hora": "10:00",  "Tipo": "Tarea",     "Descripción": "Entrega informe Física"},
        {"Día": "Domingo",   "Hora": "12:00",  "Tipo": "Descanso",  "Descripción": "Descanso y familia"},
    ])

if "tareas" not in st.session_state:
    # Lista de tareas pendientes iniciales
    st.session_state.tareas = [
        {"texto": "📚 Estudiar para prueba de Cálculo", "completada": False},
        {"texto": "📝 Entregar informe de Física", "completada": False},
        {"texto": "💼 Enviar reporte al jefe", "completada": True},
        {"texto": "📖 Leer capítulo 5 de Biología", "completada": False},
        {"texto": "🗂️ Organizar apuntes de la semana", "completada": False},
    ]

if "chat_historial" not in st.session_state:
    # Historial del chatbot
    st.session_state.chat_historial = [
        {"rol": "bot", "mensaje": "¡Hola! 🌸 Soy tu asistente Smart Balance. Cuéntame cómo te sientes hoy o qué necesitas organizar."}
    ]

# ─────────────────────────────────────────────
# SIDEBAR - NAVEGACIÓN PRINCIPAL
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌸 Smart Balance")
    st.markdown("---")

    pagina = st.radio(
        "Navegar a:",
        ["🏠 Inicio", "📅 Agenda Semanal", "✅ Recordatorios", "🤖 Chatbot", "💆 Bienestar"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**Hoy es:**")
    st.markdown(f"📆 {datetime.now().strftime('%A %d %B %Y').title()}")
    st.markdown("---")
    st.markdown("💡 *Recuerda: cada pequeño paso cuenta.*")


# ══════════════════════════════════════════════
# PÁGINA 1: INICIO
# ══════════════════════════════════════════════
if pagina == "🏠 Inicio":

    # Encabezado principal
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("# 🌸 Smart Balance")
        st.markdown(
            "### Tu compañera para equilibrar el estudio, el trabajo y el bienestar"
        )
        st.markdown("""
        <div class='card'>
        <p style='font-size:16px; color:#555; margin:0;'>
        Smart Balance te ayuda a <strong>organizar tu tiempo</strong>, gestionar tus
        <strong>tareas pendientes</strong> y cuidar tu <strong>bienestar emocional</strong>,
        todo en un solo lugar. Diseñada especialmente para estudiantes que también trabajan. 💜
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Score visual (dato ficticio demostrativo)
        score = 74
        st.markdown(f"""
        <div class='score-container'>
            <div style='font-size:14px; font-weight:700; opacity:0.85; margin-bottom:8px;'>
                ✨ Smart Balance Score
            </div>
            <div class='score-number'>{score}%</div>
            <div class='score-label'>¡Vas muy bien! 🌟</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Tarjetas de resumen rápido
    st.markdown("### 📊 Resumen de hoy")
    c1, c2, c3, c4 = st.columns(4)

    tareas_pendientes = sum(1 for t in st.session_state.tareas if not t["completada"])
    tareas_completas  = sum(1 for t in st.session_state.tareas if t["completada"])

    with c1:
        st.metric("📋 Actividades esta semana", len(st.session_state.agenda))
    with c2:
        st.metric("✅ Tareas completadas", tareas_completas)
    with c3:
        st.metric("⏳ Tareas pendientes", tareas_pendientes)
    with c4:
        pct = int(tareas_completas / max(len(st.session_state.tareas), 1) * 100)
        st.metric("📈 Progreso tareas", f"{pct}%")

    # Barra de progreso de tareas
    st.markdown("#### Tu progreso de tareas:")
    st.markdown(f"""
    <div class='progress-bar-outer'>
        <div class='progress-bar-inner' style='width:{pct}%'></div>
    </div>
    <p style='color:#6a4c93; font-weight:700; text-align:right;'>{pct}% completado</p>
    """, unsafe_allow_html=True)

    st.markdown("---")
    # Sección de motivación
    st.markdown("""
    <div class='card-blue'>
    <h3 style='margin:0 0 8px 0;'>💡 Consejo del día</h3>
    <p style='color:#555; margin:0; font-size:15px;'>
    Recuerda hacer pausas de <strong>5 minutos</strong> cada hora de estudio.
    Tu cerebro necesita descanso para consolidar lo aprendido. ¡Tú puedes! 🧠✨
    </p>
    </div>
    """, unsafe_allow_html=True)

    # Desglose del score
    st.markdown("### 🔍 Desglose del Smart Balance Score")
    dimensiones = {
        "📚 Estudio organizado": 80,
        "💼 Trabajo gestionado": 70,
        "😴 Descanso adecuado": 60,
        "💆 Bienestar emocional": 85,
    }
    for dim, val in dimensiones.items():
        st.markdown(f"**{dim}** — {val}%")
        st.markdown(f"""
        <div class='progress-bar-outer'>
            <div class='progress-bar-inner' style='width:{val}%'></div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 2: AGENDA SEMANAL
# ══════════════════════════════════════════════
elif pagina == "📅 Agenda Semanal":

    st.markdown("# 📅 Agenda Semanal")
    st.markdown("Visualiza y organiza tus actividades de la semana.")

    # Tabla con la agenda actual
    st.markdown("### 📋 Actividades registradas")

    # Mostrar la tabla con colores por tipo
    df = st.session_state.agenda.copy()

    def color_tipo(val):
        colores = {
            "Trabajo":  "background-color: #ffd6e0; color: #8b1a4a;",
            "Estudio":  "background-color: #d0e8ff; color: #1a3a8b;",
            "Descanso": "background-color: #d8f5d0; color: #1a6b2a;",
            "Tarea":    "background-color: #f5e8d0; color: #8b5a1a;",
        }
        return colores.get(val, "")

    styled = df.style.applymap(color_tipo, subset=["Tipo"])
    st.dataframe(styled, use_container_width=True, hide_index=True)

    # Leyenda de colores
    st.markdown("""
    <div style='display:flex; gap:12px; margin:8px 0 20px 0; flex-wrap:wrap;'>
        <span class='tag-trabajo'>💼 Trabajo</span>
        <span class='tag-estudio'>📚 Estudio</span>
        <span class='tag-descanso'>😴 Descanso</span>
        <span class='tag-tarea'>📝 Tarea</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Formulario para agregar nueva actividad
    st.markdown("### ➕ Agregar nueva actividad")

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            nuevo_dia  = st.selectbox("📆 Día", dias)
            nueva_hora = st.text_input("🕐 Hora (ej: 14:30)", placeholder="14:30")

        with col2:
            tipos = ["Trabajo", "Estudio", "Descanso", "Tarea"]
            nuevo_tipo = st.selectbox("🏷️ Tipo de actividad", tipos)
            nueva_desc = st.text_input("📝 Descripción", placeholder="Describe la actividad...")

        if st.button("✨ Agregar actividad"):
            if nueva_hora and nueva_desc:
                nueva_fila = {
                    "Día": nuevo_dia,
                    "Hora": nueva_hora,
                    "Tipo": nuevo_tipo,
                    "Descripción": nueva_desc
                }
                # Agregar al dataframe en session_state
                st.session_state.agenda = pd.concat(
                    [st.session_state.agenda, pd.DataFrame([nueva_fila])],
                    ignore_index=True
                )
                st.success(f"✅ Actividad '{nueva_desc}' agregada para el {nuevo_dia}.")
                st.rerun()
            else:
                st.warning("⚠️ Por favor completa la hora y la descripción.")

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 3: RECORDATORIOS
# ══════════════════════════════════════════════
elif pagina == "✅ Recordatorios":

    st.markdown("# ✅ Recordatorios y Tareas")
    st.markdown("Organiza tus pendientes y marca lo que ya completaste.")

    # Estadísticas rápidas
    total     = len(st.session_state.tareas)
    completas = sum(1 for t in st.session_state.tareas if t["completada"])
    pendientes = total - completas

    c1, c2, c3 = st.columns(3)
    c1.metric("📋 Total tareas", total)
    c2.metric("✅ Completadas", completas)
    c3.metric("⏳ Pendientes", pendientes)

    st.markdown("---")

    # Lista de tareas con checkboxes
    st.markdown("### 📌 Lista de tareas")

    for i, tarea in enumerate(st.session_state.tareas):
        col_check, col_text = st.columns([0.08, 0.92])
        with col_check:
            completada = st.checkbox(
                "",
                value=tarea["completada"],
                key=f"tarea_{i}",
                label_visibility="collapsed"
            )
            # Actualizar estado en session_state
            st.session_state.tareas[i]["completada"] = completada

        with col_text:
            if completada:
                st.markdown(
                    f"<p style='color:#aaa; text-decoration:line-through; margin:8px 0;'>{tarea['texto']}</p>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<p style='color:#3a2d5c; font-weight:600; margin:8px 0;'>{tarea['texto']}</p>",
                    unsafe_allow_html=True
                )

    st.markdown("---")

    # Agregar nueva tarea
    st.markdown("### ➕ Agregar nueva tarea")
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    nueva_tarea = st.text_input(
        "📝 Escribe tu nueva tarea",
        placeholder="Ej: Estudiar capítulo 3 de Historia..."
    )

    if st.button("✨ Agregar tarea"):
        if nueva_tarea.strip():
            st.session_state.tareas.append({
                "texto": f"📌 {nueva_tarea.strip()}",
                "completada": False
            })
            st.success(f"✅ Tarea '{nueva_tarea}' agregada.")
            st.rerun()
        else:
            st.warning("⚠️ Escribe algo antes de agregar.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Botón para limpiar las completadas
    if st.button("🗑️ Eliminar tareas completadas"):
        st.session_state.tareas = [t for t in st.session_state.tareas if not t["completada"]]
        st.success("🧹 Tareas completadas eliminadas.")
        st.rerun()


# ══════════════════════════════════════════════
# PÁGINA 4: CHATBOT DEMO
# ══════════════════════════════════════════════
elif pagina == "🤖 Chatbot":

    st.markdown("# 🤖 Chatbot Smart Balance")
    st.markdown("Cuéntame cómo te sientes o qué necesitas organizar. ¡Estoy aquí para ayudarte! 💜")

    # Función de respuestas predefinidas del chatbot
    def obtener_respuesta(mensaje):
        """Devuelve respuestas simples según palabras clave."""
        msg = mensaje.lower()

        # Palabras clave de estrés
        if any(p in msg for p in ["estresada", "estresado", "estrés", "estres", "agobiada", "agobiado"]):
            return (
                "💜 Respira profundo. Parece que estás sintiendo mucho estrés. "
                "Te sugiero hacer una pausa de 5 minutos: cierra los ojos, inhala contando hasta 4, "
                "mantén 4 segundos y exhala en 6. Repite 3 veces. "
                "Recuerda: no puedes dar lo mejor de ti si no te cuidas. 🌿"
            )

        # Palabras clave de prueba / examen
        elif any(p in msg for p in ["prueba", "examen", "test", "evaluación", "evaluacion"]):
            return (
                "📚 ¡Tú puedes con esa prueba! Te recomiendo organizar tu estudio en bloques de "
                "25 minutos con 5 de descanso (técnica Pomodoro). "
                "Empieza por los temas más difíciles cuando estés más fresca/fresco. "
                "¿Quieres que te ayude a organizar un plan de estudio en la Agenda? 📅"
            )

        # Palabras clave de cansancio
        elif any(p in msg for p in ["cansada", "cansado", "agotada", "agotado", "sin energía", "sin energia"]):
            return (
                "😴 Tu cuerpo te está pidiendo descanso y eso es completamente válido. "
                "Si puedes, toma una siesta corta de 20 minutos. "
                "Hidrátate bien y trata de dormir al menos 7 horas esta noche. "
                "El descanso también es parte del rendimiento. 💙"
            )

        # Palabras clave de organización
        elif any(p in msg for p in ["organizar", "organización", "organizacion", "orden", "planificar"]):
            return (
                "📋 ¡Excelente que quieras organizarte! Te sugiero: "
                "1️⃣ Anota todas tus tareas en la sección Recordatorios. "
                "2️⃣ Agrega tus actividades a la Agenda Semanal. "
                "3️⃣ Prioriza lo más urgente e importante primero. "
                "¿Por dónde quieres empezar? 🌟"
            )

        # Palabras clave positivas
        elif any(p in msg for p in ["bien", "feliz", "contenta", "contento", "genial", "excelente"]):
            return (
                "🌸 ¡Me alegra mucho escuchar eso! Aprovecha esta buena energía para avanzar "
                "con tus tareas más retadoras. Cuando estamos bien emocionalmente, aprendemos mejor. "
                "¡Sigue así! ✨"
            )

        # Palabras clave de tristeza
        elif any(p in msg for p in ["triste", "mal", "horrible", "pésimo", "pesimo", "deprimida", "deprimido"]):
            return (
                "💜 Lo siento mucho. Está bien no estar bien siempre. "
                "Permítete sentir lo que sientes. Si puedes, habla con alguien de confianza. "
                "Recuerda que eres más que tus resultados académicos o laborales. "
                "¿Hay algo concreto que te esté pesando? Puedo ayudarte a organizarlo. 🤗"
            )

        # Palabras clave de motivación
        elif any(p in msg for p in ["motivación", "motivacion", "motivada", "motivado", "ánimo", "animo"]):
            return (
                "🚀 ¡Aquí va tu dosis de motivación! Cada día que llegas al trabajo Y estudias "
                "estás construyendo una versión más fuerte de ti. "
                "Los resultados no siempre se ven de inmediato, pero el esfuerzo siempre cuenta. "
                "¡Tú tienes lo que se necesita! 💪✨"
            )

        # Respuesta por defecto
        else:
            return (
                "🌸 Gracias por escribirme. Puedo ayudarte si me cuentas sobre: "
                "**estrés**, **cansancio**, **pruebas o exámenes**, **organización**, "
                "o simplemente cómo te sientes. ¿Qué necesitas hoy? 💜"
            )

    # Mostrar historial de chat
    st.markdown("### 💬 Conversación")
    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.chat_historial:
            if msg["rol"] == "bot":
                st.markdown(
                    f"<div class='chat-bot'><span class='chat-avatar'>🤖</span>{msg['mensaje']}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='chat-user'>{msg['mensaje']}<span class='chat-avatar' style='margin-left:8px;'>👩‍🎓</span></div>",
                    unsafe_allow_html=True
                )

    st.markdown("---")

    # Campo de entrada del usuario
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        user_input = st.text_input(
            "Escribe tu mensaje:",
            placeholder="Ej: me siento estresada con los exámenes...",
            key="chat_input",
            label_visibility="collapsed"
        )
    with col_btn:
        enviar = st.button("Enviar 💬")

    if enviar and user_input.strip():
        # Agregar mensaje del usuario al historial
        st.session_state.chat_historial.append({
            "rol": "usuario",
            "mensaje": user_input.strip()
        })
        # Obtener y agregar respuesta del bot
        respuesta = obtener_respuesta(user_input.strip())
        st.session_state.chat_historial.append({
            "rol": "bot",
            "mensaje": respuesta
        })
        st.rerun()

    # Botón para limpiar el chat
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.chat_historial = [
            {"rol": "bot", "mensaje": "¡Hola de nuevo! 🌸 ¿Cómo te sientes hoy? Estoy aquí para ayudarte."}
        ]
        st.rerun()

    # Sugerencias rápidas
    st.markdown("### 💡 Puedes escribir sobre:")
    sugerencias = ["😰 Estrés", "📚 Prueba o examen", "😴 Cansancio", "📋 Organizarme", "😊 Cómo me siento"]
    cols = st.columns(len(sugerencias))
    for i, sug in enumerate(sugerencias):
        with cols[i]:
            st.markdown(
                f"<div style='background:white; border-radius:12px; padding:8px 12px; "
                f"text-align:center; font-size:13px; font-weight:600; color:#6a4c93; "
                f"box-shadow:0 2px 8px rgba(106,76,147,0.15); border: 1.5px solid #e0d5f5;'>"
                f"{sug}</div>",
                unsafe_allow_html=True
            )


# ══════════════════════════════════════════════
# PÁGINA 5: BIENESTAR
# ══════════════════════════════════════════════
elif pagina == "💆 Bienestar":

    st.markdown("# 💆 Bienestar y Cuidado Personal")
    st.markdown("Chequea cómo estás hoy y recibe recomendaciones personalizadas. 🌿")

    # ── Selector de estado de ánimo ──
    st.markdown("### 🌈 ¿Cómo te sientes en este momento?")

    estados = {
        "😊 Feliz":     ("feliz",     "#fffacd", "#856404", "¡Qué buena energía! Aprovéchala para avanzar con tus metas. Hoy es un gran día para estudiar esos temas difíciles. Comparte tu buena vibra con quienes te rodean. ✨"),
        "🙂 Bien":      ("bien",      "#d4edda", "#155724", "Estás en un buen punto de equilibrio. Mantén tus hábitos de estudio y descanso. Una caminata corta hoy puede mantenerte así. 🌿"),
        "😐 Normal":    ("normal",    "#e8f4fd", "#0c5460", "Es un día tranquilo. Haz una lista de tus prioridades y empieza por la más pequeña. A veces el movimiento crea motivación. 📋"),
        "😰 Estresada": ("estresada", "#fce4ec", "#880e4f", "Tómate un respiro. Antes de continuar, prueba la respiración guiada abajo. Divide tus tareas en partes pequeñas y recuerda que no tienes que hacerlo todo hoy. 💜"),
        "😩 Agotada":   ("agotada",  "#f3e5f5", "#4a148c", "Tu cuerpo y mente necesitan recuperarse. Prioriza el descanso sobre cualquier tarea. Una siesta de 20 min puede hacer maravillas. Hoy permítete hacer solo lo esencial. 🌙"),
    }

    estado_seleccionado = st.radio(
        "Estado de ánimo:",
        list(estados.keys()),
        horizontal=True,
        label_visibility="collapsed"
    )

    if estado_seleccionado:
        clave, bg, text_color, recomendacion = estados[estado_seleccionado]
        st.markdown(
            f"""<div style='background:{bg}; border-radius:16px; padding:20px 24px;
            margin:16px 0; border-left:5px solid {text_color};'>
            <h4 style='color:{text_color}; margin:0 0 8px 0;'>💡 Recomendación para ti</h4>
            <p style='color:{text_color}; margin:0; font-size:15px; font-weight:600;'>
            {recomendacion}
            </p></div>""",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ── Sección de respiración guiada ──
    st.markdown("### 🫁 Respiración Guiada")
    st.markdown("Sigue estas instrucciones para calmar tu mente en 2 minutos:")

    st.markdown("""
    <div class='breath-box'>
        <h3 style='color:#6a4c93; margin-bottom:20px;'>🌬️ Técnica 4-4-6</h3>
        <div style='display:flex; gap:16px; justify-content:center; flex-wrap:wrap;'>
            <div style='background:white; border-radius:16px; padding:20px; min-width:140px;
                        box-shadow: 0 4px 15px rgba(106,76,147,0.12); text-align:center;'>
                <div style='font-size:36px; margin-bottom:8px;'>👃</div>
                <div style='color:#6a4c93; font-weight:800; font-size:18px;'>Inhala</div>
                <div style='color:#9b8bc7; font-size:28px; font-weight:800;'>4 seg</div>
                <div style='color:#aaa; font-size:13px;'>Por la nariz</div>
            </div>
            <div style='background:white; border-radius:16px; padding:20px; min-width:140px;
                        box-shadow: 0 4px 15px rgba(106,76,147,0.12); text-align:center;'>
                <div style='font-size:36px; margin-bottom:8px;'>⏸️</div>
                <div style='color:#5b8db8; font-weight:800; font-size:18px;'>Mantén</div>
                <div style='color:#7aadd4; font-size:28px; font-weight:800;'>4 seg</div>
                <div style='color:#aaa; font-size:13px;'>Sin moverse</div>
            </div>
            <div style='background:white; border-radius:16px; padding:20px; min-width:140px;
                        box-shadow: 0 4px 15px rgba(106,76,147,0.12); text-align:center;'>
                <div style='font-size:36px; margin-bottom:8px;'>💨</div>
                <div style='color:#3a8b5e; font-weight:800; font-size:18px;'>Exhala</div>
                <div style='color:#6ab89a; font-size:28px; font-weight:800;'>6 seg</div>
                <div style='color:#aaa; font-size:13px;'>Por la boca</div>
            </div>
        </div>
        <p style='color:#7a5fa0; margin-top:20px; font-size:14px; font-weight:600;'>
        🔁 Repite este ciclo <strong>3 a 5 veces</strong> para sentir el efecto calmante.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Hábitos de bienestar ──
    st.markdown("### ✨ Hábitos de bienestar para estudiantes trabajadoras/es")

    habitos = [
        ("💧", "Hidratación",       "Toma al menos 8 vasos de agua al día. La deshidratación afecta la concentración."),
        ("🥗", "Alimentación",      "Come algo nutritivo antes de estudiar. El cerebro necesita energía real."),
        ("🚶", "Movimiento",        "15 minutos de caminata al día reducen el estrés y mejoran la memoria."),
        ("📵", "Descanso digital",  "Apaga el celular 30 min antes de dormir para mejorar la calidad del sueño."),
        ("📓", "Journaling",        "Escribir 3 cosas positivas del día activa tu bienestar emocional."),
        ("🤝", "Apoyo social",      "Comparte cómo te sientes con alguien de confianza. No cargues todo sola/solo."),
    ]

    col1, col2 = st.columns(2)
    for i, (emoji, titulo, desc) in enumerate(habitos):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(
                f"""<div class='card' style='margin:8px 0;'>
                <div style='font-size:28px; margin-bottom:6px;'>{emoji}</div>
                <h4 style='color:#6a4c93; margin:0 0 4px 0;'>{titulo}</h4>
                <p style='color:#666; margin:0; font-size:14px;'>{desc}</p>
                </div>""",
                unsafe_allow_html=True
            )