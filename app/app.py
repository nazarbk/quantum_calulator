import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pathlib
import pandas as pd

st.set_page_config(page_title="Quantum Single Qubit Visualizer", layout="centered")
st.title("Quantum Single Qubit Visualizer")

# Load CSS from the 'assets' folder
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("assets/styles.css")
load_css(css_path)

simulator = Aer.get_backend('qasm_simulator')

# Converts a statevector to its Bloch vector manually
def statevector_to_bloch_vector(state: Statevector):
    alpha = state.data[0]
    beta = state.data[1]

    x = 2 * (alpha.conjugate() * beta).real
    y = 2 * (alpha.conjugate() * beta).imag
    z = abs(alpha)** 2 - abs(beta)**2

    return [x, y, z]

# Inicializar el historial si no existe
if "gate_sequence" not in st.session_state:
    st.session_state.gate_sequence = []

col20, col21 = st.columns(2)

st.markdown(
    """
    This app lets you apply a quantum gate to a single qubit and visualize its state.
    Choose a gate below and see the resulting state vector and Bloch sphere representation.
    """
)

with st.expander("ℹ️ More Info"):
    st.markdown("""
    ### Quantum Gates:
    - **I (Identity)**: Leaves the qubit unchanged.
    - **X (Pauli-X)**: Flips the qubit state (|0⟩ to |1⟩, |1⟩ to |0⟩).
    - **Y (Pauli-Y)**: Flips the qubit state and adds a phase of i.
    - **Z (Pauli-Z)**: Adds a phase of π to the |1⟩ state.
    - **H (Hadamard)**: Creates a superposition state (|+⟩ or |-⟩).
    - **S (Phase)**: Adds a phase of π/2 to the |1⟩ state.
    - **T (T Gate)**: Adds a phase of π/4 to the |1⟩ state.
    - **RX, RY, RZ (Rotation Gates)**: Rotate the qubit state around the X, Y, Z axis (π/2).
    
    ### What does the Measure?
    - **Measurement** is the process of collapsing the qubit's state into a definite state (|0⟩ or |1⟩).
    - Before measurement, the qubit exists in a superposition (a combination of |0⟩ and |1⟩).
    - When you click "Measure", the qubit is measured 1024 times, and the app shows:
        - **Counts**: How many times each outcome (|0⟩ or |1⟩) was observed.
        - **Probability**: The relative frequency of each outcome.

    ### What is the Statevector?
    - The **statevector** represents the quantum state of the qubit.
    - It's a complex vector with two amplitudes (α and β) representing the probability of the qubit being in |1⟩ or |0⟩.
    
    ### What is a Quantum Circuit?
    - A **quantum circuit** is a sequence of quantum gates applied to one or more qubits.
    - The circuit is read from the left to right, and each gate modifies the state of the qubit.
    - In this app, the quantum circuit is shown with the gates you have applied.


    ### What is a Bloch Sphere?
    - The **Bloch Sphere** is a 3D representation of a single qubit's state.
    - The north pole represents |0⟩, the south pole  represents |1⟩.
    - The X, Y and Z axes show how the qubit state is oriented.
    """)
    

st.subheader("Apply Quantum Gates")

# Row 1
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("I", key="I", use_container_width=True, help="Leaves the qubit unchanged."):
        st.session_state.gate_sequence.append("I")
with col2:
    if st.button("X", key="X", use_container_width=True, help="Flips the qubit state (|0⟩ ↔ |1⟩)."):
        st.session_state.gate_sequence.append("X")
with col3:
    if st.button("Y", key="Y", use_container_width=True, help="Flips the wubit and adds a phase of i."):
        st.session_state.gate_sequence.append("Y")
with col4:
    if st.button("Z", key="Z", use_container_width=True, help="Adds a phase of π to |1⟩."):
        st.session_state.gate_sequence.append("Z")
with col5:
    if st.button("H", key="H", use_container_width=True, help="Creates superposition of |0⟩ and |1⟩."):
        st.session_state.gate_sequence.append("H")

