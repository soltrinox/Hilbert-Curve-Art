## HILBERT CURVE SQUIRCLE 

####  Plots and Mathematical Foundations

by **Rayyan Zahid** & F.D. Rosario

### Introduction

The Hilbert curve is one of the most influential constructions in discrete geometry and scientific computing: a space-filling curve that provides a continuous, surjective mapping from a one‑dimensional interval onto a two‑dimensional square. Introduced by David Hilbert in 1891, it refines the earlier Peano curve idea while adopting a particularly elegant, recursive structure. At finite order, the Hilbert curve is realized as a polyline through an \(n\times n\) grid (with \( n = 2^{\text{order}} \)) that visits each lattice cell exactly once. As order increases, the traversal refines by factors of two along each axis and, crucially, preserves spatial locality: indices that are neighbors in one dimension tend to map to nearby points in the plane. This property, far from being just aesthetic, explains why Hilbert orderings underpin cache‑aware layouts, spatial indexing, image storage, domain decomposition, and a variety of visualization techniques where coherence matters.

Mathematically, the limiting Hilbert map \( H : [0,1] \to [0,1]^2 \) is continuous and onto yet necessarily non‑injective; the path has fractal character with Hausdorff dimension 2 despite being traced by a one‑dimensional parameter. In computational practice, we operate on discrete approximations: a Hilbert index \( d \in \{0,\dots,n^2-1\} \) is decoded into integer coordinates \((x,y)\in\{0,\dots,n-1\}^2\) by peeling off two bits per scale step and applying a rotate–reflect–swap within a sub‑square of side \(s\) that doubles each iteration. This bitwise algorithm is simple, exact over integers, and runs in \(O(\log n)\) per index. Once lattice coordinates are produced, an affine normalization maps them to the canonical square \([-1,1]^2\), yielding an order‑invariant coordinate system that centers and symmetrizes the geometry. These two steps, bitwise decoding and normalization, form the backbone of the simulator in this repository.

