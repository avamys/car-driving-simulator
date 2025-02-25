# Racing Simulator

A 3D car racing physics simulator built with Python, PyGame, and OpenGL. Experience realistic car physics in a procedurally generated world with dynamic terrain and vegetation.

## Features

### Vehicle Physics
- Realistic engine simulation with:
  - Dynamic power curves and gear ratios
  - Clutch simulation and transmission effects
  - RPM-based performance characteristics
  - Realistic acceleration and deceleration

### Driving Dynamics
- Advanced handling system including:
  - Speed-sensitive steering
  - Terrain-aware suspension
  - Drift mechanics with handbrake control
  - Realistic slope effects and gravity
  - Momentum and weight transfer simulation

### Environment
- Procedurally generated terrain with multiple biomes
- Dynamic vegetation system with various tree types
- Real-time terrain deformation and interaction
- Collision detection with environmental objects
- Realistic road network with different surface types

### Graphics
- Full 3D rendering with OpenGL
- Dynamic camera system with smooth following
- Real-time lighting and shadows
- Vehicle model with animated wheels
- Environmental effects and skybox

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Required Packages
```bash
pip install pygame
pip install PyOpenGL
pip install PyOpenGL_accelerate
pip install numpy
```

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/car-sim.git
cd car-sim
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Simulator

Launch the simulator by running:
```bash
python main.py
```

## Controls

- **Arrow Keys**: Control the car
  - Up: Accelerate
  - Down: Brake/Reverse
  - Left/Right: Steering

- **Gear Control**:
  - A: Shift Down
  - D: Shift Up

- **Special Controls**:
  - Space: Handbrake
  - ESC: Exit game

## Tips for Better Experience

1. Start in first gear and gradually build up speed
2. Use handbrake for drifting at higher speeds
3. Be mindful of terrain - steep slopes will affect vehicle performance
4. Watch your RPM gauge for optimal shift points
5. Avoid hitting trees - collision physics are realistic!

## Known Issues

- High-speed collisions might cause unexpected behavior
- Terrain generation can be slow on first load
- Some graphics cards might need updated OpenGL drivers

## Contributing

Feel free to contribute to this project! Whether it's bug fixes, new features, or improvements to the physics system, all contributions are welcome.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## Credits

This project was developed with the assistance of:
- Cursor IDE - The world's best IDE
- Claude AI - Advanced AI pair programming assistant

Special thanks to the open-source community and the contributors of PyGame and PyOpenGL.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Plans

- [ ] Add multiplayer support
- [ ] Implement weather effects
- [ ] Add more vehicle types
- [ ] Enhance graphics with modern OpenGL features
- [ ] Add race track editor
