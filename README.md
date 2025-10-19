# The Art of Space-Filling: From Hilbert's Curve to Squircles

## Introduction

In the fascinating intersection of mathematics and computer science, there exist beautiful and profoundly useful concepts that challenge our understanding of space and dimension. This document explores one such concept: the journey of a **space-filling curve** from its natural home in a perfect square to a new, more rounded domain called a **squircle**. We will explore the elegant Hilbert Curve, understand the nature of the squircle, and then dive into a gallery of seven different mathematical techniques used to map one onto the other, each with its own unique character and purpose.

This project provides interactive tools to visualize these concepts, allowing you to see for yourself how abstract mathematical formulas translate into beautiful and complex diagrams.

## Getting Started

This project uses Python and requires a virtual environment to manage dependencies. Follow these steps to get up and running.

### Prerequisites

- You need to have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/).

### 1. Create a Virtual Environment

First, create a virtual environment to keep the project's dependencies isolated. Run this command in your terminal from the project's root directory:

```bash
python -m venv venv
```

### 2. Activate the Virtual Environment

Before you can install packages or run the application, you need to activate the virtual environment.

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS and Linux:**
```bash
source venv/bin/activate
```

Your terminal prompt should change to indicate that you are now in the `(venv)` environment.

### 3. Install Dependencies

With the virtual environment active, install the required packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

You can now run either of the user interfaces:

*   **To run the gallery view (recommended):**
    ```bash
    python HilbertSVG.py
    ```
*   **To run the comparator view:**
    ```bash
    python HilbertCompare.py
    ```

### Using the Tools

-   **Order Slider:** Use the slider at the bottom of the window to change the complexity of the Hilbert curves in real-time.
-   **Save SVGs:** Click the "Save SVGs" button to export clean, transparent-background vector images of the diagrams. The files will be saved into a new folder named with the current date and time.

## The Hilbert Curve: A Journey into Infinity

### What is it?

A Hilbert Curve is a type of **fractal**—a never-ending, self-similar pattern. It's also a **space-filling curve**, which means that although it is a continuous, one-dimensional line, it is drawn in a way that it passes through every single point within a two-dimensional space, like a square. Imagine drawing a single, unbroken line that completely colors in a square without ever lifting your pen; that is the essence of a Hilbert Curve.

### How does it work?

The magic of the Hilbert Curve lies in **recursion**. It is built by repeating a simple process over and over again.

1.  **Order 1:** Start with a simple, U-shaped line that connects the centers of four smaller squares within a larger one.
2.  **Order 2:** Take that entire U-shape, shrink it down, and place a copy in each of the four quadrants. Two of these copies are rotated to ensure the line remains continuous.
3.  **Higher Orders:** Repeat this process. With each new "order," the curve becomes more complex and convoluted, folding in on itself to fill the space more densely.

This recursive nature is why it's a fractal. If you were to zoom in on a section of a high-order Hilbert Curve, it would look just like a lower-order version of the entire curve.

### Why is it useful?

The most important property of the Hilbert Curve is **locality preservation**. This means that points that are close to each other along the one-dimensional line of the curve are also very likely to be close to each other in the two-dimensional square. This property is incredibly valuable in computer science:

*   **Databases:** It can be used to organize multi-dimensional data (like geographic coordinates) in a one-dimensional way, making searches and queries much more efficient.
*   **Image Processing:** It helps in dithering (simulating more colors) and compressing images by keeping related pixel data close together.
*   **Computer Graphics:** It can be used for rendering complex scenes and as an efficient pattern for 3D printing infill.

## The Squircle: A Shape Between Worlds

A **squircle** is exactly what it sounds like: a shape that smoothly blends the properties of a square and a circle. It has the straight, stable feel of a square but with soft, rounded corners. This makes it a visually pleasing shape often used in design, from app icons (the original iPhone used a form of squircle) to architecture.

Mathematically, the most common squircle is a type of **superellipse**, defined by the equation:

`x⁴ + y⁴ = r⁴`

Where `r` is the radius. By changing the exponent, you can create a whole family of shapes, from a square (exponent of infinity) to a diamond (exponent of 1) to a circle (exponent of 2).

## A Gallery of Transformations: 7 Ways to Squish a Square

How do you fit the Hilbert Curve, which is perfectly designed for a square, into a rounded shape like a circle or a squircle? The answer is **geometric mapping**—a set of mathematical rules that transform each point `(x, y)` from the original square to a new point `(x', y')` in the destination shape. 

Here are the seven methods implemented in our visualization tools, each with its own visual signature:

1.  **Superellipse (Lamé) Mapping:**
    *   **How it Works:** This method scales each point radially outwards from the center until it hits the boundary of the superellipse. It ensures the overall shape is a perfect, mathematically defined squircle.
    *   **Characteristics:** It produces a shape that is aesthetically pleasing and a true squircle. It is not area-preserving, meaning the density of the curve changes, becoming more compressed near the corners.

2.  **Shirley–Chiu Concentric Mapping:**
    *   **How it Works:** A brilliant method that maps concentric squares to concentric circles. It divides the square into four triangular regions and uses a different formula for each to ensure a smooth, continuous transformation.
    *   **Characteristics:** This is a true **area-preserving** map. The density of the curve remains uniform, making it look very natural and undistorted. It is widely used in computer graphics for high-quality sampling.

3.  **Fernandez-Guasti (FG) Squircular Mapping:**
    *   **How it Works:** This method uses a specific set of equations that can smoothly transition between a square and a circle using a "squareness" parameter. It's not a simple radial projection but a more complex analytical formula.
    *   **Characteristics:** It produces a unique squircle shape that is different from the superellipse. It is not area-preserving but is computationally efficient.

4.  **Simple Radial Mapping:**
    *   **How it Works:** This is the most intuitive but distorting method. It takes each point in the square and simply moves it to the boundary of the shape along a straight line from the center. 
    *   **Characteristics:** It creates significant distortion, as all points are pushed to the edge. This is not very useful in practice but provides an excellent visual baseline for what a "bad" mapping looks like.

5.  **Naïve Polar Mapping:**
    *   **How it Works:** This method converts the square's Cartesian coordinates `(x, y)` to polar coordinates `(radius, angle)` and then plots them directly. 
    *   **Characteristics:** This produces a distinctive "bow-tie" or pincushion distortion. It demonstrates what happens when you incorrectly assume that the geometry of a square and a circle are directly interchangeable.

6.  **Equal-Area (Approximate) Mapping:**
    *   **How it Works:** This is a simpler attempt at preserving area than the Shirley-Chiu method. It adjusts the radius of each point by taking its square root.
    *   **Characteristics:** While not perfectly area-preserving, it does a much better job of maintaining uniform density than naïve methods. It serves as a good middle-ground in terms of complexity and quality.

7.  **Polynomial (Conformal) Mapping:**
    *   **How it Works:** This method uses a polynomial equation derived from complex analysis (approximating the Schwarz-Christoffel transformation). Its goal is to be **conformal**, meaning it preserves angles.
    *   **Characteristics:** Local shapes within the curve are less distorted (e.g., tiny squares in the original grid remain tiny squares, not diamonds). This is crucial in applications like texture mapping in 3D graphics.