What makes this simulator distinctive is that it does not stop at drawing the classical, axis‑aligned Hilbert curve. Instead, it treats the normalized coordinates as input to a family of planar mappings that transform the curve into new geometries. The included mappings span complementary design goals:
- a Lamé (superellipse) boundary with exponent \(p=4\), which softens corners while preserving axial straightness;
- the Shirley–Chiu concentric square‑to‑disk map, renowned in rendering for its continuity and relatively low distortion while sending square edges to the circle;
- the Fernandez–Guasti (FG) squircular map, an analytic rounding of the square governed by a “squareness” parameter \(s\) (fixed to 1 here);
- a simple L∞ radial projection that normalizes by \( m = \max(|x|,|y|) \), illustrating how choice of norm determines “radial” behavior and accentuates corners;
- a naïve polar identity (convert to \((r,\theta)\) and back) that serves as a baseline for radial reasoning;
- an equal‑area‑inspired radial warp \( r' = \sqrt{r} \), demonstrating how monotone radial changes redistribute density; and
- a complex polynomial warp \( z' = z + a z^5 + b z^9 \) that smoothly rounds corners while approximately preserving symmetries along axes, echoing the qualitative feel of truncated Schwarz–Christoffel mappings without their integral machinery.

The implications are both conceptual and practical. Conceptually, the simulator provides a living laboratory for space‑filling curves: by sliding the order parameter, one observes self‑similar refinement, orientation flips, and the way a local rotate‑before‑translate rule yields global structure. This bridges bit‑level reasoning (extracting \(rx, ry\) flags, conditioning on \(ry\), reflecting about \(s-1\)) with emergent geometric features (turn distributions, clusters of short segments, and coherent sweeps). The Hilbert curve’s famed locality becomes visible rather than abstract: contrast it with raster or Morton (Z‑order) traversals and the advantage for cache behavior and neighborhood queries is immediate.

Practically, the mapping suite turns the simulator into a platform for distortion analysis and design. Each mapping highlights trade‑offs among area preservation, boundary correspondence, angular fidelity, and smoothness. The Shirley–Chiu map excels when one needs a smooth, continuous, edge‑to‑circle correspondence with moderate distortion, useful for disc‑based plots or importance sampling over circular domains. FG squircles offer analytic simplicity and an interpretable parameter \(s\) to dial between “square‑ish” and “circle‑ish” shapes. The Lamé superellipse with \(p=4\) emphasizes algebraic control over corner softness. L∞ projection teaches how norm choices alter the notion of “radial stretching,” sending almost everything to the square’s boundary and exaggerating corner influence. The equal‑area‑inspired warp shows how a purely radial change can equalize densities in disk‑like settings (while only approximately so on the square). The polynomial warp provides a compact, differentiable deformation that rounds corners without the overhead of full conformal mapping.

These transformations are not merely for visual effect; they affect how the Hilbert‑ordered samples behave as a sampling pattern in new domains. For instance, when transforming Hilbert samples into a disk for radial heatmaps, the choice between Shirley–Chiu and a radial \(\sqrt{r}\) warp determines whether density or angular shape gets priority. In scientific visualization, rounding corners may help emphasize central structures; in generative art, the interplay of a coherent Hilbert backbone with different boundary shapes yields distinct textures and aesthetics. Because the simulator plots polylines with equal axis scaling and provides clean SVG export, the output is suitable for both analytical inspection (grid on, axes visible) and publication‑grade artwork (transparent background, axes off).

The simulator also exposes the numerical realities that govern robust implementations. Singular configurations must be guarded: at the origin, \(m=0\) in L∞ scaling; in Shirley–Chiu branches, denominators \(a\) or \(b\) can vanish; in polar conversions, \(\operatorname{atan2}(0,0)\) must be avoided. The code addresses these with explicit early returns and branch conditions that guarantee nonzero denominators. Normalization to \([-1,1]^2\) removes order‑dependence from constants and makes parameters comparable across experiments. Performance scales predictably: generating \(n^2\) points dominates; each mapping is \(O(1)\) per point and amenable to vectorization. For interactive use, one can preview at lower orders or with cheaper mappings, then export high‑order SVGs once satisfied.

Finally, the design invites extension. One can add true conformal (or quasi‑conformal) square‑to‑disk maps, expose the FG parameter \(s\) for continuous interpolation, explore other Lamé exponents \(p\), or supplement visual comparisons with quantitative diagnostics like local area ratio, angular distortion, and metric stretch. Inverse mappings could enable round‑trip workflows between square and disk. Swapping the traversal itself, to Morton, Peano, or custom curves, would reveal how traversal choice interacts with mapping distortion to shape both appearance and neighborhood coherence. In short, the repository is more than a viewer: it is a compact, reproducible environment where discrete geometry, mapping theory, numerical care, and design practice meet.

### 1) Notation and Global Parameters

- **order**: An integer \(k \ge 1\) specifying the Hilbert curve order.
- **n**: The grid side-length \( n = 2^{\text{order}} = 2^{k} \). Grid points have integer coordinates in \(\{0, 1, \dots, n-1\}\).
- **d**: The Hilbert index (also called the distance or traversal index) \( d \in \{0, 1, \dots, n^2 - 1\} \). Each \(d\) uniquely maps to a grid point \((x, y)\).
- **(x, y)**: Integer grid coordinates before normalization; \( x, y \in \{0, 1, \dots, n-1\} \).
- **(x', y')**: Normalized real-valued coordinates in the square \([-1, 1]^2\).
- **s**: A power-of-two scale that runs over \( 1, 2, 4, \dots, n \) in the Hilbert mapping algorithm.
- **rx, ry**: Orientation bits in \(\{0,1\}\) extracted from \(d\) at each scale step to drive the Hilbert rotation/reflect/swap operations.
- **m**: The L∞ radial scale factor \( m = \max(|x|, |y|) \) used by several mappings.
- **r,\; r'**: Euclidean radii before/after a radial transform.
- **\(\theta\)**: The polar angle \( \theta = \operatorname{atan2}(y, x) \in (-\pi, \pi] \).
- **z**: A complex-plane encoding \( z = x + i y \), sometimes used to write 2D warps as a complex polynomial.
- **s (squareness parameter in FG mapping)**: In this repository, the symbol \(s\) is reused in two contexts. In the Hilbert algorithm, \( s \) is a scale that doubles each step; in the Fernandez–Guasti mapping, \( s \in [0,1] \) is a shape parameter controlling the “squareness.” The code fixes the latter to \( s = 1 \). Context disambiguates which \( s \) is meant.


### 2) Hilbert Index-to-Coordinate Mapping: \( d \mapsto (x, y) \)

Both  and  implement the same classical algorithm for converting a Hilbert curve index \(d\) into integer grid coordinates \((x, y)\). Conceptually, \(d\) is processed two bits at a time, from least significant to most significant, while a scale \( s \) doubles each iteration. Orientation bits \( rx \) and \( ry \) determine how the partial square of side \( s \) is rotated and/or reflected before adding an \( s \)-sized step in either the \(x\) or \(y\) direction.

The algorithm updates a running pair \((x, y)\) starting from \((0, 0)\) via:

\[
\begin{aligned}
&\text{Initialize:}\quad x \leftarrow 0,\; y \leftarrow 0,\; s \leftarrow 1,\; d_0 \leftarrow d.\\
&\text{While } s < n:\\
&\qquad rx \leftarrow \big\lfloor d_0 / 2 \big\rfloor \bmod 2,\\
&\qquad ry \leftarrow (d_0 \oplus rx) \bmod 2,\\
&\qquad (x, y) \leftarrow \operatorname{rotate\_hilbert}(s, x, y, rx, ry),\\
&\qquad x \leftarrow x + s \cdot rx,\quad y \leftarrow y + s \cdot ry,\\
&\qquad d_0 \leftarrow \left\lfloor d_0 / 4 \right\rfloor,\quad s \leftarrow 2s.\\
\end{aligned}
\]

Here \(\oplus\) denotes bitwise XOR. The effect is to peel off the next 2-bit quadrant code from \(d_0\) each step, adjust orientation for that quadrant, and move the current point by \( s \) along \(x\) and/or \(y\). The update finishes with \( (x, y) \in \{0,\dots,n-1\}^2 \).

The orientation update \(\operatorname{rotate\_hilbert}\) is a piecewise affine transform:

\[
\operatorname{rotate\_hilbert}(s, x, y, rx, ry) =
\begin{cases}
\big(y, x\big), & \text{if } ry = 0,\; rx = 0\\[4pt]
\big( (s-1) - y,\; (s-1) - x \big), & \text{if } ry = 0,\; rx = 1\\[4pt]
\big(x, y\big), & \text{if } ry = 1\;\text{(no pre-swap)}
\end{cases}
\]

Explanation:
- If \( ry = 0 \), the algorithm applies a pre-translation orientation correction. When \( rx = 0 \), it simply swaps \(x\) and \(y\). When \( rx = 1 \), it reflects both \(x\) and \(y\) about the center of the \( s \times s \) block, then swaps. This encodes a 90° rotation with or without mirroring, consistent with the Hilbert curve’s recursive construction.
- If \( ry = 1 \), no pre-swap orientation is needed.

After this orientation, the algorithm advances by \( s \cdot rx \) along \(x\) and \( s \cdot ry \) along \(y\). Equivalently, represent the step vector as \( s\,(rx, ry) \).

Key derived values:
- \( n = 2^{\text{order}} \)
- Total points in the traversal: \( n^2 = 4^{\text{order}} \).

Domain and range:
- Input: \( d \in \{0, 1, \dots, n^2 - 1\} \).
- Output: \( (x, y) \in \{0, 1, \dots, n-1\}^2 \).


### 3) Affine Normalization to the Square \([-1, 1]^2\)

To plot geometry on a symmetric, scale-invariant square, the integer grid point \((x, y)\) is mapped to a normalized coordinate \((x', y')\) with an affine transformation that sends the discrete range \( \{0,\dots,n-1\} \) to \([-1, 1]\):

\[
\begin{aligned}
x' &= \frac{2x}{n - 1} - 1,\\
y' &= \frac{2y}{n - 1} - 1.
\end{aligned}
\]

Parameters and roles:
- \(n\): side length, \( n = 2^{\text{order}} \).
- \(x, y\): integer grid coordinates.
- Output \(x', y'\): real coordinates in \([-1,1]^2\). The mapping sends corners \((0, 0) \mapsto (-1, -1)\) and \((n-1, n-1) \mapsto (1, 1)\).

Special case in the code: if \(n=1\), then the only point \((0, 0)\) maps to \((0.0, 0.0)\). This avoids division by zero and is consistent with the convention that a 1-point curve is centered.


### 4) Geometric Mappings Applied to the Normalized Curve

After normalization, a family of 2D warps are applied to transform the Hilbert path into various shapes. For each mapping, we document the equation, all parameters, and discuss its geometric behavior and constraints. Unless otherwise stated, the input domain is \((x, y) \in [-1,1]^2\), and the mapping returns \((u, v)\) in some target subset of \(\mathbb{R}^2\). Implementation details such as handling of the origin \((0, 0)\) are included as notes.


#### 4.1) Superellipse (Lamé) Mapping (Exponent \(p=4\))

Goal: Warp rays from the origin so that the image of the square approaches a superellipse (Lamé curve) of order 4. The general superellipse is defined by

\[
|u|^{p} + |v|^{p} = R^{p},\quad p > 0.
\]

In the code, \(p=4\) and \(R=1\). The implemented scaling proceeds in two steps:

1) Compute the L∞-normalized direction:
\[
x_b = \frac{x}{m},\quad y_b = \frac{y}{m},\quad m = \max(|x|, |y|).
\]
When \(m = 0\), set \((u, v) = (0, 0)\).

2) Scale along the ray \((x, y)\) by a factor \(c\) chosen so that \((u, v) = c\,(x, y)\) lies on the \(p=4\) Lamé boundary in the direction determined by \((x_b, y_b)\):

