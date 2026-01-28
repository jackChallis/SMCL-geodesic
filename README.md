# SMCL "Burst of Knowledge" Geodesic Sphere Model

A Python implementation of the San Mateo County Libraries (SMCL) logo geometry, officially referred to as the "Burst of Knowledge."

## About the Design

Geometrically, the logo represents a geodesic sphere (specifically, a subdivided icosahedron) composed of floating, disconnected triangles. The design symbolizes the spread of information and the convergence of shared ideas into a central hub.

## How It Works

The algorithm involves three main steps:

1. **Generate a base Icosahedron** - A 20-sided polyhedron using the golden ratio
2. **Subdivide into a Geodesic Sphere** - Each triangle is split into 4 smaller triangles, with vertices normalized to the sphere surface
3. **Shrink faces for the "floating" effect** - Each triangle is shrunk toward its center, creating gaps between faces

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the script to generate and display the 3D model:

```bash
python smcl_burst_of_knowledge.py
```

### Customization

You can modify the parameters in the script:

```python
# subdivisions: Higher = more/smaller triangles (2-3 recommended)
# shrink_factor: < 1.0 creates larger gaps between triangles
polys = create_burst_logo(subdivisions=2, shrink_factor=0.75)
```

### Using as a Module

```python
from smcl_burst_of_knowledge import create_burst_logo, visualize

# Generate geometry
polys = create_burst_logo(subdivisions=3, shrink_factor=0.8)

# Visualize with custom colors
visualize(polys, facecolor='#FF6B6B', edgecolor='#FF6B6B')
```

## Output

The script generates an interactive 3D matplotlib visualization and saves a PNG image (`burst_of_knowledge.png`).

## Manim Animations

This project includes Manim animations for creating videos of the geodesic sphere.

### 3D Rotating Animation

```bash
# Low quality preview (fast)
manim -pql geodesic_3d.py RotatingGeodesic

# High quality
manim -pqh geodesic_3d.py RotatingGeodesic

# 4K quality
manim -pqk geodesic_3d.py RotatingGeodesic
```

Available 3D scenes:
- `RotatingGeodesic` - Smooth camera rotation around the sphere
- `GeodesicBuildUp` - Triangles fade in with a staggered animation, then rotate

### 2D Logo-Style Animation

```bash
# Static logo view
manim -pql geodesic_2d.py LogoStyle

# Rotating 2D projection
manim -pql geodesic_2d.py LogoRotate2D

# Build-up animation with triangles flying in
manim -pql geodesic_2d.py LogoBuildUp
```

Available 2D scenes:
- `LogoStyle` - Static 2D projection resembling the SMCL logo
- `LogoRotate2D` - 2D projection with the sphere rotating
- `LogoBuildUp` - Triangles fly in from outside to form the logo

### Quality Flags

- `-pql` - Preview, low quality (480p, 15fps) - fast rendering
- `-pqm` - Preview, medium quality (720p, 30fps)
- `-pqh` - Preview, high quality (1080p, 60fps)
- `-pqk` - Preview, 4K quality (2160p, 60fps)

Output videos are saved to `media/videos/`.

## License

MIT License
