import os
import json
import time
import litellm
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

groq_key = obtener_api_key("GROQ_API_KEY", "API Key de Groq")
serper_key = obtener_api_key("SERPER_API_KEY", "API Key de Serper.dev")

litellm.num_retries = 5
litellm.retry_after = 40
litellm.drop_params = True

llm = LLM(
    model="openai/llama-3.3-70b-versatile",
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_key
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
        tools = [search_tool] if id_agente in ["validador_logistico", "scout", "contextualista"] else []
        
        agentes_dict[id_agente] = Agent(
            role=cfg["role"],
            goal=cfg["goal"],
            backstory=cfg["backstory"],
            llm=llm,
            tools=tools,
            verbose=True,
            allow_delegation=False,
            max_retry_limit=5
        )
    
    tareas_lista = []
    orden = [
        ("verificar_infraestructura", "validador_logistico"),
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
    mes_año = input("-> Mes y año (ej: agosto 2026): ").strip()
    dia_salida = input("-> Día exacto de salida (ej: 15): ").strip()

    print("\n[+] Iniciando agentes (con reintentos automaticos)...")
    
    max_intentos = 5
    for intento in range(1, max_intentos + 1):
        try:
            agentes, tareas = preparar_tripulacion(config, llm, search_tool)
            
            crew = Crew(
                agents=agentes,
                tasks=tareas,
                process=Process.sequential,
                verbose=True,
                max_rpm=5
            )

            resultado = crew.kickoff(inputs={
                "origen": origen,
                "destino": destino,
                "presupuesto": presupuesto,
                "periodo": mes_año,
                "dia": dia_salida
            })

            print("\n" + "="*60)
            print("  RESULTADO DEL VIAJE")
            print("="*60 + "\n")
            print(resultado)
            return

        except Exception as e:
            error_msg = str(e).lower()
            
            if "rate_limit" in error_msg or "429" in error_msg:
                espera = 60 * intento
                print(f"\n[!] Rate Limit alcanzado (intento {intento}/{max_intentos}).")
                print(f"    Esperando {espera}s antes de reintentar...")
                time.sleep(espera)
                
            elif "tool_use_failed" in error_msg or "failed_generation" in error_msg:
                espera = 15 * intento
                print(f"\n[!] El modelo genero un formato de herramienta invalido (intento {intento}/{max_intentos}).")
                print(f"    Esto es intermitente. Reintentando en {espera}s...")
                time.sleep(espera)
                
            else:
                print(f"\n[ERROR] Error inesperado: {e}")
                return

    print("\n[ERROR] Se agotaron los {max_intentos} reintentos. Espera unos minutos e intentalo de nuevo.")

if __name__ == "__main__":
    main()
