import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# 1. Configuracion de Entorno y APIs
load_dotenv()

def obtener_api_key(nombre_env, nombre_legible):
    key = os.getenv(nombre_env)
    if not key:
        print(f"\n[!] No se encontro {nombre_env} en el archivo .env")
        key = input(f"    Introduce tu {nombre_legible}: ").strip()
        os.environ[nombre_env] = key
    return key

# 2. Inicializacion Nativa del LLM (GROQ - 100% GRATIS)
groq_key = "YOUR_GROQ_API_KEY"
serper_key = obtener_api_key("SERPER_API_KEY", "API Key de Serper.dev")

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=groq_key
)

search_tool = SerperDevTool(api_key=serper_key)

# 3. Carga de Configuracion
def cargar_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando config.json: {e}")
        exit(1)

config = cargar_config()

# 4. Creacion de Agentes y Tareas (Logica Nativa)
def preparar_tripulacion(config, llm, search_tool):
    agentes_dict = {}
    
    # Agentes: Iteracion sobre el diccionario del JSON
    for id_agente, cfg in config["agents"].items():
        # Validador, scout y contextualista tienen herramientas de busqueda
        tools = [search_tool] if id_agente in ["validador_logistico", "scout", "contextualista"] else []
        
        agentes_dict[id_agente] = Agent(
            role=cfg["role"],
            goal=cfg["goal"],
            backstory=cfg["backstory"],
            llm=llm,
            tools=tools,
            verbose=True,
            allow_delegation=False
        )
    
    # Tareas: Vinculacion secuencial
    tareas_lista = []
    # Definimos el orden logico de las tareas segun sus IDs en el JSON
    orden = [
        ("verificar_infraestructura", "validador_logistico"), # Primera tarea
        ("busqueda_vuelos", "scout"),
        ("analisis_destino", "contextualista"),
        ("analisis_financiero", "analista_financiero"),
        ("resumen_final", "concierge")
    ]
    
    for id_tarea, id_agente in orden:
        cfg_tarea = config["tasks"][id_tarea]
        tareas_lista.append(Task(
            description=cfg_tarea["description"],
            expected_output=cfg_tarea["expected_output"],
            agent=agentes_dict[id_agente]
        ))
        
    return list(agentes_dict.values()), tareas_lista

# 5. Ejecucion Principal
def main():
    print("\n" + "="*60)
    print("  AGENCIA DE VIAJES INTELIGENTE (Native CrewAI)")
    print("="*60)

    # Captura de datos del usuario
    origen = input("\n-> Origen: ").strip()
    destino = input("-> Destino: ").strip()
    presupuesto = input("-> Presupuesto (EUR): ").strip()
    mes_año = input("-> Mes y año (ej: agosto 2026): ").strip()
    dia_salida = input("-> Día exacto de salida (ej: 15): ").strip()

    print("\n[+] Iniciando agentes con proteccion de cuota (max_rpm=10)...")
    
    agentes, tareas = preparar_tripulacion(config, llm, search_tool)
    
    # Crew con proteccion anti-baneo
    crew = Crew(
        agents=agentes,
        tasks=tareas,
        process=Process.sequential,
        verbose=True,
        max_rpm=10  # Regla estricta para evitar Error 429
    )

    # Inicio del proceso
    resultado = crew.kickoff(inputs={
        "origen": origen,
        "destino": destino,
        "presupuesto": presupuesto,
        "periodo": mes_año,
        "dia": dia_salida  # Nueva variable enviada a los agentes
    })

    print("\n" + "="*60)
    print("  RESULTADO DEL VIAJE")
    print("="*60 + "\n")
    print(resultado)

if __name__ == "__main__":
    main()
