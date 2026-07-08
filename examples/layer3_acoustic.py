#!/usr/bin/env python3
"""
LAYER 3: ACOUSTIC
Geometry → Sound (SWAM Synthesis + IFT8 Percussion)

Here the crystal vibrates. We synthesize audio from geometric structure.
"""

import numpy as np

class Layer3_Acoustic:
    def __init__(self, sample_rate=44100):
        self.sr = sample_rate
        self.tube_gain = 3.5
    
    def tube_preamp(self, signal):
        """Soft-clipping tube amplifier (asymmetric)"""
        return np.where(
            signal > 0,
            np.tanh(signal * self.tube_gain),
            np.arctan(signal * self.tube_gain * 0.8)
        )
    
    def fender_eq(self, signal, sample_rate=44100):
        """Twin Reverb EQ: Scoop at 500Hz, Bright above 3kHz"""
        spec = np.fft.rfft(signal)
        freqs = np.fft.rfftfreq(len(signal), 1/sample_rate)
        
        # Bright boost
        spec[freqs > 3000] *= 2.0
        # Scoop (classic Fender)
        spec[(freqs > 400) & (freqs < 600)] *= 0.3
        
        return np.fft.irfft(spec)
    
    def swam_friction(self, geometry, duration=1.0):
        """SWAM: Synthesis and Wavetable from Additive Modeling
        Simulates crystal friction sound"""
        
        # Calculate velocity from geometry displacements
        points = len(geometry)
        t = np.linspace(0, duration, int(duration * self.sr))
        
        # Resonance frequency (Silicon crystal harmonic)
        f_resonance = 543  # Hz
        
        # Generate base oscillation
        base = np.sin(2 * np.pi * f_resonance * t)
        
        # Modulate by geometry
        if len(geometry) > 0:
            geometry_energy = np.mean(np.abs(geometry))
            modulation = 1.0 + (geometry_energy * 0.5)
        else:
            modulation = 1.0
        
        # Add friction noise
        friction = np.random.normal(0, 0.1, len(t))
        
        # Combine
        signal = (base * modulation + friction * 0.2) * 0.5
        
        return signal
    
    def ift8_percussion(self, binary_string, duration=2.0):
        """IFT8: Binary → Percussion Pattern
        Each 8-bit group generates a drum beat"""
        
        bpm = 120
        beat_duration = (60.0 / bpm) / 4  # Sixteenth note
        
        audio = []
        
        # Process each byte (8 bits)
        for byte_idx in range(0, len(binary_string), 8):
            byte = binary_string[byte_idx:byte_idx+8]
            
            # Map bits to percussion
            for bit_idx, bit in enumerate(byte):
                if bit == '1':
                    # KICK on bits 1,2 (low freq)
                    freq = 60
                    if bit_idx in [4]:  # Bit 4 = SNARE (high freq)
                        freq = 1200
                else:
                    # Silence
                    freq = 0
                
                # Generate tone
                t_local = np.linspace(0, beat_duration, int(beat_duration * self.sr), endpoint=False)
                if freq > 0:
                    tone = np.sin(2 * np.pi * freq * t_local) * 0.5
                    # Envelope
                    envelope = np.exp(-5 * t_local / beat_duration)
                    audio.append(tone * envelope)
                else:
                    audio.append(np.zeros_like(t_local))
        
        return np.concatenate(audio) if audio else np.array([])
    
    def print_info(self, signal):
        if len(signal) > 0:
            print(f"  Duration: {len(signal) / self.sr:.2f}s")
            print(f"  Peak: {np.max(np.abs(signal)):.3f}")
            print(f"  RMS: {np.sqrt(np.mean(signal**2)):.3f}")


# --- DEMONSTRATION ---
if __name__ == "__main__":
    print("\n" + "#"*70)
    print("# WAKA-OS LAYER 3: ACOUSTIC SYNTHESIS")
    print("#"*70)
    
    layer3 = Layer3_Acoustic()
    
    # Example 1: SWAM Friction
    print(f"\n[SWAM] Crystal Friction Synthesis")
    geometry = np.random.normal(0, 0.001, 512)
    signal_swam = layer3.swam_friction(geometry, duration=1.0)
    signal_swam_processed = layer3.tube_preamp(signal_swam)
    signal_swam_processed = layer3.fender_eq(signal_swam_processed)
    print("  Generated:")
    layer3.print_info(signal_swam_processed)
    
    # Example 2: IFT8 Percussion
    print(f"\n[IFT8] Binary → Drum Pattern")
    binary = "11001010" * 5
    signal_perc = layer3.ift8_percussion(binary, duration=2.0)
    signal_perc = layer3.tube_preamp(signal_perc)
    print(f"  Pattern: {binary}")
    print("  Generated:")
    layer3.print_info(signal_perc)
    
    # Example 3: Combined
    print(f"\n[COMBINED] SWAM + IFT8 Orchestration")
    combined = signal_swam_processed[:len(signal_perc)] + signal_perc
    combined = layer3.tube_preamp(combined) * 0.5  # Prevent clipping
    print("  Generated:")
    layer3.print_info(combined)
    
    print("\n" + "="*70)
    print(" ✅ Layer 3 complete. Geometry vibrates as sound.")
    print(" Next: Layer 4 measures the thermal consequences.")
    print("="*70 + "\n")
