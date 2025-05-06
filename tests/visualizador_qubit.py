import streamlit as st
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt
import numpy as np
import io

st.set_page_config(page_title="Visualizador de Qubits", layout="centered")

st.title("🔮 Visualizador de Qubits Interactivo")

# Selección de puertas
st.sidebar.header("📌 Aplicar puertas cuánticas")
gates = st.sidebar.multiselect(
    "Selecciona las puertas que quieras aplicar (en orden):",
    ["H", "X", "Z", "RX(π/2)", "RY(π/2)", "RZ(π/2)"]
)

# Crear circuito
qc = QuantumCircuit(1)
for gate in gates:
    if gate == "H":
        qc.h(0)
    elif gate == "X":
        qc.x(0)
    elif gate == "Z":
        qc.z(0)
    elif gate == "RX(π/2)":
        qc.rx(np.pi / 2, 0)
    elif gate == "RY(π/2)":
        qc.ry(np.pi / 2, 0)
    elif gate == "RZ(π/2)":
        qc.rz(np.pi / 2, 0)

# Estado antes de medir
state = Statevector.from_instruction(qc)
amplitudes = state.data
prob_0 = np.abs(amplitudes[0])**2
prob_1 = np.abs(amplitudes[1])**2

st.subheader("🧠 Estado cuántico (antes de medir)")
st.markdown(f"- Amplitudes: {np.round(amplitudes, 3)}")
st.markdown(f"- Probabilidades: |0⟩ = {prob_0:.2f}, |1⟩ = {prob_1:.2f}")

# Mostrar esfera de Bloch
st.subheader("🧭 Esfera de Bloch")
bloch_fig = plot_bloch_vector(state.data)
buf = io.BytesIO()
plt.savefig(buf, format="png")
st.image(buf)

# Botón para medir (colapso)
if st.button("📉 Medir el qubit"):
    from qiskit_aer import Aer
    from qiskit import transpile

    qc.measure_all()
    simulator = Aer.get_backend("qasm_simulator")
    transpiled = transpile(qc, simulator)
    result = simulator.run(transpiled, shots=1).result()
    counts = result.get_counts()
    colapso = list(counts.keys())[0]
    st.success(f"🧨 El qubit colapsó a: |{colapso}⟩")