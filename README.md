# Optimized Drone Delivery System

## Overview
This project is a Python-based simulation tool for optimized drone delivery systems. It utilizes genetic algorithms (GA) to compute efficient delivery paths and enables visualization of the results. The system is designed for scalability and flexibility, making it ideal for research and real-world applications.

## Features
- **Optimized Delivery Paths**:
  - Uses genetic algorithms to determine the most efficient routes for drones.
  - Incorporates constraints like weather conditions.

- **Graph Visualization**:
  - Displays delivery routes.
  - Color-coded weather conditions for better insight.

## Setup

### Prerequisites
- Python 3.8 or higher
- Required libraries:
  - `matplotlib`
  - `numpy`

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/ayeshakashif-ak/Optimizing-drone-delivery-routes.git
   ```
2. Navigate to the project directory:
   ```bash
   cd optimized-drone-delivery
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the System
The `main.py` script is the entry point for the system. It initializes the graph, runs the genetic algorithm for drone delivery optimization, and visualizes the results. To run it:
```bash
python main.py
```

### Visualizing Results
The visualization includes:
- Optimized delivery routes for drones.
- Color-coded weather conditions.
- 
### Adjusting Parameters
Modify the parameters in `main.py` to:
- Change the number of drones.
- Change the number of nodes.

## File Structure
- `main.py`: Entry point of the system.
- `graph.py`: Manages graph creation and visualization.
- `drone.py`: Defines drone behavior and path simulation.
- `genetic_algorithm.py`: Implements the genetic algorithm for path optimization.

## Examples
1. **Optimized Delivery**:
   - Efficient paths calculated using GA.

2. **Customizable Parameters**:
   - Adjust GA settings to explore different optimization strategies.
   - Define custom delivery locations and traffic conditions.

## Future Improvements (To-Do)
- Add support for dynamic obstacles in routes.
- Enhance visualization with 3D mapping.
- Introduce advanced optimization techniques for comparison.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

