# Agencia de Viajes Inteligente

Proyecto con dos versiones:

- `Groq/`: versión con Groq.
- `Ollama Local/`: versión con Ollama local.

## Si ya lo tienes instalado

### Groq

```bash
cd "/home/rodrigo/Agentes_Inteligentes/Trabajo/Agentes_Inteligentes_ws/Groq"
source venv/bin/activate
python main.py
```

### Ollama Local

```bash
ollama serve
```

En otra terminal:

```bash
cd "/home/rodrigo/Agentes_Inteligentes/Trabajo/Agentes_Inteligentes_ws/Ollama Local"
source venv/bin/activate
python main.py
```

## Si es la primera vez

### Groq

```bash
cd "/home/rodrigo/Agentes_Inteligentes/Trabajo/Agentes_Inteligentes_ws/Groq"
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

En `.env` pon:

```bash
GROQ_API_KEY=tu_clave_de_groq
SERPER_API_KEY=tu_clave_de_serper
```

### Ollama Local

```bash
cd "/home/rodrigo/Agentes_Inteligentes/Trabajo/Agentes_Inteligentes_ws/Ollama Local"
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Después:

```bash
ollama serve
ollama pull llama3.1
```

En `.env` pon:

```bash
SERPER_API_KEY=tu_clave_de_serper
```