\[
c = \big( x_b^{4} + y_b^{4} \big)^{-\tfrac{1}{4}},\qquad (u, v) = c\,(x, y).
\]

Interpretation:
- The pair \((x_b, y_b)\) lies on the boundary of the L∞ unit square (at least one of \(|x_b|\) or \(|y_b|\) equals 1). The scale \(c\) enforces the constraint \(|u|^4 + |v|^4 = 1\) in that direction.
- This gives a square-to-superellipse warping that is continuous and monotone along rays through the origin, with the L∞ direction normalization stabilizing behavior near the axes.

Variables and parameters:
- Input \((x, y)\in[-1,1]^2\), \( m = \max(|x|, |y|) \).
- Output \((u, v)\) satisfies approximately the \(p=4\) Lamé boundary where the incoming ray intersects it.
- Numerical safeguard at \(m=0\): return \((0, 0)\).


#### 4.2) Shirley–Chiu Concentric Square-to-Disk Mapping

Goal: Map the square \([-1,1]^2\) to the unit disk \(u^2 + v^2 \le 1\) with good uniformity and continuity. The Shirley–Chiu mapping is a well-known piecewise definition that converts square coordinates into polar coordinates \((r, \phi)\) before returning \((u, v)\).

Let
\[
a = 2x,\quad b = 2y.
\]
Then define \((r, \phi)\) piecewise by the following cases (all divisions below are well-defined on their allowed branches; the implementation guards the origin explicitly):

