# %%

from pprop import Propagator #noqa
import pennylane as qml
import numpy as np
import pytest

# %%
def ry_chain(params):
    for i in range(4):
        qml.RY(params[i], wires=0)
    return [qml.expval(qml.PauliZ(0))]

def layered_ansatz(params):
    num_qubits = 6
    p = 0
    for _ in range(2):
        for q in range(num_qubits):
            qml.RY(params[p], wires=q)
            qml.RZ(params[p + 1], wires=q)
            p += 2
        for q in range(num_qubits - 1):
            qml.CNOT(wires=[q, q + 1])
    return [
        qml.expval(qml.PauliZ(0)),
        qml.expval(qml.PauliZ(2) @ qml.PauliZ(3)),
        qml.expval(qml.PauliX(5) + 0.5 * qml.PauliZ(4)),
    ]

def propagated(ansatz, **kwargs):
    prop = Propagator(ansatz, k1=None, **kwargs)
    prop.propagate()
    return prop

# %%
def test_sine_order_single_qubit():
    for k2 in range(4):
        prop = propagated(ry_chain, k2=k2, k2_mode="sine")
        assert prop(np.zeros(4))[0] == 1.0

    prop = propagated(ry_chain, k2=2, k2_mode="sine")
    assert abs(prop(np.full(4, 0.05))[0] - 0.980060) < 1e-6

    prop = propagated(ry_chain, k2=2, k2_mode="frequency")
    assert prop(np.zeros(4))[0] == 0.0

def test_sine_order_converges():
    exact = propagated(layered_ansatz)
    rng = np.random.default_rng(0)
    theta = rng.uniform(-0.1, 0.1, exact.num_params)
    zero = np.zeros(exact.num_params)

    errors = []
    for k2 in range(8):
        prop = propagated(layered_ansatz, k2=k2, k2_mode="sine")
        assert np.max(np.abs(prop(zero) - exact(zero))) == 0.0
        errors.append(np.max(np.abs(prop(theta) - exact(theta))))

    # A partial sum can overshoot at one fixed theta (here k2=3 -> 4 does),
    # so only every second step is required to shrink the error.
    assert all(b <= a for a, b in zip(errors, errors[2:])), errors
    assert errors[-1] < 1e-6, errors

def test_frequency_mode_unchanged():
    for k2 in (None, 0, 2, 4):
        default = propagated(layered_ansatz, k2=k2)
        frequency = propagated(layered_ansatz, k2=k2, k2_mode="frequency")
        assert default.k2_mode == "frequency"
        assert frequency.exprs == default.exprs

def test_bad_k2_mode():
    for mode in ("Sine", "cos", "", None, 1):
        with pytest.raises(ValueError):
            Propagator(ry_chain, k2=2, k2_mode=mode)
