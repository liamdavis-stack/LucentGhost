import json
import math

MAX_QUBITS = 14

def _normalize(state):
    norm = math.sqrt(sum(abs(a) ** 2 for a in state))
    if norm == 0:
        raise ValueError("Cannot normalize zero vector")
    return [a / norm for a in state]

def _basis_state(bitstring):
    n = len(bitstring)
    size = 1 << n
    state = [0j] * size
    state[int(bitstring, 2)] = 1.0 + 0j
    return state

def _bell_state():
    return _normalize([1 + 0j, 0j, 0j, 1 + 0j])

def _ghz_state(n_qubits):
    if n_qubits < 2:
        raise ValueError("GHZ requires at least 2 qubits")
    size = 1 << n_qubits
    state = [0j] * size
    state[0] = 1 / math.sqrt(2)
    state[-1] = 1 / math.sqrt(2)
    return state
def _apply_x(state, n, target):
    new = [0j] * len(state)
    shift = n - 1 - target
    for i, amp in enumerate(state):
        j = i ^ (1 << shift)
        new[j] += amp
    return new

def _apply_z(state, n, target):
    new = state[:]
    shift = n - 1 - target
    for i in range(len(new)):
        if (i >> shift) & 1:
            new[i] = -new[i]
    return new

def _apply_h(state, n, target):
    new = [0j] * len(state)
    shift = n - 1 - target
    inv_sqrt2 = 1 / math.sqrt(2)
    for i, amp in enumerate(state):
        bit = (i >> shift) & 1
        j0 = i & ~(1 << shift)
        j1 = i | (1 << shift)
        if bit == 0:
            new[j0] += inv_sqrt2 * amp
            new[j1] += inv_sqrt2 * amp
        else:
            new[j0] += inv_sqrt2 * amp
            new[j1] -= inv_sqrt2 * amp
    return new

def _apply_cnot(state, n, control, target):
    new = [0j] * len(state)
    c_shift = n - 1 - control
    t_shift = n - 1 - target
    for i, amp in enumerate(state):
        j = i ^ (1 << t_shift) if ((i >> c_shift) & 1) else i
        new[j] += amp
    return new
def _probabilities(state):
    n = int(math.log2(len(state)))
    out = {}
    for i, amp in enumerate(state):
        p = abs(amp) ** 2
        if p > 1e-12:
            out[format(i, f"0{n}b")] = round(p, 12)
    return out

def _top_amplitudes(state, top_k=8):
    n = int(math.log2(len(state)))
    items = []
    for i, amp in enumerate(state):
        if abs(amp) > 1e-12:
            items.append((format(i, f"0{n}b"), str(amp), abs(amp)))
    items.sort(key=lambda x: x[2], reverse=True)
    return [{"basis": b, "amp": a} for b, a, _ in items[:top_k]]

def _norm(state):
    return float(sum(abs(a) ** 2 for a in state))

def _fidelity_pure(a, b):
    overlap = sum(x.conjugate() * y for x, y in zip(a, b))
    return float(abs(overlap) ** 2)

def _measure_first_qubit_purity_proxy(state, n):
    a00 = 0j
    a01 = 0j
    a10 = 0j
    a11 = 0j
    half = 1 << (n - 1)
    for r in range(half):
        amp0 = state[r]
        amp1 = state[r + half]
        a00 += amp0.conjugate() * amp0
        a01 += amp0.conjugate() * amp1
        a10 += amp1.conjugate() * amp0
        a11 += amp1.conjugate() * amp1
    return float((a00 * a00 + a01 * a10 + a10 * a01 + a11 * a11).real)
