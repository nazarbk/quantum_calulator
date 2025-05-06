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
gates = st.selectbox("Choose a quantum gate to apply:", ["I", "X", "Y", "Z", "H", "S", "T", "RX", "RY", "RZ"], key="selectbox_gate")

# Optional parameter for rotation gates


# Quantum Circuit
qc = QuantumCircuit(1)

# Apply selected gate
for gate in gates:
    if gate == "I":
        qc.id(0)
        st.session_state.gate_sequence.append(("I", None))
    elif gate == 'X':
        qc.x(0)
        st.session_state.gate_sequence.append(("X", None))
    elif gate == 'Y':
        qc.y(0)
        st.session_state.gate_sequence.append(("Y", None))
    elif gate == 'Z':
        qc.z(0)
        st.session_state.gate_sequence.append(("Z", None))
    elif gate == 'H':
        qc.h(0)
        st.session_state.gate_sequence.append(("H", None))
    elif gate == 'S':
        qc.s(0)
        st.session_state.gate_sequence.append(("S", None))
    elif gate == 'T':
        qc.t(0)
        st.session_state.gate_sequence.append(("T", None))
    elif gate == 'RX':
        qc.rx(np.pi, 0)
        st.session_state.gate_sequence.append(("RX", np.pi)) # Default angle
    elif gate == 'RY':
        qc.ry(np.pi, 0)
        st.session_state.gate_sequence.append(("RY", np.pi))
    elif gate == 'RZ':
        qc.rz(np.pi, 0)
        st.session_state.gate_sequence.append(("RZ", np.pi))

# Display gate sequence with delete button
if st.session_state.gate_sequence:
    st.markdown("### Gate Sequence")
    for idx, (gate, angle) in enumerate(st.session_state.gate_sequence):
        col_a, col_b = st.columns([5, 1])
        with col_a:
            if angle is not None:
                st.write(f"{idx + 1}. {gate} (0 = {angle:.2f}rad)")
            else:
                st.write(f"{idx + 1}. {gate}")
        with col_b:
            if st.button("❌", key=f"delete_{idx}"):
                st.session_state.gate_sequence.pop(idx)
                st.experimental_rerun()

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
    