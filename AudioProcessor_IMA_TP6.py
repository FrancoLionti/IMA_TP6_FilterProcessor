import numpy as np
from scipy import signal
import soundfile as sf
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class AudioProcessor_IMA_TP6:
    def __init__(self, input_folder, output_base_folder="processed_output"):
        """
        Initialize the audio processor with input and output paths
        """
        self.input_folder = Path(input_folder)
        self.output_base_folder = Path(output_base_folder)
        
        # Sample rate configuration
        self.sampleRate = 48000.0
        self.nyquistRate = self.sampleRate/2.0
        
        # Specific center frequencies (50 Hz to 5 kHz)
        self.centerFrequency_Hz = np.array([
            50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 
            630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000
        ])
        
        # Calculate bandwidth
        G = 2
        factor = np.power(G, 1.0/6.0)
        self.lowerCutoffFrequency_Hz = self.centerFrequency_Hz/factor
        self.upperCutoffFrequency_Hz = self.centerFrequency_Hz*factor
        
        # Create output directory
        self.create_output_directories()
    
    def create_output_directories(self):
        """
        Create the directory structure for outputs
        """
        self.output_base_folder.mkdir(exist_ok=True)
        self.csv_output = self.output_base_folder / "csv_data"
        self.csv_output.mkdir(exist_ok=True)
    
    def process_audio(self, audio_path):
        """
        Process a single audio file
        """
        print(f"\nProcessing: {audio_path.name}")
        
        # Read audio file
        audio_data, fs = sf.read(audio_path)
        if fs != self.sampleRate:
            print(f"Warning: File sample rate ({fs} Hz) differs from expected ({self.sampleRate} Hz)")
        
        # Apply filters and get filtered signals
        filtered_signals = self.apply_filters(audio_data)
        
        # Calculate and export band responses
        self.export_band_responses(filtered_signals, audio_path.stem)
        
        print(f"Completed processing: {audio_path.name}")
    
    def apply_filters(self, audio_data):
        """
        Apply all filters to the audio data
        """
        filtered_signals = []
        for lower, upper, center in zip(self.lowerCutoffFrequency_Hz, 
                                      self.upperCutoffFrequency_Hz, 
                                      self.centerFrequency_Hz):
            order = 2 if center < 100 else 4
            sos = signal.butter(
                N=order,
                Wn=np.array([lower, upper])/self.nyquistRate,
                btype='bandpass',
                analog=False,
                output='sos'
            )procesar
            filtered = signal.sosfiltfilt(sos, audio_data, padtype='constant')
            filtered_signals.append(filtered)
        return filtered_signals
    
    def calculate_band_level(self, signal):
        """
        Calculate the RMS level in dB for a signal
        """
        rms = np.sqrt(np.mean(np.square(signal)))
        return 20 * np.log10(rms) if rms > 0 else -100
    
    def export_band_responses(self, filtered_signals, filename):
        """
        Export band responses in a clean, organized format
        """
        # Calculate band levels
        band_levels = []
        for signal in filtered_signals:
            level = self.calculate_band_level(signal)
            band_levels.append(level)
        
        # Create DataFrame
        df = pd.DataFrame({
            'Frequency (Hz)': self.centerFrequency_Hz,
            'Band Level (dB)': band_levels
        })
        
        # Export to CSV
        csv_path = self.csv_output / f"{filename}_band_levels.csv"
        df.to_csv(csv_path, index=False, float_format='%.2f')
        print(f"Exported band levels to: {csv_path}")
    
    def process_folder(self):
        """
        Process all audio files in the input folder
        """
        audio_extensions = ['.wav', '.WAV']
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(self.input_folder.glob(f'*{ext}'))
        
        if not audio_files:
            print(f"No audio files found in {self.input_folder}")
            return
        
        print(f"Found {len(audio_files)} audio files to process")
        
        for audio_file in audio_files:
            self.process_audio(audio_file)
        
        print("\n Batch processing complete!")
        print(f"Results saved in: {self.output_base_folder.absolute()}")

# Example usage
if __name__ == "__main__":
    processor = AudioProcessor_IMA_TP6_IMA_TP6(
        input_folder="MEDICIONES TR Y L/L E",
        output_base_folder="processed_output"
    )
    processor.process_folder()