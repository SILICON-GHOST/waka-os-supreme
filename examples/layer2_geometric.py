#!/usr/bin/env python3
"""
LAYER 2: GEOMETRIC
Binary → 3D Coordinates in crystalline structure

Here we take the flat binary and sculpt it into 3D space.
Each bit becomes an atomic displacement in the silicon lattice.
"""

import numpy as np
import sys

class Layer2_Geometric:
    def __init__(self, lattice_size=(10, 10, 10)):
        self.size = lattice_size
        # Silicon crystal structure (diamond cubic)
        self.base_vectors = np.array([
            [0, 0, 0],
            [0.5, 0.5, 0],
            [0.5, 0, 0.5],
            [0, 0.5, 0.5],
            [0.25, 0.25, 0.25],
            [0.75, 0.75, 0.25],
            [0.75, 0.25, 0.75],
            [0.25, 0.75, 0.75]
        ])
        
        # Generate lattice
        self.atoms = self._generate_lattice()
        self.original_positions = self.atoms.copy()
        self.lattice_constant = 5.43  # Angstrom for Silicon
    
    def _generate_lattice(self):
        """Create a 3D silicon lattice"""
        atoms = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    for vec in self.base_vectors:
                        pos = np.array([x, y, z]) + vec
                        atoms.append(pos)
        return np.array(atoms)
    
    def inscribe_binary(self, binary_string, amplitude=0.0003):
        """Displace atoms based on binary pattern"""
        for i, bit in enumerate(binary_string):
            if i >= len(self.atoms):
                break
            
            if bit == '1':
                # Displace atom along X-axis (the "writing" axis)
                self.atoms[i, 0] += amplitude
        
        return self.atoms
    
    def render_ascii_2d(self, axis_pair=(0, 1), scale=50):
        """Simple ASCII visualization of 2D projection"""
        if axis_pair == (0, 1):
            x, y = self.atoms[:, 0], self.atoms[:, 1]
            label = "XY Plane"
        elif axis_pair == (0, 2):
            x, y = self.atoms[:, 0], self.atoms[:, 2]
            label = "XZ Plane"
        else:
            x, y = self.atoms[:, 1], self.atoms[:, 2]
            label = "YZ Plane"
        
        # Normalize to screen
        x_norm = ((x - np.min(x)) / (np.max(x) - np.min(x) + 0.1) * (scale - 1)).astype(int)
        y_norm = ((y - np.min(y)) / (np.max(y) - np.min(y) + 0.1) * (scale // 2 - 1)).astype(int)
        
        # Create grid
        grid = [[' ' for _ in range(scale)] for _ in range(scale // 2)]
        for xi, yi in zip(x_norm, y_norm):
            if 0 <= xi < scale and 0 <= yi < scale // 2:
                grid[yi][xi] = '●'
        
        print(f"\n{label} Projection:")
        for row in grid:
            print("".join(row))
    
    def get_statistics(self):
        """Return geometric statistics"""
        displacements = np.linalg.norm(self.atoms - self.original_positions, axis=1)
        return {
            'num_atoms': len(self.atoms),
            'max_displacement': np.max(displacements),
            'mean_displacement': np.mean(displacements),
            'center_of_mass': np.mean(self.atoms, axis=0)
        }


# --- DEMONSTRATION ---
if __name__ == "__main__":
    print("\n" + "#"*70)
    print("# WAKA-OS LAYER 2: GEOMETRIC SCULPTURE")
    print("#"*70)
    
    # Create lattice
    layer2 = Layer2_Geometric(lattice_size=(8, 8, 8))
    stats = layer2.get_statistics()
    
    print(f"\n[LATTICE] Silicon Crystal Structure")
    print(f"  Atoms:     {stats['num_atoms']}")
    print(f"  Size:      8×8×8 unit cells")
    print(f"  Constant:  {layer2.lattice_constant} Å")
    
    # Inscribe binary
    print(f"\n[INSCRIPTION] Binary Pattern → Atomic Displacements")
    binary = "11001010" * 10  # Example pattern
    layer2.inscribe_binary(binary, amplitude=0.001)
    
    stats = layer2.get_statistics()
    print(f"  Pattern:   {binary[:16]}... (len={len(binary)})")
    print(f"  Max Displacement: {stats['max_displacement']:.6f} Å")
    print(f"  Mean Displacement: {stats['mean_displacement']:.6f} Å")
    print(f"  Center of Mass: {stats['center_of_mass']}")
    
    # Visualize
    print(f"\n[VISUALIZATION] ASCII Projection")
    layer2.render_ascii_2d(axis_pair=(0, 1))
    layer2.render_ascii_2d(axis_pair=(0, 2))
    
    print("\n" + "="*70)
    print(" ✅ Layer 2 complete. Binary is now sculpted geometry.")
    print(" Next: Layer 3 converts geometry to audio vibration.")
    print("="*70 + "\n")
