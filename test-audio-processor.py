import unittest
import numpy as np
from pathlib import Path
from src.audio_processor import AudioProcessor

class TestAudioProcessor(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.processor = AudioProcessor(
            input_folder="test_audio",
            output_base_folder="test_output"
        )
        
    def test_init(self):
        """Test initialization of AudioProcessor."""
        self.assertEqual(self.processor.sampleRate, 48000.0)
        self.assertEqual(self.processor.nyquistRate, 24000.0)
        self.assertTrue(isinstance(self.processor.centerFrequency_Hz, np.ndarray))
        
    def test_calculate_band_level(self):
        """Test band level calculation."""
        # Test with known signal
        test_signal = np.ones(1000) * 0.5  # Should give -6.02 dB
        level = self.processor.calculate_band_level(test_signal)
        self.assertAlmostEqual(level, -6.02, places=2)
        
        # Test with zero signal
        zero_signal = np.zeros(1000)
        level = self.processor.calculate_band_level(zero_signal)
        self.assertEqual(level, -100)

if __name__ == '__main__':
    unittest.main()
