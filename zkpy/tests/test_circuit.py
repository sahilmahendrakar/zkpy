from zkpy.circuit import Circuit
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


def test_gen_witness(tmp_path, datadir):
    circ_file = datadir / 'example_circuit.circom'
    r1cs_file = datadir / "example_circuit.r1cs"
    sym_file = datadir / "example_circuit.r1cs"
    js_dir = datadir / "example_circuit_js"
    wasm_file = datadir / "example_circuit_js/example_circuit.wasm"
    circ = Circuit(circ_file, r1cs=r1cs_file, sym_file=sym_file, js_dir=js_dir, wasm=wasm_file, working_dir=tmp_path)
    inp_file = datadir / 'input.json'
    circ.gen_witness(input_file=inp_file)
    wtns_file = tmp_path / "witness.wtns"
    assert wtns_file.exists()
