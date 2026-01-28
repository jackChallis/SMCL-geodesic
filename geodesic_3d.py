"""
3D Rotating Geodesic Sphere Animation (Manim)

Creates a rotating animation of the SMCL "Burst of Knowledge" geodesic sphere.

Usage:
    manim -pql geodesic_3d.py RotatingGeodesic      # Low quality preview
    manim -pqh geodesic_3d.py RotatingGeodesic      # High quality
    manim -pqk geodesic_3d.py RotatingGeodesic      # 4K quality
"""

from manim import *
import numpy as np


def normalize(v):
    """Normalize a vector or array of vectors to unit length."""
    norm = np.linalg.norm(v, axis=1, keepdims=True)
    return v / norm


def get_icosahedron():
    """Returns vertices and faces of a regular icosahedron."""
    t = (1.0 + np.sqrt(5.0)) / 2.0

    verts = np.array([
        [-1,  t,  0], [ 1,  t,  0], [-1, -t,  0], [ 1, -t,  0],
        [ 0, -1,  t], [ 0,  1,  t], [ 0, -1, -t], [ 0,  1, -t],
        [ t,  0, -1], [ t,  0,  1], [-t,  0, -1], [-t,  0,  1]
    ], dtype=float)

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
    midpoint_cache = {}

    def get_midpoint(i1, i2):
        key = tuple(sorted((i1, i2)))
        if key in midpoint_cache:
            return midpoint_cache[key]

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


def create_geodesic_triangles(subdivisions=2, shrink_factor=0.75, scale=2.5):
    """
    Creates a list of shrunk triangle vertex arrays for the geodesic sphere.
    """
    verts, faces = get_icosahedron()

    for _ in range(subdivisions):
        verts, faces = subdivide(verts, faces)

    triangles = []
    for face in faces:
        tri_verts = verts[face] * scale
        center = np.mean(tri_verts, axis=0)
        shrunk_verts = center + (tri_verts - center) * shrink_factor
        triangles.append(shrunk_verts)

    return triangles


class RotatingGeodesic(ThreeDScene):
    """3D rotating geodesic sphere animation."""

    def construct(self):
        # Set up the 3D camera
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        # Create the geodesic triangles
        triangles = create_geodesic_triangles(subdivisions=2, shrink_factor=0.75)

        # SMCL blue color
        smcl_blue = "#4169E1"

        # Create Manim polygon objects for each triangle
        triangle_mobjects = VGroup()

        for tri_verts in triangles:
            # Convert to 3D points
            points = [np.array([v[0], v[1], v[2]]) for v in tri_verts]

            # Create a filled polygon
            triangle = Polygon(
                *points,
                fill_color=smcl_blue,
                fill_opacity=0.9,
                stroke_color=smcl_blue,
                stroke_width=1,
            )
            triangle_mobjects.add(triangle)

        # Add all triangles to the scene
        self.add(triangle_mobjects)

        # Rotate the camera around the sphere
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(8)
        self.stop_ambient_camera_rotation()

        # Final pause
        self.wait(1)


class GeodesicBuildUp(ThreeDScene):
    """Animation showing the geodesic sphere being built up."""

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        triangles = create_geodesic_triangles(subdivisions=2, shrink_factor=0.75)
        smcl_blue = "#4169E1"

        # Create all triangle mobjects
        triangle_mobjects = VGroup()
        for tri_verts in triangles:
            points = [np.array([v[0], v[1], v[2]]) for v in tri_verts]
            triangle = Polygon(
                *points,
                fill_color=smcl_blue,
                fill_opacity=0.9,
                stroke_color=smcl_blue,
                stroke_width=1,
            )
            triangle_mobjects.add(triangle)

        # Animate triangles appearing
        self.play(
            LaggedStart(
                *[FadeIn(t, scale=0.5) for t in triangle_mobjects],
                lag_ratio=0.01,
                run_time=3
            )
        )

        # Start rotating
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(5)
        self.stop_ambient_camera_rotation()

        self.wait(1)
