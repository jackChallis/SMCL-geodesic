"""
SMCL 'Burst of Knowledge' Geodesic Sphere Model

This script generates a 3D model of the San Mateo County Libraries (SMCL) logo,
officially referred to as the "Burst of Knowledge."

Geometrically, it represents a geodesic sphere (specifically, a subdivided
icosahedron) composed of floating, disconnected triangles. The design symbolizes
the spread of information and the convergence of shared ideas into a central hub.

Algorithm:
1. Generate a base Icosahedron (a 20-sided polyhedron)
2. Subdivide it into smaller triangles to form a Geodesic Sphere
3. Shrink the faces individually to create the "floating" gap effect
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def normalize(v):
    """Normalize a vector or array of vectors to unit length."""
    norm = np.linalg.norm(v, axis=1, keepdims=True)
    return v / norm


def get_icosahedron():
    """Returns vertices and faces of a regular icosahedron."""
    t = (1.0 + np.sqrt(5.0)) / 2.0

    # Vertices
    verts = np.array([
        [-1,  t,  0], [ 1,  t,  0], [-1, -t,  0], [ 1, -t,  0],
        [ 0, -1,  t], [ 0,  1,  t], [ 0, -1, -t], [ 0,  1, -t],
        [ t,  0, -1], [ t,  0,  1], [-t,  0, -1], [-t,  0,  1]
    ])

    # Faces (indices of vertices)
    faces = np.array([
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ])

    return normalize(verts), faces


def subdivide(verts, faces):
    """Subdivides each triangle into 4 smaller triangles."""
    new_faces = []
    new_verts = verts.tolist()

    # Cache middle points to avoid duplicates
    midpoint_cache = {}

    def get_midpoint(i1, i2):
        # Sort indices to ensure consistency
        key = tuple(sorted((i1, i2)))
        if key in midpoint_cache:
            return midpoint_cache[key]

        # Calculate midpoint and normalize to push it to sphere surface
        v1, v2 = verts[i1], verts[i2]
        mid = (v1 + v2) / 2.0
        mid = mid / np.linalg.norm(mid)

        new_verts.append(mid)
        idx = len(new_verts) - 1
        midpoint_cache[key] = idx
        return idx

    for f in faces:
        v1, v2, v3 = f
        a = get_midpoint(v1, v2)
        b = get_midpoint(v2, v3)
        c = get_midpoint(v3, v1)

        new_faces.extend([
            [v1, a, c],
            [v2, b, a],
            [v3, c, b],
            [a, b, c]
        ])

    return np.array(new_verts), np.array(new_faces)


def create_burst_logo(subdivisions=2, shrink_factor=0.85):
    """
    Generates the geometry for the SMCL logo.

    Args:
        subdivisions: Higher number = more/smaller triangles (logo looks like freq 2 or 3)
        shrink_factor: < 1.0 creates gaps between triangles

    Returns:
        List of polygon vertices representing the shrunk triangles
    """
    # 1. Start with Icosahedron
    verts, faces = get_icosahedron()

    # 2. Subdivide to make it a sphere
    for _ in range(subdivisions):
        verts, faces = subdivide(verts, faces)

    # 3. Create independent triangles and shrink them
    final_polys = []

    for face in faces:
        # Get vertices for this face
        tri_verts = verts[face]

        # Calculate center of the triangle
        center = np.mean(tri_verts, axis=0)

        # Shrink vertices towards center
        # New_V = Center + (V - Center) * factor
        shrunk_verts = center + (tri_verts - center) * shrink_factor
        final_polys.append(shrunk_verts)

    return final_polys


def visualize(polys, title="SMCL 'Burst of Knowledge' Model",
              facecolor='#4169E1', edgecolor='#4169E1', alpha=0.9,
              save_path=None):
    """
    Visualize the geodesic sphere model.

    Args:
        polys: List of polygon vertices
        title: Plot title
        facecolor: Color for triangle faces
        edgecolor: Color for triangle edges
        alpha: Transparency (0-1)
        save_path: If provided, save the figure to this path
    """
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create the collection of triangles
    mesh = Poly3DCollection(polys, facecolors=facecolor,
                            edgecolors=edgecolor, alpha=alpha)
    ax.add_collection3d(mesh)

    # Set plot limits
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)

    # Turn off grid and axis for a cleaner logo look
    ax.axis('off')

    plt.title(title)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print(f"Figure saved to: {save_path}")

    plt.show()


if __name__ == "__main__":
    # Generate the model
    polys = create_burst_logo(subdivisions=2, shrink_factor=0.75)

    # Visualize it
    visualize(polys, save_path="burst_of_knowledge.png")
