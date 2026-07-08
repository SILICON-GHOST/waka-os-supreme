#!/usr/bin/env python3
"""
LAYER 1: LINGUISTIC
Text → Binary encoding

This is the foundation: converting human language into quantized form.
Nothing fancy—just pure lexical transformation.
"""

import numpy as np

class Layer1_Linguistic:
    def __init__(self):
        self.archive = []
    
    def text_to_binary(self, text):
        """Convert text to 8-bit binary representation"""
        binary = "".join(f"{ord(c):08b}" for c in text)
        return binary
    
    def binary_to_text(self, binary):
        """Reverse: binary back to text (lossy if corrupted)"""
        chars = []
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                try:
                    chars.append(chr(int(byte, 2)))
                except:
                    chars.append("?")
        return "".join(chars)
    
    def parse_rtttl(self, rtttl_string):
        """Parse RTTTL (Ring Tone Text Transfer Language) format"""
        # Format: Name:Control,Control:Note,Note,Note
        parts = rtttl_string.split(':')
        name = parts[0]
        
        if len(parts) == 3:
            control = parts[1]
            notes = parts[2].split(',')
        else:
            control = ""
            notes = parts[1].split(',')
        
        # Parse control (bpm, octave, duration)
        params = {}
        for param in control.split(','):
            if '=' in param:
                k, v = param.split('=')
                params[k.strip()] = v.strip()
        
        return {
            'name': name,
            'bpm': int(params.get('b', '120')),
            'octave': int(params.get('o', '5')),
            'duration': int(params.get('d', '4')),
            'notes': notes
        }
    
    def gravure_manifeste(self, text, freq=55.84547):
        """Store text in crystal lattice (conceptually)"""
        binary = self.text_to_binary(text)
        self.archive.append({
            'text': text,
            'binary': binary,
            'frequency': freq,
            'length': len(binary)
        })
        return binary
    
    def print_state(self):
        print("\n" + "="*70)
        print(" LAYER 1: LINGUISTIC STATE")
        print("="*70)
        
        for i, entry in enumerate(self.archive):
            print(f"\n[Archive {i}]")
            print(f"  Text:     {entry['text']!r}")
            print(f"  Binary:   {entry['binary'][:40]}... (len={entry['length']})")
            print(f"  Frequency: {entry['frequency']} Hz (gravure point)")


# --- DEMONSTRATION ---
if __name__ == "__main__":
    layer1 = Layer1_Linguistic()
    
    print("\n" + "#"*70)
    print("# WAKA-OS LAYER 1: LINGUISTIC TRANSFORMATION")
    print("#"*70)
    
    # Example 1: Simple text encoding
    print("\n[EXAMPLE 1] Simple Text Encoding")
    text = "HELLO"
    binary = layer1.text_to_binary(text)
    print(f"  Input:  {text}")
    print(f"  Binary: {binary}")
    print(f"  Back:   {layer1.binary_to_text(binary)}")
    
    # Example 2: Store manifesto
    print("\n[EXAMPLE 2] Manifesto Gravure")
    manifesto = "We will conquer the planet"
    binary = layer1.gravure_manifeste(manifesto)
    print(f"  Stored: {manifesto!r}")
    print(f"  Bits:   {len(binary)} (each bit → atomic displacement)")
    
    # Example 3: RTTTL parsing
    print("\n[EXAMPLE 3] RTTTL Musical Notation")
    rtttl = "NokiaTune:d=4,o=5,b=225:8e6,8d6,f#,g#"
    parsed = layer1.parse_rtttl(rtttl)
    print(f"  Title:   {parsed['name']}")
    print(f"  BPM:     {parsed['bpm']}")
    print(f"  Notes:   {parsed['notes'][:3]}...")
    
    # Example 4: Multiple archives
    print("\n[EXAMPLE 4] Multiple Archives")
    layer1.gravure_manifeste("WAKA", freq=63.675)
    layer1.gravure_manifeste("SILICON", freq=440.0)
    layer1.print_state()
    
    print("\n" + "="*70)
    print(" ✅ Layer 1 complete. Text is now binary, ready for Layer 2.")
    print("="*70 + "\n")
