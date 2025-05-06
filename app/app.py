import streamlit as st
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt
import numpy as np

# Converts a statevector to its Bloch vector manually
def statevector_to_bloch_vector(state: Statevector):
    alpha = state.data[0]
    beta = state.data[1]

    x = 2 * (alpha.conjugate() * beta).real
    y = 2 * (alpha.conjugate() * beta).imag
    z = abs(alpha)** 2 - abs(beta)**2

    return [x, y, z]

st.set_page_config(page_title="Quantum Qubit Visualizer", layout="centered")
st.title("Quantum Qubit Visualizer")
st.markdown(
    """
    This app lets you apply a quantum gate to a single qubit and visualize its state.
    Choose a gate below and see the resulting state vector and Bloch sphere representation.
    """
)

# Persistent storage for gate sequence
if "gate_sequence" not in st.session_state:
    st.session_state.gate_sequence = []
if "last_added_gate" not in st.session_state:
    st.session_state.last_added_gate = None
                
# Two rows of gate buttons
st.subheader("Apply Quantum Gates")

# Gate selection
selected_gate = st.selectbox("Choose a quantum gate to apply:", ["I", "X", "Y", "Z", "H", "S", "T", "RX", "RY", "RZ"], key="selectbox_gate")

# Optional parameter for rotation gates

# Add gare only if new selection
current_gate = (selected_gate)
if current_gate != st.session_state.last_added_gate:
    st.session_state.gate_sequence.append(current_gate)
    st.session_state.last_added_gate = current_gate

if st.session_state.gate_sequence:
    st.subheader("Gate Sequence:")
    cols = st.columns(len(st.session_state.gate_sequence))
    for idx, (gate) in enumerate(st.session_state.gate_sequence):
        label = f"{gate}"
        with cols[idx]:
            if st.button(f"{label} ❌", key=f"del_{idx}"):
                st.session_state.gate_sequence.pop(idx)
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
        qc.rx(np.pi, 0)
    elif gate == 'RY':
        qc.ry(np.pi, 0)
    elif gate == 'RZ':
        qc.rz(np.pi, 0)


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
    st.pyplot(qc.draw("mpl"))

with col12:
    st.subheader("Bloch Sphere:")
    fig_bloch = plt.figure()
    ax_bloch = fig_bloch.add_subplot(projection='3d')
    plot_bloch_vector(bloch, ax=ax_bloch)
    st.pyplot(fig_bloch)
    