import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for performance
import matplotlib.pyplot as plt
from scipy.integrate import simpson


class MobiusStrip:
    def __init__(self, R, w, n):
        """
        Initialize the Möbius strip parameters.
        Mesh generation is deferred to save memory if unused.
        """
        self.R = R
        self.w = w
        self.n = n
        self.u = np.linspace(0, 2 * np.pi, n)
        self.v = np.linspace(-w / 2, w / 2, n)
        self.U, self.V = np.meshgrid(self.u, self.v)
        self._X = self._Y = self._Z = None  # Lazy-loaded mesh

    def compute_mesh(self):
        """
        Compute the (x, y, z) coordinates of the Möbius strip.
        """
        U, V, R = self.U, self.V, self.R
        X = (R + V * np.cos(U / 2)) * np.cos(U)
        Y = (R + V * np.cos(U / 2)) * np.sin(U)
        Z = V * np.sin(U / 2)
        return X, Y, Z

    @property
    def X(self):
        if self._X is None:
            self._X, self._Y, self._Z = self.compute_mesh()
        return self._X

    @property
    def Y(self):
        if self._Y is None:
            self._X, self._Y, self._Z = self.compute_mesh()
        return self._Y

    @property
    def Z(self):
        if self._Z is None:
            self._X, self._Y, self._Z = self.compute_mesh()
        return self._Z

    def compute_surface_area(self):
        """
        Approximate the surface area using the parametric surface formula.
        """
        du = self.u[1] - self.u[0]
        dv = self.v[1] - self.v[0]

        Xu, Xv = np.gradient(self.X, du, dv, axis=(1, 0))
        Yu, Yv = np.gradient(self.Y, du, dv, axis=(1, 0))
        Zu, Zv = np.gradient(self.Z, du, dv, axis=(1, 0))

        cross_prod = np.cross(
            np.stack([Xu, Yu, Zu], axis=-1),
            np.stack([Xv, Yv, Zv], axis=-1)
        )
        area_density = np.linalg.norm(cross_prod, axis=2)
        area = simpson(simpson(area_density, self.v), self.u)

        # Explicit memory cleanup
        del Xu, Xv, Yu, Yv, Zu, Zv, cross_prod, area_density
        import gc
        gc.collect()

        return area

    def compute_edge_length(self):
        """
        Approximate the length of the Möbius strip edge.
        """
        edge_u = np.linspace(0, 2 * np.pi, self.n)
        edge_v = np.full_like(edge_u, self.w / 2)

        x = (self.R + edge_v * np.cos(edge_u / 2)) * np.cos(edge_u)
        y = (self.R + edge_v * np.cos(edge_u / 2)) * np.sin(edge_u)
        z = edge_v * np.sin(edge_u / 2)

        dx = np.diff(x)
        dy = np.diff(y)
        dz = np.diff(z)

        segment_lengths = np.sqrt(dx**2 + dy**2 + dz**2)
        total_length = np.sum(segment_lengths)

        # Explicit memory cleanup
        del x, y, z, dx, dy, dz, segment_lengths
        import gc
        gc.collect()

        return total_length

    def analyze(self):
        """
        Compute surface area and edge length, and return them with the matplotlib Figure.
        """
        area = self.compute_surface_area()
        edge_length = self.compute_edge_length()

        fig = plt.figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(self.X, self.Y, self.Z, rstride=1, cstride=1,
                        color='c', edgecolor='k', alpha=0.8)
        ax.set_title("Möbius Strip")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.tight_layout()

        return [area, edge_length], fig

    def clear(self):
        """
        Clear cached mesh arrays to release memory.
        """
        self._X = self._Y = self._Z = None
        import gc
        gc.collect()

