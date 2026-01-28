"""
2D Logo-Style Geodesic Animation (Manim)

Creates a 2D projection of the SMCL "Burst of Knowledge" that resembles the logo.

Usage:
    manim -pql geodesic_2d.py LogoStyle           # Low quality preview
    manim -pqh geodesic_2d.py LogoStyle           # High quality
    manim -pql geodesic_2d.py LogoRotate2D        # 2D rotation animation
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


def rotation_matrix(axis, theta):
    """Return the rotation matrix for rotation around axis by theta radians."""
    axis = axis / np.linalg.norm(axis)
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    return np.array([
        [a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
        [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
        [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]
    ])


def create_geodesic_triangles_3d(subdivisions=2, shrink_factor=0.75, scale=2.5):
    """Creates 3D triangle vertices for the geodesic sphere."""
    verts, faces = get_icosahedron()

    for _ in range(subdivisions):
        verts, faces = subdivide(verts, faces)

    triangles = []
    for face in faces:
        tri_verts = verts[face] * scale
        center = np.mean(tri_verts, axis=0)
        shrunk_verts = center + (tri_verts - center) * shrink_factor
        triangles.append(shrunk_verts)

    return triangles, verts * scale, faces


def project_to_2d(triangles_3d, view_angle_x=0.3, view_angle_y=0.2):
    """
    Project 3D triangles to 2D using orthographic projection.
    Rotates the sphere first to get a good viewing angle.
    """
    # Apply rotation to get a good view angle
    rot_x = rotation_matrix(np.array([1, 0, 0]), view_angle_x)
    rot_y = rotation_matrix(np.array([0, 1, 0]), view_angle_y)
    rot = rot_y @ rot_x

    triangles_2d = []
    z_depths = []

    for tri in triangles_3d:
        # Rotate the triangle
        rotated = (rot @ tri.T).T
        # Project to 2D (just drop z, orthographic projection)
        tri_2d = rotated[:, :2]
        triangles_2d.append(tri_2d)
        # Store average z depth for sorting
        z_depths.append(np.mean(rotated[:, 2]))

    return triangles_2d, z_depths


class LogoStyle(Scene):
    """Static 2D logo-style view of the geodesic sphere."""

    def construct(self):
        # Create 3D triangles
        triangles_3d, _, _ = create_geodesic_triangles_3d(
            subdivisions=2, shrink_factor=0.75, scale=2.5
        )

        # Project to 2D with a nice viewing angle
        triangles_2d, z_depths = project_to_2d(
            triangles_3d, view_angle_x=0.4, view_angle_y=0.3
        )

        # Sort by depth (back to front)
        sorted_indices = np.argsort(z_depths)

        smcl_blue = "#4169E1"

        # Create all triangles
        triangle_group = VGroup()

        for idx in sorted_indices:
            tri_2d = triangles_2d[idx]
            z = z_depths[idx]

            # Vary opacity based on depth for 3D effect
            opacity = 0.6 + 0.4 * (z + 2.5) / 5.0
            opacity = np.clip(opacity, 0.4, 1.0)

            points = [np.array([v[0], v[1], 0]) for v in tri_2d]

            triangle = Polygon(
                *points,
                fill_color=smcl_blue,
                fill_opacity=opacity,
                stroke_color=smcl_blue,
                stroke_width=0.5,
            )
            triangle_group.add(triangle)

        # Animate the logo appearing
        self.play(
            LaggedStart(
                *[FadeIn(t, scale=0.8) for t in triangle_group],
                lag_ratio=0.005,
                run_time=2
            )
        )

        self.wait(2)


class LogoRotate2D(Scene):
    """2D animation showing the geodesic sphere rotating (projected)."""

    def construct(self):
        smcl_blue = "#4169E1"

        # Create 3D triangles
        triangles_3d, _, _ = create_geodesic_triangles_3d(
            subdivisions=2, shrink_factor=0.75, scale=2.5
        )

        def create_frame(angle_y):
            """Create a frame of the rotating sphere at a given angle."""
            rot_x = rotation_matrix(np.array([1, 0, 0]), 0.4)
            rot_y = rotation_matrix(np.array([0, 1, 0]), angle_y)
            rot = rot_y @ rot_x

            triangles_2d = []
            z_depths = []

            for tri in triangles_3d:
                rotated = (rot @ tri.T).T
                tri_2d = rotated[:, :2]
                triangles_2d.append(tri_2d)
                z_depths.append(np.mean(rotated[:, 2]))

            sorted_indices = np.argsort(z_depths)

            triangle_group = VGroup()

            for idx in sorted_indices:
                tri_2d = triangles_2d[idx]
                z = z_depths[idx]
                opacity = 0.6 + 0.4 * (z + 2.5) / 5.0
                opacity = np.clip(opacity, 0.4, 1.0)

                points = [np.array([v[0], v[1], 0]) for v in tri_2d]

                triangle = Polygon(
                    *points,
                    fill_color=smcl_blue,
                    fill_opacity=opacity,
                    stroke_color=smcl_blue,
                    stroke_width=0.5,
                )
                triangle_group.add(triangle)

            return triangle_group

        # Create initial frame
        current_frame = create_frame(0)
        self.add(current_frame)

        # Animate rotation
        num_steps = 120
        for i in range(1, num_steps + 1):
            angle = 2 * PI * i / num_steps
            new_frame = create_frame(angle)

            self.remove(current_frame)
            self.add(new_frame)
            current_frame = new_frame

            self.wait(1/30)

        self.wait(1)


class LogoBuildUp(Scene):
    """Animated build-up of the 2D logo with triangles flying in."""

    def construct(self):
        triangles_3d, _, _ = create_geodesic_triangles_3d(
            subdivisions=2, shrink_factor=0.75, scale=2.5
        )

        triangles_2d, z_depths = project_to_2d(
            triangles_3d, view_angle_x=0.4, view_angle_y=0.3
        )

        sorted_indices = np.argsort(z_depths)
        smcl_blue = "#4169E1"

        # Create triangles starting from random positions outside
        triangles_start = VGroup()
        triangles_end = VGroup()

        for idx in sorted_indices:
            tri_2d = triangles_2d[idx]
            z = z_depths[idx]
            opacity = 0.6 + 0.4 * (z + 2.5) / 5.0
            opacity = np.clip(opacity, 0.4, 1.0)

            points = [np.array([v[0], v[1], 0]) for v in tri_2d]

            # Final position
            triangle_end = Polygon(
                *points,
                fill_color=smcl_blue,
                fill_opacity=opacity,
                stroke_color=smcl_blue,
                stroke_width=0.5,
            )

            # Starting position - fly in from outside
            triangle_start = triangle_end.copy()
            direction = np.array([np.mean(tri_2d[:, 0]), np.mean(tri_2d[:, 1]), 0])
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
            triangle_start.shift(direction * 8)
            triangle_start.set_opacity(0)

            triangles_start.add(triangle_start)
            triangles_end.add(triangle_end)

        self.add(triangles_start)

        # Animate triangles flying into position
        self.play(
            *[
                AnimationGroup(
                    t_start.animate.move_to(t_end.get_center()),
                    t_start.animate.set_opacity(t_end.get_fill_opacity()),
                )
                for t_start, t_end in zip(triangles_start, triangles_end)
            ],
            run_time=3,
            lag_ratio=0.01
        )

        self.wait(2)