# Row 2
col6, col7, col8, col9, col10 = st.columns(5)
with col6:
    if st.button("S", key="S", use_container_width=True, help="Adds a phase of π to |1⟩."):
        st.session_state.gate_sequence.append("S")
with col7:
    if st.button("T", key="T", use_container_width=True, help="Adds a phase of π/4 to |1⟩."):
        st.session_state.gate_sequence.append("T")
with col8:
    if st.button("RX", key="RX", use_container_width=True, help="Rotation around X-axis (π/2)."):
        st.session_state.gate_sequence.append("RX")
with col9:
    if st.button("RY", key="RY", use_container_width=True, help="Rotation around Y-axis (π/2)."):
        st.session_state.gate_sequence.append("RY")
with col10:
    if st.button("RZ", key="RZ", use_container_width=True, help="Rotation around Z-axis (π/2)."):
        st.session_state.gate_sequence.append("RZ")


col15, col16 = st.columns(2)

with col15:
    if st.button("Clear all", key="clear_all", use_container_width=True):
            st.session_state.gate_sequence = []
            st.rerun()

# Quantum Circuit
qc = QuantumCircuit(1)

# Apply selected gate
for gate in st.session_state.gate_sequence:
    if gate == "I":
        qc.id(0)
    elif gate == 'X':
        qc.x(0)
    elif gate == 'Y':
        qc.y(0)
    elif gate == 'Z':
        qc.z(0)
    elif gate == 'H':
        qc.h(0)
    elif gate == 'S':
        qc.s(0)
    elif gate == 'T':
        qc.t(0)
    elif gate == 'RX':
        qc.rx(np.pi/2, 0)
    elif gate == 'RY':
        qc.ry(np.pi/2, 0)
    elif gate == 'RZ':
        qc.rz(np.pi/2, 0)

measurement_result = None
with col16:
    if st.button("Measure", key="measure", use_container_width=True):
        measure_circuit = qc.copy()
        measure_circuit.measure_all()

        result = simulator.run(transpile(measure_circuit, simulator), shots=1024).result()
        counts = result.get_counts()
        measurement_result = counts

if measurement_result:
    st.subheader("Measurement Result:")
    
    # Convert counts to DataFrame
    counts_df = pd.DataFrame([
        {"State": key, "Shots": val, "Probability": f"{val/1024:.2%}"}
        for key, val in measurement_result.items()
    ])

    st.table(counts_df.sort_values("State"))
  
if st.session_state.gate_sequence:
    st.subheader("Gate Sequence:")
    rows = [st.session_state.gate_sequence[i:i+5] for i in range (0, len(st.session_state.gate_sequence), 5)]
    for row in rows:
        cols = st.columns(len(row))
        for idx, (gate, col) in enumerate(zip(row, cols)):
            with col:
                real_idx = (rows.index(row) * 5) + idx
                if st.button(f"{gate}", key=f"del_{real_idx}", use_container_width=True, type="primary"):
                    st.session_state.gate_sequence.pop(real_idx)
                    st.rerun()

# Statevector and Bloch Sphere
# Get the statevector from the circuit
state = Statevector.from_instruction(qc)
bloch = statevector_to_bloch_vector(state)

# Output
st.subheader("Statevector (Dirac Notation):")
latex_str = state.draw('latex').data.replace('$$','')
st.latex(latex_str)

col11, col12 = st.columns(2)

with col11:
    st.subheader("Quantum Circuit:")

with col12:
    st.subheader("Bloch Sphere:")

col13, col14 = st.columns(2, vertical_alignment="center")

with col13:
    style = {
        "backgroundcolor": "#0e1117",
        "textcolor": "#ffffff",
        "linecolor": "#ffffff",
        "maxwidth": "80%"    
    }
    fig_qc = qc.draw("mpl", style=style, scale=2.0, fold=4)
    st.pyplot(fig_qc, use_container_width=True)

with col14:
    fig_bloch = plt.figure()
    ax_bloch = fig_bloch.add_subplot(projection='3d')
    plot_bloch_vector(bloch, ax=ax_bloch)
    st.pyplot(fig_bloch, use_container_width=True)
    