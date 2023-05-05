from zkpy.circuit import Circuit
from zkpy.ptau import PTau
from distutils import dir_util
from pytest import fixture
import os
from pathlib import Path


# Uses existing test files for better unit test isolation
@fixture
def datadir(tmpdir, request):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))
    return Path(tmpdir)


def test_compile_creates_3_files(tmp_path, datadir):
    circ_file = datadir / 'example_circuit.circom'
    circ = Circuit(circ_file, working_dir=tmp_path)
    circ.compile()
    r1cs_file = tmp_path / "example_circuit.r1cs"
    sym_file = tmp_path / "example_circuit.sym"
    js_dir = tmp_path / "example_circuit_js"
    assert r1cs_file.exists()
    assert sym_file.exists()
    assert js_dir.exists()


def test_get_info(datadir):
    circ_file = datadir / 'example_circuit.circom'
    r1cs_file = datadir / "example_circuit.r1cs"
    circ = Circuit(circ_file, r1cs=r1cs_file)
    circ.get_info()


def test_print_constraints(datadir):
    circ_file = datadir / 'example_circuit.circom'
    r1cs_file = datadir / "example_circuit.r1cs"
    sym_file = datadir / "example_circuit.sym"
    circ = Circuit(circ_file, r1cs=r1cs_file, sym_file=sym_file)
    circ.print_constraints()


def test_gen_witness(tmp_path, datadir):
    circ_file = datadir / 'example_circuit.circom'
    r1cs_file = datadir / "example_circuit.r1cs"
    sym_file = datadir / "example_circuit.sym"
    js_dir = datadir / "example_circuit_js"
    wasm_file = datadir / "example_circuit_js/example_circuit.wasm"
    circ = Circuit(circ_file, r1cs=r1cs_file, sym_file=sym_file, js_dir=js_dir, wasm=wasm_file, working_dir=tmp_path)
    inp_file = datadir / 'input.json'
    circ.gen_witness(input_file=inp_file)
    wtns_file = tmp_path / "witness.wtns"
    assert wtns_file.exists()


def test_contribute_phase2(tmp_path, datadir):
    circ_file = datadir / 'example_circuit.circom'
    zkey_file = datadir / 'zkey_groth16.zkey'
    circ = Circuit(circ_file, zkey=zkey_file, working_dir=tmp_path)
    circ.contribute_phase2(entropy="random text")
    new_zkey = tmp_path / circ.zkey_file
    assert new_zkey.exists() and new_zkey != zkey_file


def test_prove(tmp_path, datadir):
    circ_file = datadir / 'example_circuit.circom'
    zkey_file = datadir / 'zkey.zkey'
    wtns_file = datadir / 'witness.wtns'
    circ = Circuit(circ_file, witness=wtns_file, zkey=zkey_file, working_dir=tmp_path)
    circ.prove("plonk")
    public_file = tmp_path / circ.public_file
    proof_file = tmp_path / circ.proof_file
    assert public_file.exists() and proof_file.exists()


def test_verify_zkey(datadir):
    circ_file = datadir / 'example_circuit.circom'
    ptau_file = datadir / 'phase2.ptau'
    zkey_file = datadir / 'zkey_groth16.zkey'
    r1cs_file = datadir / "example_circuit.r1cs"
    ptau = PTau(ptau_file=ptau_file)
    circuit = Circuit(circ_file, r1cs=r1cs_file, zkey=zkey_file)
    assert circuit.verify_zkey(ptau)


def test_export_vkey(tmp_path, datadir):
    circ_file = datadir / 'example_circuit.circom'
    zkey_file = datadir / 'zkey.zkey'
    circuit = Circuit(circ_file, zkey=zkey_file, working_dir=tmp_path)
    circuit.export_vkey()
    vkey_file = tmp_path / circuit.vkey_file
    assert vkey_file.exists()


def test_verify(datadir):
    circ_file = datadir / 'example_circuit.circom'
    vkey_file = datadir / 'vkey.json'
    public_file = datadir / 'public.json'
    proof_file = datadir / 'proof.json'
    circuit = Circuit(circ_file)
    circuit.verify("plonk", vkey_file=vkey_file, public_file=public_file, proof_file=proof_file)


def test_check_circ_compiled_r1cs(tmp_path, datadir):
    circ_file = datadir / 'example_circuit.circom'
    circ = Circuit(circ_file, working_dir=tmp_path)
    assert circ.check_circ_compiled() is False


def test_check_circ_compiled_sym(tmp_path, datadir):
    circ_file = datadir / 'example_circuit.circom'
    r1cs_file = datadir / "example_circuit.r1cs"
    circ = Circuit(circ_file, working_dir=tmp_path, r1cs=r1cs_file)
    assert circ.check_circ_compiled() is False


def test_check_circ_compiled_wasm(tmp_path, datadir):
    circ_file = datadir / 'example_circuit.circom'
    r1cs_file = datadir / "example_circuit.r1cs"
    sym_file = datadir / "example_circuit.r1cs"
    circ = Circuit(circ_file, r1cs=r1cs_file, sym_file=sym_file, working_dir=tmp_path)
    assert circ.check_circ_compiled() is False


def test_export_r1cs_to_json(tmp_path, datadir):
    circ_file = datadir / 'example_circuit.circom'
    r1cs_file = datadir / "example_circuit.r1cs"
    circ = Circuit(circ_file, r1cs=r1cs_file, working_dir=tmp_path)
    json_file = tmp_path / circ.export_r1cs_to_json()
    assert json_file.exists()


def test_fullprove(tmp_path, datadir):
    circ_file = datadir / 'example_circuit.circom'
    input_file = datadir / 'input.json'
    circuit = Circuit(circ_file, working_dir=tmp_path)
    circuit.fullprove("plonk", input_file)
    public_file = tmp_path / circuit.public_file
    proof_file = tmp_path / circuit.proof_file
    assert public_file.exists() and proof_file.exists()
