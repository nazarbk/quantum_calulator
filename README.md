# Quantum Single Qubit Visualizer

This project is a **Quantum Single Qubit Visualizer** built with Streamlit, Qiskit and Matplotlib. It allows users to apply quantum gates to a single qubit, visualize the resulting state in Dirac notation, and see its representation on the Bloch Sphere.

## 🚀 Features
- Apply a variety of **quantum gates (I, X, Y, Z, H, S, T, RX, RY, RZ)** to the qubit.
- Visualize the **quantum circuit**.
- Display the **Statevector** in Dirac notatio.
- Show the **Bloch Sphere**.
- Perform **Quantum Measurement** and see the result as a probability table.
- **Help section (ℹ️ Info)** that explains each concept in detail.

## 🧩 How to Run Locally
1. Clone this repository:
    ```bash
    git clone https://github.com/nazarbk/quantum_single_qubit_visualizer.git
2. Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
4. Run the Streamlit app:
    streamlit run app.py