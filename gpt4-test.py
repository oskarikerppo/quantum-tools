from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit.circuit import Parameter
from qiskit.circuit.library import QFT
from qiskit.circuit.library.standard_gates import RZGate
 
def controlled_phase_rotations(circuit, control, target, aux, n):
    theta = Parameter("θ")
    for i in range(n):
        for j in range(n):
            for k in range(j+1):
                circuit.append(RZGate(theta).control(1), [control[i], target[j]])
                circuit.u1(-theta / 2 ** (j - k), aux[j])
 
def add_qft(circuit, control, target, aux, n):
    circuit.append(QFT(n, do_swaps=False, inverse=False), target)
    circuit.append(QFT(n, do_swaps=False, inverse=False), aux)
    controlled_phase_rotations(circuit, control, target, aux, n)
    circuit.append(QFT(n, do_swaps=False, inverse=True), target)
    circuit.append(QFT(n, do_swaps=False, inverse=True), aux)
 
def create_addition_circuit(n, a, b):
    qc = QuantumCircuit(3 * n)
 
    # Prepare input state
    for idx, bit in enumerate(reversed(bin(a)[2:].zfill(n))):
        if bit == '1':
            qc.x(idx)
    for idx, bit in enumerate(reversed(bin(b)[2:].zfill(n))):
        if bit == '1':
            qc.x(n + idx)
 
    # Perform addition using QFT
    add_qft(qc, list(range(0, n)), list(range(n, 2*n)), list(range(2*n, 3*n)), n)
 
    return qc
 
# Define the inputs
n = 3
a = 5
b = 3
 
# Create the quantum circuit
qc = create_addition_circuit(n, a, b)
 
# Execute the circuit on the statevector simulator
backend = Aer.get_backend('statevector_simulator')
result = execute(qc, backend).result()
statevector = result.get_statevector()
 
# Print the final state
print("Final state:", statevector)
 