\[
(r, \phi) =
\begin{cases}
\big(a, \ \tfrac{\pi}{4}\, \tfrac{b}{a}\big), & a > -b\ \text{and}\ a > b,\\[6pt]
\big(b, \ \tfrac{\pi}{4}\, \big(2 - \tfrac{a}{b}\big)\big), & a > -b\ \text{and}\ a \le b,\\[6pt]
\big(-a,\ \tfrac{\pi}{4}\, \big(4 + \tfrac{b}{a}\big)\big), & a \le -b\ \text{and}\ a < b,\\[6pt]
\big(-b,\ \tfrac{\pi}{4}\, \big(6 - \tfrac{a}{b}\big)\big), & a \le -b\ \text{and}\ a \ge b.
\end{cases}
\]

Finally convert back to Cartesian and rescale:

\[
(u, v) = \tfrac{1}{2}\,\big( r\cos\phi,\ r\sin\phi \big).
\]

Properties and intent:
- The mapping is continuous across case boundaries, sends the square boundary to the circle boundary, and distributes area reasonably uniformly.
- The factor \(\tfrac{1}{2}\) compensates for the initial scaling by \(a=2x\), \(b=2y\), ensuring \(r \in [0, 2]\) maps to \([0,1]\) in the disk.

Variables and parameters:
- Input \((x, y) \in [-1,1]^2\); origin case \((x, y) = (0, 0)\) maps to \((u, v) = (0,0)\).
- Output \((u, v)\) satisfies \( u^2 + v^2 \le 1 \).


#### 4.3) Simple L∞-Radial Mapping

Goal: Radially scale each point so that its L∞ radius becomes 1. This projects every square point onto the boundary of the L∞ unit ball (the square \([-1,1]^2\)) along a straight line from the origin.

Define the L∞ radius and scale:

\[
m = \max(|x|, |y|),\quad (u, v) =
\begin{cases}
\big(\tfrac{x}{m}, \tfrac{y}{m}\big), & m \ne 0,\\
(0, 0), & m = 0.
\end{cases}
\]

Properties:
- For all nonzero inputs, \( \max(|u|, |v|) = 1 \). The mapping is “radial” with respect to the L∞ norm and is well-defined for all \((x, y) \ne (0, 0)\).
- Geometrically, this is a square-to-square projection along rays through the origin.

Variables and parameters:
- Input \((x, y)\in[-1,1]^2\); output \((u, v)\in[-1,1]^2\) with L∞ norm equal to 1 (except at the origin).


#### 4.4) Naïve Polar Mapping (Identity in Polar Coordinates)

Goal: Demonstrate the polar-coordinate decomposition without additional warping. This mapping converts \((x, y)\) to polar and back, leaving the point unchanged.

Compute
\[
r = \sqrt{x^2 + y^2},\quad \theta = \operatorname{atan2}(y, x),\qquad (u, v) = (r\cos\theta,\ r\sin\theta) = (x, y).
\]

Observation:
- The result is the identity transformation in exact arithmetic. In practice, it serves as a baseline “radial” visualization or a placeholder where more sophisticated radial warps might be substituted.

Variables and parameters:
- Input/output \((x, y)\) in \([-1,1]^2\), unchanged (with the origin handled explicitly in code to avoid invoking \(\operatorname{atan2}(0,0)\)).


#### 4.5) Fernandez–Guasti (FG) Squircular Mapping

Goal: Map the square \([-1,1]^2\) toward a “squircle” shape, an intermediate form between square and circle, using a closed-form Fernandez–Guasti transformation.

With squareness parameter fixed in the code to \( s = 1 \), the mapping is

\[
u = x\, \sqrt{ 1 - \tfrac{s^2}{2}\, y^{2} },\qquad v = y\, \sqrt{ 1 - \tfrac{s^2}{2}\, x^{2} }.
\]

