# Audio Processing Tool

Este proyecto implementa un procesador de audio que aplica filtros de banda y analiza señales de audio. El procesador puede manejar múltiples archivos de audio y generar análisis de frecuencia en formato CSV.

## Estructura del Proyecto
```
audio-processor/
├── src/
│   └── audio_processor.py
├── tests/
│   └── test_audio_processor.py
├── examples/
│   └── example_usage.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/yourusername/audio-processor.git
cd audio-processor
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

```python
from audio_processor import AudioProcessor

# Crear una instancia del procesador
processor = AudioProcessor(
    input_folder="path/to/audio/files",
    output_base_folder="path/to/output"
)

# Procesar todos los archivos en la carpeta
processor.process_folder()
```

## Requisitos

- Python 3.8+
- NumPy
- SciPy
- pandas
- soundfile
