import streamlit as st
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt
import numpy as np
import pathlib

st.set_page_config(page_title="Quantum Single Qubit Visualizer", layout="centered")
st.title("Quantum Single Qubit Visualizer")
st.markdown(
    """
    This app lets you apply a quantum gate to a single qubit and visualize its state.
    Choose a gate below and see the resulting state vector and Bloch sphere representation.
    """
)

# Load CSS from the 'assets' folder
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

css_path = pathlib.Path("assets/styles.css")
load_css(css_path)

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

st.subheader("Apply Quantum Gates")

# Row 1
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("I", key="I", use_container_width=True):
        st.session_state.gate_sequence.append("I")
with col2:
    if st.button("X", key="X", use_container_width=True):
        st.session_state.gate_sequence.append("X")
with col3:
    if st.button("Y", key="Y", use_container_width=True):
        st.session_state.gate_sequence.append("Y")
with col4:
    if st.button("Z", key="Z", use_container_width=True):
        st.session_state.gate_sequence.append("Z")
with col5:
    if st.button("H", key="H", use_container_width=True):
        st.session_state.gate_sequence.append("H")

# Row 2
col6, col7, col8, col9, col10 = st.columns(5)
with col6:
    if st.button("S", key="S", use_container_width=True):
        st.session_state.gate_sequence.append("S")
with col7:
    if st.button("T", key="T", use_container_width=True):
        st.session_state.gate_sequence.append("T")
with col8:
    if st.button("RX", key="RX", use_container_width=True):
        st.session_state.gate_sequence.append("RX")
with col9:
    if st.button("RY", key="RY", use_container_width=True):
        st.session_state.gate_sequence.append("RY")
with col10:
    if st.button("RZ", key="RZ", use_container_width=True):
        st.session_state.gate_sequence.append("RZ")

if st.button("Clear all", key="clear_all", use_container_width=True):
    st.session_state.gate_sequence = []
    st.rerun()
  
if st.session_state.gate_sequence:
    st.subheader("Gate Sequence:")
    rows = [st.session_state.gate_sequence[i:i+5] for i in range (0, len(st.session_state.gate_sequence), 5)]
    for row in rows:
        cols = st.columns(len(row))
        for idx, (gate, col) in enumerate(zip(row, cols)):
            with col:
                real_idx = (rows.index(row) * 5) + idx
                if st.button(f"{gate} ❌", key=f"del_{real_idx}", use_container_width=True, type="primary"):
                    st.session_state.gate_sequence.pop(real_idx)
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
    st.pyplot(qc.draw("mpl"), use_container_width=True)

with col12:
    st.subheader("Bloch Sphere:")
    fig_bloch = plt.figure()
    ax_bloch = fig_bloch.add_subplot(projection='3d')
    plot_bloch_vector(bloch, ax=ax_bloch)
    st.pyplot(fig_bloch, use_container_width=True)
    