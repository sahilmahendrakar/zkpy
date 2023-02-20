''' CLI Wrapper for SnarkJS and Circom; Handles compiling, proving, and verifying a circuit '''

import subprocess
import os

# TODO: add ability to change working directory

class Circuit:
    def __init__(self, circ_file):
        self.circ_file = circ_file

    # These assume output directory is same as working directory
    def get_base(self):
        return self.circ_file.split(".")[0]

    def get_r1cs_file(self):
        return self.get_base() + ".r1cs"

    def get_sym_file(self):
        return self.get_base() + ".sym"
    
    def get_js_dir(self):
        return self.get_base() + "_js"
    
    def get_wasm_file(self):
        return os.path.join(self.get_js_dir(), self.get_base()+".wasm")

    def compile(self):
        proc = subprocess.run(["circom", self.circ_file, "--r1cs", "--sym", "--wasm"], capture_output=True)

    def get_info(self):
        pass


    def test(self):
        proc = subprocess.run(["touch", "hello_world"], capture_output=True)

circuit = Circuit("circom.circom")
circuit.get_base()