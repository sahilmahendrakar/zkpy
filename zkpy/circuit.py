''' CLI Wrapper for SnarkJS and Circom; Handles compiling, proving, and verifying a circuit '''

import subprocess
import os

from ptau import PTau

GROTH = "groth16"
PLONK = "plonk"
FFLONK = "fflonk"


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
        proc = subprocess.run(["snarkjs", "r1cs", "info", self.r1cs_file], capture_output=True)
        print(proc.stdout.decode())

    def print_constraints(self):
        proc = subprocess.run(["snarkjs", "r1cs", "print", self.r1cs_file, self.sym_file], capture_output=True)
        print(proc.stdout.decode())

    # TODO: Export r1cs to json

    # TODO: handle filename conflict
    def gen_witness(self, input_file, output_file="witness.wtns"):
        gen_wtns_file = os.path.join(self.js_dir, "generate_witness.js")
        proc = subprocess.run(["node", gen_wtns_file, self.wasm_file, input_file, output_file], capture_output=True)

    # Sets up to generate proof. Scheme = proving scheme
    def setup(self, scheme, ptau, output_file="circuit_final.zkey"):
        # TODO: check scheme is either plonk, fflonk, or groth
        proc = subprocess.run(["snarkjs", scheme, "setup", self.r1cs_file, ptau.ptau_file, output_file], capture_output=True)
        



ptau = PTau()
print("Starting powers of tau")
ptau.start()
print("Contribute")
ptau.contribute()
print("Beacon")
ptau.beacon()
print("Phase2")
ptau.prep_phase2()
print("Verify")
ptau.verify()

circuit = Circuit("circom.circom")
circuit.compile()
circuit.get_info()
circuit.print_constraints()
circuit.gen_witness("input.json")
circuit.setup("plonk", ptau)