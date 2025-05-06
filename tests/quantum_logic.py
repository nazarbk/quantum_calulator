from qiskit import *
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import numpy as np

class QuantumCalculator:
    def __init__(self):
        self.qc = QuantumCircuit(1, 1)
        self.backend = Aer.get_backend('statevector_simulator')

    def apply_gate(self, gate, *args):
        # Apply a quantum gate to the qubit
        if gate == "x":
            self.qc.x(0)
        elif gate == "y":
            self.qc.y(0)
        elif gate == "z":
            self.qc.z(0)
        elif gate == "h":
            self.qc.h(0)
        elif gate == "s":
            self.qc.s(0)
        elif gate == "t":
            self.qc.t(0)
        elif gate == "rx":
            self.qc.t(args[0], 0)
        elif gate == "ry":
            self.qc.t(args[0], 0)
        elif gate == "rz":
            self.qc.t(args[0], 0) 
    
    def get_statevector(self):
        # Return the current statevector of the qubit
        statevector = Statevector.from_instruction(self.qc)
        return statevector

    def measure(self):
        # Measure the qubit and collapse its state
        measure_circuit = self.qc.copy()
        measure_circuit.measure(0, 0)
        simulator = Aer.get_backend('qasm_simulator')
        result = (transpile(measure_circuit, simulator), backend=simulator, shots=1).result()
        counts = result.get_counts()
        return counts

    def reset(self):
        self.qc = QuantumCircuit(1, 1)