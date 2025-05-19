## **🌀 Möbius Strip Analyzer**

This Python application computes and visualizes Möbius strips using parametric equations. It numerically estimates their **surface area** and **edge length**, generates 3D plots, and saves them with corresponding metrics into a Word document — useful for geometry research, visualization, or educational purposes.

---

## **📁 Project Structure**


`Mobius_Strip/`  
`├── mobius_strip.py         # Core class for geometry and plotting`  
`├── mobius_testcases.txt    # Input test cases`  
`├── Test.py                 # Test runner script for batch analysis`  
`├── mobius_plots/           # Folder where generated plots are saved`  
`└── Mobius_Strip_Results.docx # Word file with results and plots`

---

## **📦 Requirements**

Install the required packages with:

 
`pip install requirements.txt`

---

## **🧠 How It Works**

### **`mobius_strip.py`**

Encapsulates the logic in the `MobiusStrip` class:

* **Constructor** accepts radius `R`, strip width `w`, and resolution `n`.

* **Mesh** is computed from parametric equations, but lazily — only when needed.

* **Numerical Methods**:

  * `compute_surface_area()` uses cross product of partial derivatives and double integration (`scipy.integrate.simpson`).

  * `compute_edge_length()` approximates edge perimeter by summing distances between boundary segments.

* **Memory Optimized**:

  * Mesh generation is deferred (`lazy-loading`).

  * Garbage collection and explicit memory release between operations.

### **`analyze()` Method**

Returns:

* `[surface_area, edge_length]` as a list

* A `matplotlib` figure object ready to save/export

---

## **🧪 `mobius_testcases.txt`**

Each line contains parameters for one Möbius strip:

 
`# Format: R w n`  
`1.0 0.3 200`  
`1.5 0.2 150`  
`...`

Commented lines (`#`) and blanks are ignored.

---

## **🔁 `Test.py`**

Reads test cases and:

1. Instantiates the `MobiusStrip` object.

2. Computes surface area and edge length.

3. Saves the plot as a `.jpg`.

4. Inserts results and images into a Word document.

### **Key Features:**

* Skips oversized `n > 2000` cases to avoid memory overflow.

* Releases memory after each iteration using `plt.close()`, `del`, and `gc.collect()`.

* Supports batch processing of dozens of cases efficiently.

---

## **🧹 Memory Management**

* `matplotlib.use('Agg')` disables GUI rendering for better performance.

* Mesh arrays and plot objects are explicitly deleted after use.

* The `clear()` method ensures the `MobiusStrip` object releases memory before reuse.

---

## **📄 Output**

A Microsoft Word file named `Mobius_Strip_Results.docx` is created. Each test case includes:

* Input parameters

* Surface area and edge length

* A visual 3D plot of the strip

---

## **🚧 Challenges & Techniques**

* Möbius strip’s **non-orientability** was handled via full 0 to 2π traversal.

* Fine resolution grids improved integration accuracy.

* Used `numpy.gradient` for partial derivatives and `scipy.simpson` for accurate surface integration.

* Managed memory across potentially thousands of array entries and plots.

---

