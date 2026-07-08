#!/usr/bin/env python3
"""
LAYER 5: MUTATION
Thermal Stress → Autonomous Text Transformation (Glitch Feedback)

The final loop: stress corrupts the original message.
The output becomes the new input. Möbius computes.
"""

import numpy as np
import random
import time

class Layer5_Mutation:
    def __init__(self, bpm_base=120):
        self.bpm = bpm_base
        self.stress = 0.0
        self.glitch_symbols = ["ø", "µ", "§", "æ", "∞", "∆", "†", "‡", "¢", "¤"]
        self.archive = []
    
    def corrupt_text(self, text, corruption_rate=0.2):
        """Randomly replace characters with glitch symbols"""
        text_list = list(text)
        num_corruptions = max(1, int(len(text) * corruption_rate))
        
        for _ in range(num_corruptions):
            idx = random.randint(0, len(text_list) - 1)
            text_list[idx] = random.choice(self.glitch_symbols)
        
        return "".join(text_list)
    
    def stress_to_bpm(self, thermal_stress):
        """Convert thermal stress (0-1) to BPM acceleration"""
        # Base 120 BPM → up to 300 BPM at full stress
        self.bpm = 120 + (thermal_stress * 180)
        return self.bpm
    
    def simulate_autonomous_loop(self, initial_text, thermal_stress_curve, iterations=20):
        """Simulate the complete feedback loop"""
        current_text = initial_text
        self.archive = []
        
        print(f"\n[AUTONOMOUS LOOP] {iterations} cycles of text mutation")
        print(f"  Input: {initial_text!r}")
        print(f"\n  Cycle │ Text                       │ Stress │ BPM   │ Corruption")
        print(f"  ─────────────────────────────────────────────────────────────")
        
        for cycle in range(iterations):
            # Get stress for this cycle
            if cycle < len(thermal_stress_curve):
                self.stress = thermal_stress_curve[cycle]
            
            # Stress drives BPM
            self.stress_to_bpm(self.stress)
            
            # Corruption probability increases with stress
            corruption_rate = 0.05 + (self.stress * 0.25)
            
            # Apply mutation
            mutated_text = self.corrupt_text(current_text, corruption_rate)
            
            # Record
            self.archive.append({
                'cycle': cycle,
                'text': mutated_text,
                'stress': self.stress,
                'bpm': self.bpm,
                'corruption': corruption_rate
            })
            
            # Display
            text_display = mutated_text[:23].ljust(23)
            print(f"  {cycle:4d}  │ {text_display} │ {self.stress:5.1%} │ {self.bpm:5.0f} │ {corruption_rate:5.1%}")
            
            # Update for next iteration
            current_text = mutated_text
            
            # If corruption is too high, system becomes incomprehensible
            if corruption_rate > 0.4:
                print(f"  ...")
                print(f"  [SYSTEM DEGRADATION] Text has become unrecognizable.")
                break
        
        return current_text
    
    def print_evolution(self):
        """Show text evolution over time"""
        print(f"\n[TEXT EVOLUTION]")
        print(f"  {self.archive[0]['text']!r}  (initial)")
        for i in range(1, min(5, len(self.archive))):
            print(f"  {self.archive[i]['text']!r}  (cycle {i})")
        if len(self.archive) > 5:
            print(f"  ...")
            print(f"  {self.archive[-1]['text']!r}  (final)")


# --- DEMONSTRATION ---
if __name__ == "__main__":
    print("\n" + "#"*70)
    print("# WAKA-OS LAYER 5: MUTATION & GLITCH FEEDBACK")
    print("#"*70)
    
    layer5 = Layer5_Mutation()
    
    # Scenario 1: Low stress
    print(f"\n[SCENARIO 1] Low Thermal Stress")
    text = "WAKA-OS-SUPREME"
    # Gradual stress curve
    stress_curve = np.linspace(0.0, 0.2, 15).tolist()
    layer5.simulate_autonomous_loop(text, stress_curve, iterations=15)
    layer5.print_evolution()
    
    # Scenario 2: Rapid escalation
    print(f"\n[SCENARIO 2] Rapid Thermal Escalation")
    text = "SILICON-GHOST"
    # Fast stress spike
    stress_curve = [0.1, 0.2, 0.3, 0.5, 0.7, 0.85, 0.95]
    layer5.simulate_autonomous_loop(text, stress_curve, iterations=10)
    layer5.print_evolution()
    
    print("\n" + "="*70)
    print(" ✅ Layer 5 complete. The Möbius loop is closed.")
    print("\n The output became the input.")
    print(" The text evolved through stress.")
    print(" The system learned by degrading.")
    print("="*70 + "\n")
