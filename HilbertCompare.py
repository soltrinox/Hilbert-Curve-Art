
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from datetime import datetime
import math
import cmath

# --- Hilbert Curve Generation Logic ---
def hilbert_curve(order):
    points = []
    n = 2**order
    for i in range(n * n):
        points.append(hilbert_index_to_xy(i, n))
    return points

def hilbert_index_to_xy(index, n):
    x, y = 0, 0
    s = 1
    while s < n:
        rx = 1 & (index >> 1)
        ry = 1 & (index ^ rx)
        x, y = rotate(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        index >>= 2
        s <<= 1
    return x, y

def rotate(n, x, y, rx, ry):
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        x, y = y, x
    return x, y

def normalize_points(points, n):
    if n == 1:
        return [(0.0, 0.0)]
    return [((2 * p[0] / (n - 1)) - 1, (2 * p[1] / (n - 1)) - 1) for p in points]

# --- Mapping Transformations ---

def transform_superellipse(points):
    """Superellipse (Lamé) Mapping."""
    transformed_points = []
    for x, y in points:
        if x == 0 and y == 0:
            transformed_points.append((0, 0))
            continue
        m = max(abs(x), abs(y))
        if m == 0: transformed_points.append((0,0)); continue
        x_b, y_b = x / m, y / m
        c = (1**4 / (x_b**4 + y_b**4))**0.25
        transformed_points.append((c * x, c * y))
    return transformed_points

def transform_shirley_chiu(points):
    """Shirley–Chiu Concentric Mapping."""
    transformed_points = []
    for x, y in points:
        a, b = 2 * x, 2 * y
        if a == 0 and b == 0: transformed_points.append((0,0)); continue
        if a > -b:
            if a > b: r_map, phi = a, (math.pi / 4) * (b / a) if a != 0 else 0
            else: r_map, phi = b, (math.pi / 4) * (2 - (a / b)) if b != 0 else 0
        else:
            if a < b: r_map, phi = -a, (math.pi / 4) * (4 + (b / a)) if a != 0 else 0
            else: r_map, phi = -b, (math.pi / 4) * (6 - (a / b)) if b != 0 else 0
        u, v = 0.5 * r_map * math.cos(phi), 0.5 * r_map * math.sin(phi)
        transformed_points.append((u, v))
    return transformed_points

def transform_simple_radial(points):
    """Simple Radial Mapping."""
    transformed_points = []
    for x, y in points:
        if x == 0 and y == 0: transformed_points.append((0, 0)); continue
        m = max(abs(x), abs(y))
        if m == 0: transformed_points.append((0,0)); continue
        transformed_points.append((x/m, y/m))
    return transformed_points

def transform_naive_polar(points):
    """Radial (Naïve Polar) Mapping."""
    transformed_points = []
    for x, y in points:
        if x == 0 and y == 0: transformed_points.append((0, 0)); continue
        r, theta = math.sqrt(x**2 + y**2), math.atan2(y, x)
        transformed_points.append((r * math.cos(theta), r * math.sin(theta)))
    return transformed_points

def transform_fernandez_guasti(points):
    """Fernandez-Guasti (FG) Squircular Mapping."""
    transformed_points = []
    s = 1.0 # squareness
    for x, y in points:
        u = x * math.sqrt(1 - (s**2 / 2) * y**2)
        v = y * math.sqrt(1 - (s**2 / 2) * x**2)
        transformed_points.append((u,v))
    return transformed_points

def transform_equal_area_approx(points):
    """Equal-Area (Area-Preserving) Mapping."""
    transformed_points = []
    for x, y in points:
        r = math.sqrt(x**2 + y**2)
        theta = math.atan2(y, x)
        r_new = math.sqrt(r)
        transformed_points.append((r_new * math.cos(theta), r_new * math.sin(theta)))
    return transformed_points

def transform_polynomial(points):
    """Polynomial / Optimized Mapping."""
    transformed_points = []
    for x, y in points:
        z = complex(x, y)
        # Approximation of Schwarz-Christoffel
        z_new = z + 0.0731647 * (z**5) + 0.00358709 * (z**9)
        transformed_points.append((z_new.real, z_new.imag))
    return transformed_points

MAPPINGS = {
    "Superellipse (Lamé)": transform_superellipse,
    "Shirley-Chiu": transform_shirley_chiu,
    "FG-Squircular": transform_fernandez_guasti,
    "Simple Radial": transform_simple_radial,
    "Naïve Polar": transform_naive_polar,
    "Equal-Area Approx": transform_equal_area_approx,
    "Polynomial (Conformal)": transform_polynomial,
}

class HilbertApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hilbert Curve Mapping Comparator")
        self.order = tk.IntVar(value=4)
        self.mapping1 = tk.StringVar(value=list(MAPPINGS.keys())[0])
        self.mapping2 = tk.StringVar(value=list(MAPPINGS.keys())[1])

        self.fig, self.axs = plt.subplots(1, 3, figsize=(18, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        controls_frame = ttk.Frame(self.root, padding="10")
        controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ttk.Label(controls_frame, text="Order:").pack(side=tk.LEFT)
        ttk.Scale(controls_frame, from_=1, to=8, orient=tk.HORIZONTAL, variable=self.order, command=self.on_param_change).pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.order_label = ttk.Label(controls_frame, text=f'{self.order.get()}')
        self.order_label.pack(side=tk.LEFT, padx=5)

        ttk.Label(controls_frame, text="Middle:").pack(side=tk.LEFT)
        combo1 = ttk.Combobox(controls_frame, textvariable=self.mapping1, values=list(MAPPINGS.keys()))
        combo1.pack(side=tk.LEFT, padx=5)
        combo1.bind("<<ComboboxSelected>>", self.on_param_change)

        ttk.Label(controls_frame, text="Right:").pack(side=tk.LEFT)
        combo2 = ttk.Combobox(controls_frame, textvariable=self.mapping2, values=list(MAPPINGS.keys()))
        combo2.pack(side=tk.LEFT, padx=5)
        combo2.bind("<<ComboboxSelected>>", self.on_param_change)

        ttk.Button(controls_frame, text="Save Displayed SVGs", command=self.save_displayed_svgs).pack(side=tk.RIGHT, padx=10)

        self.update_plot()

    def on_param_change(self, event=None):
        self.order.set(round(self.order.get()))
        self.order_label.config(text=f'{self.order.get()}')
        self.update_plot()

    def update_plot(self):
        order = self.order.get()
        hilbert_points = hilbert_curve(order)
        normalized_points = normalize_points(hilbert_points, 2**order)

        # Static left plot (original)
        self.axs[0].clear()
        self.axs[0].plot([p[0] for p in normalized_points], [p[1] for p in normalized_points], 'b-')
        self.axs[0].set_title(f'Original Hilbert Curve (Order {order})')
        self.axs[0].axis('equal'); self.axs[0].grid(True)

        # Middle plot
        map_func1 = MAPPINGS[self.mapping1.get()]
        points1 = map_func1(normalized_points)
        self.axs[1].clear()
        self.axs[1].plot([p[0] for p in points1], [p[1] for p in points1], 'b-')
        self.axs[1].set_title(f'{self.mapping1.get()} (Order {order})')
        self.axs[1].axis('equal'); self.axs[1].grid(True)

        # Right plot
        map_func2 = MAPPINGS[self.mapping2.get()]
        points2 = map_func2(normalized_points)
        self.axs[2].clear()
        self.axs[2].plot([p[0] for p in points2], [p[1] for p in points2], 'b-')
        self.axs[2].set_title(f'{self.mapping2.get()} (Order {order})')
        self.axs[2].axis('equal'); self.axs[2].grid(True)

        self.fig.tight_layout()
        self.canvas.draw()

    def save_displayed_svgs(self):
        order = self.order.get()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_folder = os.path.join(os.getcwd(), timestamp)
        os.makedirs(output_folder, exist_ok=True)

        hilbert_points = hilbert_curve(order)
        normalized_points = normalize_points(hilbert_points, 2**order)

        # Save original
        self.save_single_svg(normalized_points, output_folder, f'original_order_{order}.svg')

        # Save middle plot
        map_func1 = MAPPINGS[self.mapping1.get()]
        points1 = map_func1(normalized_points)
        filename1 = f'{self.mapping1.get().lower().replace(" ", "_")}_order_{order}.svg'
        self.save_single_svg(points1, output_folder, filename1)

        # Save right plot
        map_func2 = MAPPINGS[self.mapping2.get()]
        points2 = map_func2(normalized_points)
        filename2 = f'{self.mapping2.get().lower().replace(" ", "_")}_order_{order}.svg'
        self.save_single_svg(points2, output_folder, filename2)

        feedback_label = ttk.Label(self.root, text=f"Saved 3 SVGs to {output_folder}", foreground="green")
        feedback_label.pack(side=tk.BOTTOM, fill=tk.X)
        self.root.after(4000, lambda: feedback_label.pack_forget())

    def save_single_svg(self, points, folder, filename):
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot([p[0] for p in points], [p[1] for p in points], 'b-')
        ax.axis('equal'); ax.axis('off')
        fig.savefig(os.path.join(folder, filename), format='svg', transparent=True, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

if __name__ == '__main__':
    root = tk.Tk()
    app = HilbertApp(root)
    root.mainloop()
