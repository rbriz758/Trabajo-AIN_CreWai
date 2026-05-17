import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

load_dotenv()

def obtener_api_key(nombre_env, nombre_legible):
    key = os.getenv(nombre_env)
    if not key:
        print(f"\n[!] No se encontro {nombre_env} en el archivo .env")
        key = input(f"    Introduce tu {nombre_legible}: ").strip()
        os.environ[nombre_env] = key
    return key

gemini_key = obtener_api_key("GEMINI_API_KEY", "API Key de Google Gemini")
serper_key = obtener_api_key("SERPER_API_KEY", "API Key de Serper.dev")

llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

search_tool = SerperDevTool(api_key=serper_key)

def cargar_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando config.json: {e}")
        exit(1)

config = cargar_config()

def preparar_tripulacion(config, llm, search_tool):
    agentes_dict = {}
    
    for id_agente, cfg in config["agents"].items():
        tools = [search_tool] if id_agente in ["scout", "contextualista"] else []
        
        agentes_dict[id_agente] = Agent(
            role=cfg["role"],
            goal=cfg["goal"],
            backstory=cfg["backstory"],
            llm=llm,
            tools=tools,
            verbose=True,
            allow_delegation=False
        )
    
    tareas_lista = []
    orden = [
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

def main():
    print("\n" + "="*60)
    print("  AGENCIA DE VIAJES INTELIGENTE (Native CrewAI)")
    print("="*60)

    origen = input("\n-> Origen: ").strip()
    destino = input("-> Destino: ").strip()
    presupuesto = input("-> Presupuesto (EUR): ").strip()
    periodo = input("-> Periodo (ej: agosto 2026): ").strip()

    print("\n[+] Iniciando agentes con proteccion de cuota (max_rpm=10)...")
    
    agentes, tareas = preparar_tripulacion(config, llm, search_tool)
    
    crew = Crew(
        agents=agentes,
        tasks=tareas,
        process=Process.sequential,
        verbose=True,
        max_rpm=10
    )

    resultado = crew.kickoff(inputs={
        "origen": origen,
        "destino": destino,
        "presupuesto": presupuesto,
        "periodo": periodo
    })

    print("\n" + "="*60)
    print("  RESULTADO DEL VIAJE")
    print("="*60 + "\n")
    print(resultado)

if __name__ == "__main__":
    main()
