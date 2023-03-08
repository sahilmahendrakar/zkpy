from zkpy.ptau import PTau
from zkpy.circuit import Circuit

example_circuit = """pragma circom 2.0.0;

/*This circuit template checks that c is the multiplication of a and b.*/

template Multiplier2 () {

   // Declaration of signals.
   signal input a;
   signal input b;
   signal output c;

   // Constraints.
   c <== a * b;
}

component main = Multiplier2();"""

example_input = """{"a": "3", "b": "11"}"""


def test_ptau_circuit(tmp_path):
    ptau = PTau(working_dir=tmp_path)
    ptau.start()
    ptau_file_start = tmp_path / ptau.ptau_file
    assert ptau_file_start.exists()
    ptau.contribute()
    ptau_file_contrib = tmp_path / ptau.ptau_file
    assert ptau_file_start != ptau_file_contrib
    assert ptau_file_contrib.exists()
    ptau.beacon()
    ptau_file_beacon = tmp_path / ptau.ptau_file
    assert ptau_file_beacon != ptau_file_contrib
    assert ptau_file_beacon.exists()
    ptau.prep_phase2()
    ptau_file_phase2 = tmp_path / ptau.ptau_file
    assert ptau_file_phase2 != ptau_file_beacon
    assert ptau_file_phase2.exists()

    circ_file = tmp_path / 'example_circuit.circom'
    with circ_file.open("w") as f:
        f.write(example_circuit)
    circ = Circuit(circ_file, working_dir=tmp_path)
    circ.compile()
    r1cs_file = tmp_path / "example_circuit.r1cs"
    sym_file = tmp_path / "example_circuit.r1cs"
    js_dir = tmp_path / "example_circuit_js"
    assert r1cs_file.exists()
    assert sym_file.exists()
    assert js_dir.exists()
    inp_file = tmp_path / 'input.json'
    with inp_file.open("w") as f:
        f.write(example_input)
    circ.gen_witness(input_file=inp_file)
    wtns_file = tmp_path / "witness.wtns"
    assert wtns_file.exists()

    circ.setup("plonk", ptau)
    zkey_file = tmp_path / circ.zkey_file
    assert zkey_file.exists()

    circ.prove("plonk")
    proof_file = tmp_path / "proof.json"
    public_file = tmp_path / "public.json"
    assert proof_file.exists()
    assert public_file.exists()


# def test_ptau_start_contribute(tmp_path):
#     ptau = PTau(working_dir=tmp_path)
#     ptau.start()
#     ptau_file_start = tmp_path / ptau.ptau_file
#     assert ptau_file_start.exists()
#     ptau.contribute()
#     ptau_file_contrib = tmp_path / ptau.ptau_file
#     assert ptau_file_start != ptau_file_contrib
#     assert ptau_file_contrib.exists()

# def test_ptau_start_contribute_beacon(tmp_path):
#     ptau = PTau(working_dir=tmp_path)
#     ptau.start()
#     ptau_file_start = tmp_path / ptau.ptau_file
#     assert ptau_file_start.exists()
#     ptau.contribute()
#     ptau_file_contrib = tmp_path / ptau.ptau_file
#     assert ptau_file_start != ptau_file_contrib
#     assert ptau_file_contrib.exists()
#     ptau.beacon()
#     ptau_file_beacon = tmp_path / ptau.ptau_file
#     assert ptau_file_beacon != ptau_file_contrib
#     assert ptau_file_beacon.exists()

# def test_ptau_start_contribute_beacon_phase2(tmp_path):
#     ptau = PTau(working_dir=tmp_path)
#     ptau.start()
#     ptau_file_start = tmp_path / ptau.ptau_file
#     assert ptau_file_start.exists()
#     ptau.contribute()
#     ptau_file_contrib = tmp_path / ptau.ptau_file
#     assert ptau_file_start != ptau_file_contrib
#     assert ptau_file_contrib.exists()
#     ptau.beacon()
#     ptau_file_beacon = tmp_path / ptau.ptau_file
#     assert ptau_file_beacon != ptau_file_contrib
#     assert ptau_file_beacon.exists()
#     ptau.prep_phase2()
#     ptau_file_phase2 = tmp_path / ptau.ptau_file
#     assert ptau_file_phase2 != ptau_file_beacon
#     assert ptau_file_phase2.exists()

# def test_int_verify_fails_if_file_changed(tmp_path):
#     ptau = PTau(working_dir=tmp_path)
#     ptau.start()
#     ptau_file_start = tmp_path / ptau.ptau_file
#     assert ptau_file_start.exists()
#     ptau.contribute()
#     ptau_file_contrib = tmp_path / ptau.ptau_file
#     assert ptau_file_start != ptau_file_contrib
#     assert ptau_file_contrib.exists()
#     with ptau_file_contrib.open("w") as f:
#         f.write('asdjfakjsfk')
#     assert ptau.verify() == False
