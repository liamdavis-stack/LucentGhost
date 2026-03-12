#!/usr/bin/env python3
import json
from datetime import datetime

from lucent_operators import (
    canonical_basis,
    gram_matrix,
    orthogonality_report,
    lucent_circuit,
)

def box(title):
    print("=" * 60)
    print(title.center(60))
    print("=" * 60)

def partition_basis(basis, block_size):
    if not isinstance(basis, list) or not basis:
        return None
    if not isinstance(block_size, int) or block_size <= 0:
        return None

    blocks = []
    for i in range(0, len(basis), block_size):
        blocks.append(basis[i:i + block_size])
    return blocks
def block_summary(blocks):
    if not isinstance(blocks, list):
        return None

    summary = []
    for i, block in enumerate(blocks, 1):
        dim = len(block[0]) if block and isinstance(block[0], list) else None
        summary.append({
            "block_index": i,
            "vectors_in_block": len(block),
            "ambient_dimension": dim
        })
    return summary

def generate_space(dimension, block_size=None):
    basis = canonical_basis(dimension)
    if basis is None:
        return None

    gram = gram_matrix(basis)
    ortho = orthogonality_report(basis)

    blocks = None
    blocks_info = None
    if block_size:
        blocks = partition_basis(basis, block_size)
        blocks_info = block_summary(blocks)

    circuit = lucent_circuit(
        basis,
        reference=canonical_basis(dimension),
        invariants=["nonempty", "vector_family_same_dim", "orthogonal_basis"]
    )

    return {
        "module": "HillGenPro",
        "version": "0.1",
        "timestamp": int(datetime.utcnow().timestamp()),
        "dimension": dimension,
        "basis": basis,
        "gram_matrix": gram,
        "orthogonality": ortho,
        "direct_sum_blocks": blocks_info,
        "circuit": circuit
    }
def print_space_report(payload):
    box("HILLGENPRO REPORT")
    print("module:", payload["module"])
    print("version:", payload["version"])
    print("dimension:", payload["dimension"])
    print()

    print("basis vectors:")
    for i, v in enumerate(payload["basis"], 1):
        print(f"e{i} =", v)
    print()

    print("gram matrix:")
    for row in payload["gram_matrix"]:
        print(row)
    print()

    ortho = payload["orthogonality"]
    print("orthogonality:")
    print("  orthogonal:", ortho["orthogonal"])
    print("  nonzero_diagonal:", ortho["nonzero_diagonal"])
    print("  orthonormal:", ortho["orthonormal"])
    print()

    if payload["direct_sum_blocks"] is not None:
        print("direct-sum block summary:")
        for block in payload["direct_sum_blocks"]:
            print(block)
        print()

    print("lucent circuit:")
    print("  accepted:", payload["circuit"]["accepted"])
    print("  registry:", payload["circuit"]["registry"])
    print("  stage:", payload["circuit"]["stage"])
    print()
def save_receipt(payload):
    ts = payload["timestamp"]
    out = f"/root/lucentghost/receipts/hillgenpro_{ts}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print("saved receipt:", out)
    print()

def main():
    box("HILLGENPRO")
    dim_text = input("Enter dimension n: ").strip()
    if not dim_text.isdigit():
        print("Invalid dimension.")
        return

    dimension = int(dim_text)
    block_text = input("Enter block size for direct-sum partition (blank for none): ").strip()
    block_size = int(block_text) if block_text.isdigit() else None

    payload = generate_space(dimension, block_size=block_size)
    if payload is None:
        print("Generation failed.")
        return

    print_space_report(payload)

    while True:
        cmd = input("[s] save receipt | [j] show raw json | [q] quit: ").strip().lower()
        if cmd == "q":
            break
        if cmd == "s":
            save_receipt(payload)
        elif cmd == "j":
            print(json.dumps(payload, indent=2))
            print()

if __name__ == "__main__":
    main()
