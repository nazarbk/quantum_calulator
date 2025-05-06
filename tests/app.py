from flask import Flask, request, jsonify
from qiskit import *
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector

app = Flask(__name__)

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    gates = data.get('gates',[])

    simulator = Aer.get_backend('qasm_simulator')

    # Create circuit with 1 qubit
    qc = QuantumCircuit(1)

    # Apply the received doors
    for gate in gates:
        if gate == 'h':
            qc.h(0)
        elif gate == 'x':
            qc.x(0)
        elif gate == 'z':
            qc.z(0)
        elif gate.startswith('rz'):
            # For example: 'rz(pi/4)'
            angle = gate[3:-1] # Extract the value between parenthesis
            qc.rz(eval(angle), 0)
        elif gate == 'measure':
            qc.measure(0, 0)


    # Get the State Vector
    state = Statevector.from_instruction(qc)
    amplitudes = state.data.tolist()
    probabilities = [abs(a) ** 2 for a in amplitudes]

    result = {
        'amplitudes': [complex(a).__str__() for a in amplitudes],
        'probabilities': probabilities
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)