# Car Physics Simulator

A 3D car physics simulator built with Python, PyGame, and OpenGL. Experience realistic car physics in a procedurally generated world with dynamic terrain, vegetation, and road networks.

## Project Structure

```
car-sim/
├── main.py          # Main game loop and initialization
├── car.py           # Vehicle physics and rendering
├── camera.py        # Third-person camera system
├── world.py         # World management and chunk loading
├── terrain.py       # Terrain generation and rendering
├── vegetation.py    # Tree system and vegetation
├── road.py          # Road network generation
└── skybox.py        # Sky rendering and effects
```

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
- Python 3.10 or higher
- pip (Python package installer)

```bash
# Clone the repository
git clone https://github.com/avamys/car-driving-simulator.git
cd car-driving-simulator

# Install the package in editable mode
pip install -e .
```

The package will automatically install all required dependencies:
- pygame
- PyOpenGL
- numpy

## Running the Simulator

After installation, you can run the simulator in two ways:

1. Using the installed command:
```bash
car-sim
```

2. Running the module directly:
```bash
python -m car_sim
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

- [ ] Implement weather effects
- [ ] Add more vehicle types
- [ ] Enhance graphics with modern OpenGL features
