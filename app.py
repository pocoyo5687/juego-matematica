import streamlit as st
import random
import time

# 1. Configuración de la pestaña web
st.set_page_config(
    page_title="MathQuest - Desafío Matemático",
    page_icon="🧮",
    layout="centered"
)

# Estilos visuales personalizados
st.markdown("""
<style>
    .title {
        font-size: 2.8rem;
        color: #2E5BFF;
        text-align: center;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #5A6A85;
        text-align: center;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🧮 MathQuest</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">¡Responde rápido, sube de nivel y bate tu propio récord!</div>', unsafe_allow_html=True)

# 2. Inicializar variables de juego en el Estado de la Sesión
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

def generar_pregunta():
    lvl = st.session_state.level
    if lvl == 1:
        st.session_state.num1 = random.randint(1, 10)
        st.session_state.num2 = random.randint(1, 10)
        st.session_state.operator = random.choice(['+', '-'])
    elif lvl == 2:
        st.session_state.num1 = random.randint(10, 50)
        st.session_state.num2 = random.randint(10, 50)
        st.session_state.operator = random.choice(['+', '-'])
    else:
        st.session_state.num1 = random.randint(3, 12)
        st.session_state.num2 = random.randint(3, 12)
        st.session_state.operator = '*'
    
    # GUARDAR LA RESPUESTA CORRECTA EN MEMORIA INMEDIATAMENTE
    if st.session_state.operator == '+':
        st.session_state.correct_ans = st.session_state.num1 + st.session_state.num2
    elif st.session_state.operator == '-':
        st.session_state.correct_ans = st.session_state.num1 - st.session_state.num2
    else:
        st.session_state.correct_ans = st.session_state.num1 * st.session_state.num2

# Generar la primera pregunta si no existe
if 'num1' not in st.session_state:
    generar_pregunta()

def reiniciar_juego():
    st.session_state.score = 0
    st.session_state.level = 1
    st.session_state.game_over = False
    generar_pregunta()

# Barra lateral informativa
st.sidebar.header("🎮 Reglas del Juego")
st.sidebar.write("Responde correctamente para acumular puntos. Cada 3 aciertos aumentará la dificultad.")
if st.sidebar.button("🔄 Reiniciar Partida"):
    reiniciar_juego()
    st.rerun()

# 4. Interfaz del Juego
if not st.session_state.game_over:
    # Marcador en tiempo real
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="🏆 Puntuación Actual", value=st.session_state.score)
    with col2:
        st.metric(label="⭐ Nivel de Dificultad", value=st.session_state.level)

    # Bloque visual de la pregunta matemática usando los datos guardados
    st.info(f"### ¿Cuánto es: &nbsp;&nbsp;`{st.session_state.num1} {st.session_state.operator} {st.session_state.num2}`?")

    # Formulario interactivo
    with st.form(key='math_form', clear_on_submit=True):
        user_ans = st.number_input("Escribe tu respuesta aquí:", step=1, value=0)
        submit_button = st.form_submit_button(label='Enviar Respuesta 🚀')

    if submit_button:
        # Comparar con la respuesta guardada de forma segura
        if user_ans == st.session_state.correct_ans:
            st.success("🎉 ¡Excelente! Respuesta correcta.")
            st.session_state.score += 1
            
            if st.session_state.score % 3 == 0:
                st.session_state.level += 1
                st.balloons()
                
            generar_pregunta()
            time.sleep(0.8)
            st.rerun()
        else:
            st.session_state.game_over = True
            st.rerun()

else:
    # Pantalla de derrota mostrando el resultado congelado
    st.error(f"❌ ¡Oh no, te has equivocado! La respuesta correcta era **{st.session_state.correct_ans}**.")
    st.subheader(f"📊 Resumen del juego:")
    st.write(f"- **Puntos totales:** {st.session_state.score}")
    st.write(f"- **Nivel alcanzado:** Nivel {st.session_state.level}")
    
    if st.button("🎮 Volver a Intentarlo"):
        reiniciar_juego()
        st.rerun()
