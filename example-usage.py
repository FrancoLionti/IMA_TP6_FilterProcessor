from src.audio_processor import AudioProcessor
import pathlib

def main():
    # Ejemplo básico de uso
    processor = AudioProcessor(
        input_folder="input_audio",
        output_base_folder="processed_output"
    )
    processor.process_folder()

    # Ejemplo de procesamiento de un único archivo
    single_file = pathlib.Path("input_audio/sample.wav")
    if single_file.exists():
        processor.process_audio(single_file)

if __name__ == "__main__":
    main()
