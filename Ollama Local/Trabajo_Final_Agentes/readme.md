# 🌍 Sistema Multi-Agente de Planificación de Viajes (Jason + CrewAI)

Este proyecto es una aplicación híbrida que combina el razonamiento lógico BDI (Believe-Desire-Intention) de **Jason** con la potencia de los Agentes de IA modernos y búsqueda en tiempo real mediante **Python (Flask)** y la API de **Serper (Google Search)**.

## 🏗️ Arquitectura del Sistema

El sistema se divide en tres capas:
1. **Capa de Usuario (Jason/AgentSpeak):** Interfaz y flujo de decisiones lógicas.
2. **Capa Puente (Java/HTTP):** Conexión mediante solicitudes POST.
3. **Capa de Inteligencia (Python/CrewAI-Sim):** Procesamiento de datos reales extraídos de Google.

---

## 🚀 Instrucciones de Lanzamiento

Sigue estos pasos en orden para ejecutar la demostración:

### 1. Preparación del Entorno Python
Abre una terminal en la carpeta `1_IA_CrewAI` y activa tu entorno virtual:

```bash
cd ~/Escritorio/UPV/cuatri_6/agentes_trabajos/Proyecto_Agencia_Viajes/1_IA_CrewAI
source venv/bin/activate
```

### 2. Configuración de Credenciales

Debes exportar tu clave de API de Serper para permitir que los agentes busquen información real en Google:
```bash
# Exporta tu clave real antes de usar búsquedas en vivo (no incluir en el repo)
export SERPER_API_KEY="YOUR_SERPER_API_KEY"
```

### 3. Lanzar el Servidor de Inteligencia (Python)

Ejecuta el script de Flask que gestiona los agentes de IA:
```bash
python api_crewai.py
```
El servidor se iniciará en http://127.0.0.1:5000.

### 4. Lanzar el Sistema Multi-Agente (Jason)

    Abre tu IDE de Jason o ejecuta mediante Gradle/Ant.

    Inicia el proyecto (esto lanzará los agentes interfaz, director, etc.).

    Introduce los datos (Origen, Destino, Presupuesto) cuando la interfaz lo solicite.

### cosas: 
varias opciones de vuelo 2 o 3, con sus fechas. en cosas interesantes, esta bien, pero mejorarlo, sale raro. q te ponga "las 5 cosas mas importantes que ver en ...". si no hay vuelos por fechas, o por presupuesto, que de diga el pq.