def run_glassbit():
    while True:
        print("\n=== GlassBitToolKit ===")
        print("[1] Bell demo")
        print("[2] GHZ demo")
        print("[3] Custom sandbox")
        print("[0] Return")
        choice = input("Select: ").strip()

        if choice == "1":
            state = _bell_state()
            receipt = {
                "module": "GlassBitToolKit",
                "mode": "bell_demo",
                "n_qubits": 2,
                "qubit_ceiling": MAX_QUBITS,
                "norm": round(_norm(state), 12),
                "probabilities": _probabilities(state),
                "top_amplitudes": _top_amplitudes(state),
                "fidelity_to_bell": round(_fidelity_pure(state, _bell_state()), 12),
                "purity_q0_proxy": round(_measure_first_qubit_purity_proxy(state, 2), 12),
            }
            print(json.dumps(receipt, indent=2))
        elif choice == "2":
            raw = input(f"GHZ qubits [2-{MAX_QUBITS}] (default 14): ").strip()
            n = 14 if raw == "" else int(raw)
            if n < 2 or n > MAX_QUBITS:
                print(f"Invalid qubit count. Use 2-{MAX_QUBITS}.")
                continue
            state = _ghz_state(n)
            receipt = {
                "module": "GlassBitToolKit",
                "mode": "ghz_demo",
                "n_qubits": n,
                "qubit_ceiling": MAX_QUBITS,
                "norm": round(_norm(state), 12),
                "probabilities": _probabilities(state),
                "top_amplitudes": _top_amplitudes(state),
                "fidelity_to_ghz": round(_fidelity_pure(state, _ghz_state(n)), 12),
                "purity_q0_proxy": round(_measure_first_qubit_purity_proxy(state, n), 12),
            }
            print(json.dumps(receipt, indent=2))
        elif choice == "3":
            raw_n = input(f"Number of qubits [1-{MAX_QUBITS}]: ").strip()
            if not raw_n.isdigit():
                print("Enter an integer.")
                continue
            n = int(raw_n)
            if n < 1 or n > MAX_QUBITS:
                print(f"Invalid qubit count. Use 1-{MAX_QUBITS}.")
                continue

            basis = input(f"Initial basis bitstring ({n} bits, default {'0'*n}): ").strip()
            if basis == "":
                basis = "0" * n
            if len(basis) != n or any(ch not in "01" for ch in basis):
                print("Invalid bitstring.")
                continue

            state = _basis_state(basis)
            ops = []
            print("Enter operations: H q | X q | Z q | CNOT c t")
            print("Blank line to run.\n")
            while True:
                line = input("op> ").strip()
                if line == "":
                    break
                parts = line.split()
                try:
                    if len(parts) == 2 and parts[0].upper() in ("H", "X", "Z"):
                        gate = parts[0].upper()
                        q = int(parts[1])
                        if q < 0 or q >= n:
                            raise ValueError
                        if gate == "H":
                            state = _apply_h(state, n, q)
                        elif gate == "X":
                            state = _apply_x(state, n, q)
                        elif gate == "Z":
                            state = _apply_z(state, n, q)
                        ops.append({"gate": gate, "target": q})
                    elif len(parts) == 3 and parts[0].upper() == "CNOT":
                        c = int(parts[1])
                        t = int(parts[2])
                        if c < 0 or c >= n or t < 0 or t >= n or c == t:
                            raise ValueError
                        state = _apply_cnot(state, n, c, t)
                        ops.append({"gate": "CNOT", "control": c, "target": t})
                    else:
                        print("Unrecognized operation.")
                except ValueError:
                    print("Invalid operation parameters.")
            state = _normalize(state)
            ghz_fidelity = None
            if n >= 2:
                ghz_fidelity = round(_fidelity_pure(state, _ghz_state(n)), 12)

            receipt = {
                "module": "GlassBitToolKit",
                "mode": "custom_sandbox",
                "n_qubits": n,
                "qubit_ceiling": MAX_QUBITS,
                "initial_basis": basis,
                "operations": ops,
                "norm": round(_norm(state), 12),
                "probabilities": _probabilities(state),
                "top_amplitudes": _top_amplitudes(state),
                "purity_q0_proxy": round(_measure_first_qubit_purity_proxy(state, n), 12),
                "fidelity_to_ghz_same_n": ghz_fidelity,
            }
            print(json.dumps(receipt, indent=2))

        elif choice == "0":
            return
        else:
            print("Invalid choice.")
