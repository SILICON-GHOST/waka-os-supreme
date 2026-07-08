#!/usr/bin/env python3
"""
LAYER 4: THERMAL
Acoustic Energy → Heat Dissipation & System Stress

Here we model REAL physics: energy becomes heat, heat constrains behavior.
"""

import numpy as np
from enum import Enum

class SystemState(Enum):
    NOMINAL = 0
    COMPRESSED = 1
    THERMAL_STRESS = 2
    CRITICAL = 3

class Layer4_Thermal:
    def __init__(self):
        # Physical constants (Silicon/Aluminum)
        self.M_CORE_CP = 2000.0 * 500.0      # Heat capacity of core
        self.M_SHELL_CP = 500.0 * 800.0      # Heat capacity of shell
        self.K_SHELL = 0.15                  # Thermal conductivity
        
        # Initial temperatures (Celsius)
        self.t_core = 24.0
        self.t_shell = 21.0
        self.t_ambient = 15.0
        
        self.state = SystemState.NOMINAL
        self.history = []
    
    def audio_to_heat(self, signal, charge_factor=0.5):
        """Convert audio RMS energy to thermal power"""
        rms = np.sqrt(np.mean(signal**2))
        # P = I^2 * R, roughly: thermal_power ∝ signal_energy
        power = (rms ** 2) * charge_factor * 500.0
        return power
    
    def simulate_thermal_step(self, audio_signal, dt=0.01):
        """Simulate one timestep of thermal dynamics"""
        # Calculate heat generation from audio
        heat_generated = self.audio_to_heat(audio_signal)
        
        # Heat transfer between core and shell
        flux_internal = self.K_SHELL * (self.t_core - self.t_shell)
        
        # Heat dissipation to environment
        flux_external = 0.25 * (self.t_ambient - self.t_shell)
        
        # Update temperatures (simplified thermal model)
        dt_core = (heat_generated - flux_internal) / self.M_CORE_CP * dt
        dt_shell = (-flux_internal + flux_external) / self.M_SHELL_CP * dt
        
        self.t_core += dt_core
        self.t_shell += dt_shell
        
        # Clamp to physical limits
        self.t_core = np.clip(self.t_core, 5, 125)
        self.t_shell = np.clip(self.t_shell, 5, 120)
        
        # State machine
        self._update_state()
        
        # Record
        self.history.append({
            'time': len(self.history) * dt,
            't_core': self.t_core,
            't_shell': self.t_shell,
            'heat_gen': heat_generated,
            'state': self.state.name
        })
        
        return self.state
    
    def _update_state(self):
        """State machine for thermal management"""
        if self.t_core > 95.0:
            self.state = SystemState.CRITICAL
        elif self.t_core > 85.0:
            self.state = SystemState.THERMAL_STRESS
        elif self.t_core > 75.0:
            self.state = SystemState.COMPRESSED
        else:
            self.state = SystemState.NOMINAL
    
    def get_stress_metric(self):
        """Compute system stress (0.0 to 1.0)"""
        # Normalize: 24°C (nominal) → 0.0, 95°C (critical) → 1.0
        stress = max(0, (self.t_core - 24.0) / (95.0 - 24.0))
        return min(1.0, stress)
    
    def cooling_cycle(self, duration=5.0):
        """Passively cool the system"""
        steps = int(duration / 0.01)
        for _ in range(steps):
            # No audio input → only passive cooling
            silence = np.zeros(512)
            self.simulate_thermal_step(silence, dt=0.01)
    
    def print_status(self):
        stress = self.get_stress_metric()
        print(f"\n  Core:     {self.t_core:.1f}°C")
        print(f"  Shell:    {self.t_shell:.1f}°C")
        print(f"  Ambient:  {self.t_ambient}°C")
        print(f"  State:    {self.state.name}")
        print(f"  Stress:   {stress:.1%}")


# --- DEMONSTRATION ---
if __name__ == "__main__":
    print("\n" + "#"*70)
    print("# WAKA-OS LAYER 4: THERMAL DYNAMICS")
    print("#"*70)
    
    layer4 = Layer4_Thermal()
    
    # Scenario 1: Normal operation
    print(f"\n[SCENARIO 1] Normal Audio Processing")
    print(f"  Simulating 10 seconds of audio...")
    for i in range(1000):
        # Moderate audio signal
        signal = np.sin(2 * np.pi * 440 * np.linspace(0, 0.01, 512)) * 0.3
        layer4.simulate_thermal_step(signal, dt=0.01)
    
    layer4.print_status()
    
    # Scenario 2: Aggressive audio
    print(f"\n[SCENARIO 2] Aggressive Audio (Extreme Stress)")
    print(f"  Simulating 5 seconds of heavy load...")
    for i in range(500):
        # Loud audio signal
        signal = np.sign(np.sin(2 * np.pi * 100 * np.linspace(0, 0.01, 512))) * 0.9
        layer4.simulate_thermal_step(signal, dt=0.01)
    
    layer4.print_status()
    
    # Scenario 3: Emergency cooling
    print(f"\n[SCENARIO 3] Emergency Cooling (No Audio)")
    print(f"  Cooling for 5 seconds...")
    layer4.cooling_cycle(duration=5.0)
    
    layer4.print_status()
    
    # Summary
    print(f"\n[HISTORY] Thermal Timeline")
    print(f"  Total states recorded: {len(layer4.history)}")
    temps_core = [h['t_core'] for h in layer4.history]
    print(f"  Core temp range: {min(temps_core):.1f}°C → {max(temps_core):.1f}°C")
    
    print("\n" + "="*70)
    print(" ✅ Layer 4 complete. Audio has thermal consequences.")
    print(" Next: Layer 5 uses stress to mutate the text.")
    print("="*70 + "\n")