At \( s=0 \), the mapping would be the identity \((u, v) = (x, y)\). Increasing \( s \) pushes points inward more strongly near the corners, rounding the square toward a circle-like contour (but not exactly the Euclidean circle; instead it follows FG’s squircular isocurves).

Variables and parameters:
- Input \((x, y)\in[-1,1]^2\).
- Shape parameter \( s \in [0, 1] \) (here, \(s=1\)).
- Output \((u, v)\in\mathbb{R}^2\) lies on an FG squircle for points initially on the square boundary.


#### 4.6) Equal-Area Approximate Radial Mapping

Goal: Warping radial distances to better distribute area, inspired by the idea that disk area scales as \(\pi r^2\). A common equal-area transform from \(r\) to \(r'\) enforces \( r'^2 \propto r \), which suggests \( r' = \sqrt{r} \) (after appropriate normalization). The code applies the following radial-only warp:

\[
r = \sqrt{x^2 + y^2},\quad \theta = \operatorname{atan2}(y, x),\qquad r' = \sqrt{r},\qquad (u, v) = (r'\cos\theta,\ r'\sin\theta).
\]

Notes:
- As written, the input domain is still the square \([-1,1]^2\) rather than a pre-normalized disk, so the transform is an “equal-area-like” approximation rather than a strict square-to-disk area-preserving map. It compresses radii \( r \in [0, 1] \) toward larger values because \( \sqrt{r} \ge r \) for \( r \in [0, 1] \). If one first restricts to the unit disk, then \( r' = \sqrt{r} \) is the classical radial equal-area mapping.

Variables and parameters:
- Input \((x, y)\in[-1,1]^2\); output \((u, v)\) produced by a monotonic radial warp \( r \mapsto r' = \sqrt{r} \) with unchanged angle \(\theta\).


#### 4.7) Polynomial (Conformal-like) Complex Warp

Goal: Smooth corners and morph the square toward a rounder shape by adding higher-order complex polynomial terms to the identity mapping. Writing \( z = x + i y \), the implemented empirical transform is

\[
z' = z\; +\; a\, z^{5}\; +\; b\, z^{9},\qquad a = 0.0731647,\quad b = 0.00358709.
\]

Equivalently, in real coordinates \( z' = u + i v \) with \((u, v)\) the real and imaginary parts of the series above. The particular odd powers preserve rotational symmetries (e.g., mapping the axes to themselves) while introducing curvature that “rounds” the square. The coefficients \(a\) and \(b\) were chosen empirically; the mapping is reminiscent of truncated Schwarz–Christoffel-like adjustments but is not a literal SC integral.

Variables and parameters:
- Input \((x, y)\in[-1,1]^2\), encoded as \(z\).
- Output \((u, v)\) is the real/imaginary part of \( z' \) as defined above.


### 5) Edge Cases and Numerical Safeguards in the Mappings

Several mappings divide by quantities that can be zero at the origin or along axes. The code handles these cases explicitly:

- At \((x, y) = (0, 0)\), mappings that would otherwise divide by \(m = \max(|x|,|y|)\) or by \(a\) or \(b\) return \((0, 0)\).
- In the Shirley–Chiu mapping, formulas involving \(b/a\) or \(a/b\) only occur on branches where the denominator is known to be nonzero. The implementation additionally protects the origin and writes the piecewise conditions to avoid degeneracy.


### 6) Consolidated Parameter Glossary

- **order (k)**: Integer curve order. Higher \(k\) means a finer grid and longer path.
- **n**: Side length \( n = 2^{k} \). Total points \( n^2 = 4^k \).
- **d**: Hilbert index \( 0 \le d \le n^2 - 1 \) enumerating the path.
- **x, y**: Integer grid coordinates produced by the Hilbert mapping; \( 0 \le x, y \le n-1 \).
- **x', y'**: Normalized coordinates in \([-1, 1]^2\), defined by \( x' = 2x/(n-1) - 1 \), \( y' = 2y/(n-1) - 1 \).
- **s**: In the Hilbert algorithm, a doubling scale \( s = 1, 2, 4, \dots, n \) that parameterizes sub-square size. In FG mapping, a fixed squareness parameter with \( s=1 \) in this code.
- **rx, ry**: Orientation bits (0 or 1) extracted stepwise from \(d\) to control rotate/reflect/swap.
- **m**: L∞ radius \( m = \max(|x|, |y|) \) used to normalize directions and avoid division by very small values.
- **a, b**: Intermediate scaled coordinates in Shirley–Chiu mapping: \( a = 2x \), \( b = 2y \).
- **r, r'**: Euclidean radius before and after a radial transform. For example, \( r = \sqrt{x^2 + y^2} \) and in the equal-area approximation \( r' = \sqrt{r} \).
- **\theta**: Polar angle \( \theta = \operatorname{atan2}(y, x) \).
- **z**: Complex encoding of a 2D point, \( z = x + i y \), used in the polynomial warp.
- **a, b (coefficients)**: Real scalar weights in the polynomial warp: \( a = 0.0731647 \), \( b = 0.00358709 \).


### 7) Domains, Codomains, and Boundary Behavior

- The normalized Hilbert path lies entirely in the square \([-1, 1]^2\). Thus, all mapping inputs are restricted to that domain.
- Superellipse: Rays land on the \(p=4\) Lamé boundary; points inside are scaled accordingly, yielding a squircle-like shape that is less rounded than a Euclidean circle but more rounded than a square. Boundary points of the input square map to the superellipse boundary under appropriate scaling.
- Shirley–Chiu: The square boundary maps onto the unit circle \( u^2 + v^2 = 1 \), and interior points map smoothly into the unit disk.
- Simple L∞-radial: Every nonzero input maps to the L∞ boundary (another square). This is a projection to the square’s boundary along straight rays from the origin.
- Naïve polar: Identity. Boundary points remain boundary points, and interior points remain interior points.
- FG squircular: The square’s corners are rounded; the exact isocurves are FG squircles. The mapping smoothly deforms the square toward a rounded shape.
- Equal-area approximate: Radii are expanded by \( r \mapsto \sqrt{r} \) (for \( r \in [0,1] \)), pushing points outward and approximately equalizing area distribution if the domain were a disk. On the square, it’s an approximate effect.
- Polynomial warp: Corner regions are rounded by higher-order complex terms, with odd powers preserving axial symmetries. The mapping is smooth where the polynomial is smooth.


### 8) Complexity and Stability Notes

- The Hilbert mapping loop executes \( O(\log n) = O(\text{order}) \) iterations per index \( d \), where \( n = 2^{\text{order}} \). Computing the full curve of \( n^2 \) points thus costs \( O(n^2 \log n) \) using this direct method.
- All mappings are algebraic and operate pointwise after normalization. Their cost is \( O(1) \) per point.
- Numerical safeguards at the origin and on axes (e.g., avoiding division by zero) ensure stable output. The use of L∞ normalization in multiple places reduces instability near axes.




### 10) Practical Usage Notes

- The plotting logic uses Matplotlib to draw polyline segments that join successive points along the Hilbert traversal order. Subplots display different mappings side-by-side for visual comparison.
- SVG output is generated by saving each mapped polyline with equal axis scaling and without axes, yielding clean vector silhouettes of the transformed Hilbert curve.
- The choice of order controls the level of detail: \(\text{order} = 1\) yields a coarse 4-point path; each increment multiplies the number of points by 4.




### 11) Summary of Core Equations

- Hilbert update per scale step:
\[ (x, y) \leftarrow \operatorname{rotate\_hilbert}(s, x, y, rx, ry) + s\,(rx, ry). \]
with
\[ (rx, ry) = \Big( \big\lfloor d/2 \big\rfloor \bmod 2,\; (d \oplus rx) \bmod 2 \Big),\quad d \leftarrow \big\lfloor d/4 \big\rfloor. \]

- Normalization to \([-1,1]^2\):
\[ x' = 2x/(n-1) - 1,\quad y' = 2y/(n-1) - 1. \]

- Superellipse (Lamé, \(p=4\)) scaling:
\[ (u, v) = c\,(x, y),\quad c = (x_b^{4} + y_b^{4})^{-1/4},\quad (x_b, y_b) = (x/m, y/m),\; m = \max(|x|, |y|). \]

- Shirley–Chiu concentric mapping:
\[ (u, v) = \tfrac{1}{2}\big( r\cos\phi,\ r\sin\phi \big) \]\nwith the piecewise rules for \( (r, \phi) \) given above.

- Simple L∞-radial projection:
\[ (u, v) = (x/m,\ y/m),\quad m = \max(|x|, |y|),\ (0,0) \mapsto (0,0). \]

- Naïve polar identity:
\[ (u, v) = (r\cos\theta,\ r\sin\theta) = (x, y). \]

- FG squircular mapping (with \( s=1 \)):
\[ u = x\,\sqrt{1 - \tfrac{1}{2} y^2},\quad v = y\,\sqrt{1 - \tfrac{1}{2} x^2}. \]

- Equal-area-like radial warp:
\[ r' = \sqrt{r},\quad (u, v) = (r'\cos\theta,\ r'\sin\theta). \]

- Polynomial complex warp:
\[ z' = z + 0.0731647\, z^{5} + 0.00358709\, z^{9}. \]


## Overview

We provide emphasis  on the Hilbert space-filling curve construction, the normalization used to map lattice coordinates to the square `[-1, 1]^2`, and the suite of 2D mappings that transform the normalized Hilbert curve into a variety of shapes (superellipse, concentric disk mapping, FG squircle, simple L∞-radial, a naïve polar identity, an approximate equal-area radial warp, and an empirical polynomial/conformal-like warp).


Taken together, these components illustrate a compact methodology for turning abstract mathematical ideas into concrete, reproducible artifacts. The Hilbert traversal supplies a coherent, locality-preserving ordering of planar samples; normalization to `[-1, 1]^2` removes scale and unit dependencies; and the mapping suite composes with this neutral coordinate system to explore how different geometric objectives, boundary correspondence, smoothness, area distribution, and symmetry, play out in practice. Because every stage is explicit and algebraic, the example doubles as a research scaffold: it is simple to replace one module (e.g., the mapping) while holding the others constant, and thereby isolate the visual and quantitative consequences of that change.

The significance of this example for learning is immediate. Many students first encounter space-filling curves as curiosities: continuous maps from a segment to a square that seem paradoxical until one internalizes the difference between topological and metric notions of dimension. Here, the Hilbert curve becomes an operational tool. By stepping through orders and watching the curve refine, students see the recursive rotate–reflect–swap logic materialize into a global, structured path. When that path is passed through the mappings, the effect of each design choice is legible in the evolving polyline: where segments cluster, how corners are rounded, which edges get stretched or compressed. The example thus functions as a living proof that careful definitions (bit extraction, normalization) empower controlled, interpretable transformations downstream.

For practice, the example foregrounds trade-offs that are often obscured by general statements like “low distortion” or “area preserving.” The Shirley–Chiu map provides an instructive benchmark for taking a square to a disk while respecting the boundary; yet its particular piecewise definitions create characteristic angular changes near certain seams. The Fernandez–Guasti squircular map is algebraically transparent and tunable; it shows how a single parameter can interpolate between square-like and circle-like behaviors without invoking heavy machinery. The Lamé superellipse emphasizes that “rounding” is not unique, choosing `p=4` rather than `p=2` encodes a distinct aesthetic and metric. The equal-area-inspired warp demonstrates how simple radial formulas can radically alter density, an insight that carries into sampling schemes and visualization integrity. Finally, the polynomial warp illustrates how truncated series can approximate complex boundary behavior with few terms, yielding smooth, symmetric deformations that are easy to compute and differentiate.

From an applications viewpoint, the example highlights a workflow that scales. Generating `n^2` points costs dominate, but the transforms are `O(1)` and vectorizable; the Hilbert backbone guarantees coherence useful for caches, tiling, and domain decomposition. In data systems, one might linearize tiles along the Hilbert index, then warp the display domain to match human perception goals without losing locality in storage. In scientific computing, partitioned grids assigned via Hilbert order can be visualized in round or squircular domains to emphasize central features or radial symmetries. In generative art, the same pipeline produces families of images where structure is preserved while silhouette and local curvature vary, enabling controlled exploration rather than ad hoc trial-and-error.

Equally important is the example’s attention to numerical safeguards. Edge cases, division by zero at the origin, branch denominators in piecewise maps, and degenerate polar angles, are handled explicitly. This discipline makes the pipeline robust across platforms and parameter ranges, enabling reuse in teaching and production. The normalization step is not cosmetic: it standardizes constants and ranges so that equations (and their errors) are interpretable across orders and mappings. These mundane choices often determine whether elegant theory yields stable code; surfacing them in a small, self-contained example is pedagogically valuable.

The design is intentionally extensible. Readers can add new mappings (true conformal maps, quasi-conformal variants, energy-minimizing deformations), expose the FG parameter, or sweep the Lamé exponent to generalize the superellipse. One can instrument the pipeline with diagnostics: local area change (Jacobian determinant), angular distortion, or metric stretch along the polyline, then compare heatmaps across mappings and orders. Swapping the traversal, for Morton/Z-order or Peano, would test how different locality patterns interact with the same deformations. Inverse maps could close the loop for workflows that shuttle data between square and disk domains. Each of these directions leverages the same three-stage architecture: discrete traversal, canonical normalization, and mappable outputs.

The significance of this example lies less in any single mapping than in the combinatorial clarity of the whole. It demonstrates how to decompose a geometric visualization problem into orthogonal, testable pieces; how to preserve coherence (via Hilbert) while experimenting with shape; and how to turn qualitative properties into design levers that can be swapped, tuned, and compared. That synthesis, of discrete geometry, mapping theory, numerical care, and visual design, translates across disciplines, from systems engineering to scientific graphics to computational art. The example thus stands as a compact template: understandable enough for classroom discussion, precise enough for research baselines, and flexible enough to serve as a studio for invention.






### 12) References and Further Reading  

- Hilbert, D. (1891). Über die stetige Abbildung einer Linie auf ein Flächenstück. Mathematische Annalen. Wikipedia: https://en.wikipedia.org/wiki/Hilbert_curve
- Peano, G. (1890). Sur une courbe, qui remplit toute une aire plane. Mathematische Annalen, 36(1), 157–160. Wikipedia: https://en.wikipedia.org/wiki/Peano_curve
- Sierpiński, W. (1912). Sur une nouvelle courbe continue qui remplit toute une aire plane. Bulletin International de l’Académie des Sciences de Cracovie. Wikipedia: https://en.wikipedia.org/wiki/Sierpi%C5%84ski_curve
- Sagan, H. (1994). Space-Filling Curves. Springer. DOI: https://doi.org/10.1007/978-1-4612-0871-6
- Bader, M. (2012). Space-Filling Curves: An Introduction with Applications in Scientific Computing. Springer. DOI: https://doi.org/10.1007/978-3-642-31046-1
- Butz, A. R. (1971). Alternative Algorithm for Hilbert’s Space-Filling Curve. IEEE Transactions on Computers, C-20(4), 424–426. IEEE: https://ieeexplore.ieee.org/document/5009079
- Hamilton, C. (2006). Compact Hilbert Indices. University of Cambridge Tech Report UCAM-CL-TR-688. PDF: https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-688.pdf
- Moon, B., Jagadish, H. V., Faloutsos, C., & Saltz, J. H. (2001). Analysis of the Clustering Properties of the Hilbert Space-Filling Curve. IEEE TKDE, 13(1), 124–141. IEEE: https://ieeexplore.ieee.org/document/908985
- Kamel, I., & Faloutsos, C. (1994). Hilbert R-tree: An Improved R-tree Using Fractals. VLDB. PDF: https://www.vldb.org/conf/1994/P500.PDF
- Skilling, J. (2004). Programming the Hilbert Curve. AIP Conference Proceedings, 707, 381–387. AIP: https://aip.scitation.org/doi/abs/10.1063/1.1751381
- Haverkort, H. J. (2011). How many three-dimensional Hilbert curves are there? Computational Geometry, 44(2), 95–114. DOI: https://doi.org/10.1016/j.comgeo.2010.08.001
- Gotsman, C., & Lindenbaum, M. (1996). On the Metric Properties of Discrete Space-Filling Curves. IEEE Transactions on Image Processing, 5(5), 794–797. DOI: https://doi.org/10.1109/83.491319
- Fong, N., & Gotsman, C. (1999). Discrete Hilbert Curves. Graphical Models and Image Processing, 61(3), 194–201. DOI: https://doi.org/10.1006/gmip.1999.0500
- Morton, G. M. (1966). A Computer Oriented Geodetic Data Base and a New Technique in File Sequencing. (Z-order curve). Wikipedia: https://en.wikipedia.org/wiki/Z-order_curve
- Shirley, P., & Chiu, K. (1997). A Low Distortion Map Between Disk and Square. Journal of Graphics Tools, 2(3), 45–52. (Publisher) https://www.tandfonline.com/doi/abs/10.1080/10867651.1997.10487458
- Fernandez-Guasti, R. (2005). The Squircle as a Transition Between the Square and the Circle. Revista Mexicana de Física E, 51(1), 1–10. (Squircle/FG mapping). Wikipedia: https://en.wikipedia.org/wiki/Squircle
- Superellipse (Lamé curve). Wikipedia: https://en.wikipedia.org/wiki/Superellipse
- Schwarz–Christoffel mapping (background for conformal polygonal maps). Wikipedia: https://en.wikipedia.org/wiki/Schwarz%E2%80%93Christoffel_mapping
- Driscoll, T. A., & Trefethen, L. N. (2002). Schwarz–Christoffel Mapping. Cambridge University Press. (Book) https://www.cambridge.org/core/books/schwarzchristoffel-mapping/4D0243B1B6C6A3BE9C1C7B9B4F9F2C96
- Savitzky, A., & Golay, M. J. E. (1964). Smoothing and Differentiation of Data by Simplified Least Squares Procedures. Analytical Chemistry, 36(8), 1627–1639. DOI: https://doi.org/10.1021/ac60214a047
- Mandelbrot, B. B. (1982). The Fractal Geometry of Nature. W. H. Freeman. Wikipedia: https://en.wikipedia.org/wiki/The_Fractal_Geometry_of_Nature
- Wikipedia: Hilbert curve overview and properties. https://en.wikipedia.org/wiki/Hilbert_curve
- Wikipedia: Space-filling curve overview. https://en.wikipedia.org/wiki/Space-filling_curve
- Wikipedia: Disk-to-square mapping methods (overview via linked articles). https://en.wikipedia.org/wiki/Square-to-circle_mapping
- Press, W. H., Teukolsky, S. A., Vetterling, W. T., & Flannery, B. P. (2007). Numerical Recipes: The Art of Scientific Computing (3rd ed.). Cambridge University Press. (Background on polynomial fits/filters) https://numerical.recipes/


