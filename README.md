# Agencia de Viajes Inteligente

Proyecto prototipo que combina agentes BDI (Jason) con agentes LLM (Groq / Ollama) y búsquedas web para generar informes de viaje.

Resumen de carpetas:
- `Groq/` — versión que usa Groq LLM.
- `Ollama Local/` — versión local que usa Ollama.
- `Ollama Local/Trabajo_Final_Agentes/` — ejemplo con agentes Jason, puente Java y API Flask.

Preparar antes de ejecutar:
1. Copia el archivo de ejemplo de variables: `cp Groq/.env.example Groq/.env` y/o `cp "Ollama Local"/.env.example "Ollama Local"/.env`.
2. Rellena las claves en los `.env` locales (no subirlos al repo).
3. Instala dependencias en la carpeta que vayas a usar:
```bash
python -m venv venv
source venv/bin/activate
pip install -r "Groq/requirements.txt"    # o "Ollama Local/requirements.txt"
```
4. Ejecuta `python "Groq/main.py"` o `python "Ollama Local/main.py"` según la variante.

Notas:
- Los archivos `.env` deben contener claves reales; por seguridad se han reemplazado por placeholders en el repositorio.
- No subas tus claves ni el archivo `.env` a GitHub. Usa GitHub Secrets para CI/Despliegue.