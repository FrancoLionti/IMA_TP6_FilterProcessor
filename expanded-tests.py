import unittest
import numpy as np
from pathlib import Path
from src.audio_processor import AudioProcessor
import shutil
import os

class TestAudioProcessor(unittest.TestCase):
    def setUp(self):
        """
        Se ejecuta antes de cada test.
        Configura el ambiente de prueba.
        """
        self.test_input_folder = Path("test_audio")
        self.test_output_folder = Path("test_output")
        
        # Crear directorios de prueba
        self.test_input_folder.mkdir(exist_ok=True)
        
        # Inicializar el procesador
        self.processor = AudioProcessor(
            input_folder=self.test_input_folder,
            output_base_folder=self.test_output_folder
        )

    def tearDown(self):
        """
        Se ejecuta después de cada test.
        Limpia el ambiente de prueba.
        """
        # Eliminar directorios de prueba
        if self.test_input_folder.exists():
            shutil.rmtree(self.test_input_folder)
        if self.test_output_folder.exists():
            shutil.rmtree(self.test_output_folder)

    def test_initialization(self):
        """Prueba la inicialización correcta del procesador."""
        self.assertEqual(self.processor.sampleRate, 48000.0)
        self.assertEqual(self.processor.nyquistRate, 24000.0)
        self.assertEqual(len(self.processor.centerFrequency_Hz), 21)
        self.assertTrue(self.test_output_folder.exists())
        self.assertTrue((self.test_output_folder / "csv_data").exists())

    def test_calculate_band_level(self):
        """Prueba el cálculo de niveles de banda."""
        # Caso 1: Señal constante
        test_signal = np.ones(1000) * 0.5
        level = self.processor.calculate_band_level(test_signal)
        self.assertAlmostEqual(level, -6.02, places=2)
        
        # Caso 2: Señal cero
        zero_signal = np.zeros(1000)
        level = self.processor.calculate_band_level(zero_signal)
        self.assertEqual(level, -100)
        
        # Caso 3: Señal sinusoidal
        t = np.linspace(0, 1, 1000)
        sine_signal = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
        level = self.processor.calculate_band_level(sine_signal)
        self.assertGreater(level, -10)  # El nivel debe ser razonable

    def test_filter_frequencies(self):
        """Prueba que las frecuencias de filtro estén en orden correcto."""
        for i in range(len(self.processor.centerFrequency_Hz) - 1):
            self.assertLess(
                self.processor.centerFrequency_Hz[i],
                self.processor.centerFrequency_Hz[i + 1]
            )
            self.assertLess(
                self.processor.lowerCutoffFrequency_Hz[i],
                self.processor.upperCutoffFrequency_Hz[i]
            )

    def test_apply_filters(self):
        """Prueba la aplicación de filtros."""
        # Crear una señal de prueba simple
        test_signal = np.random.random(1000)
        
        # Aplicar filtros
        filtered_signals = self.processor.apply_filters(test_signal)
        
        # Verificar que tenemos el número correcto de señales filtradas
        self.assertEqual(
            len(filtered_signals), 
            len(self.processor.centerFrequency_Hz)
        )
        
        # Verificar que cada señal filtrada tiene la misma longitud que la original
        for filtered in filtered_signals:
            self.assertEqual(len(filtered), len(test_signal))

if __name__ == '__main__':
    unittest.main()
