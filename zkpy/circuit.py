''' CLI Wrapper for SnarkJS and Circom; Handles compiling, proving, and verifying a circuit '''

import subprocess
import os

# TODO: add ability to change working directory

# These handle finding file paths of created files during circuit compilation
# assume output directory is same as working directory
def get_base(circ_file):
    return circ_file.split(".")[0]

def get_r1cs_file(circ_file):
    return get_base(circ_file) + ".r1cs"

def get_sym_file(circ_file):
    return get_base(circ_file) + ".sym"

def get_js_dir(circ_file):
    return get_base(circ_file) + "_js"

def get_wasm_file(circ_file):
    return os.path.join(get_js_dir(circ_file), get_base(circ_file)+".wasm")

# TODO: Add checks if subprocess fails
class Circuit:
    def __init__(self, circ_file):
        self.circ_file = circ_file

    def compile(self):
        proc = subprocess.run(["circom", self.circ_file, "--r1cs", "--sym", "--wasm"], capture_output=True)
        self.r1cs_file = get_r1cs_file(self.circ_file)
        self.sym_file = get_sym_file(self.circ_file)
        self.wasm_file = get_wasm_file(self.circ_file)
        self.js_dir = get_js_dir(self.circ_file)

    # TODO: make sure compile was run first or files exist before continuing
    def get_info(self):
        pass


    def test(self):
        proc = subprocess.run(["touch", "hello_world"], capture_output=True)

circuit = Circuit("circom.circom")
circuit.compile()