''' CLI Wrapper for SnarkJS and Circom; Handles compiling, proving, and verifying a circuit '''

import subprocess
import os
import uuid

from ptau import PTau

GROTH = "groth16"
PLONK = "plonk"
FFLONK = "fflonk"


# TODO: add ability to change working directory

# These handle finding file paths of created files during circuit compilation
# assume output directory is same as working directory
# TODO: Might want to move these into their own utility file
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

def gen_zkey_file():
    return str(uuid.uuid4())+".zkey"

# TODO: Add checks if subprocess fails
# TODO: Add getters and setters
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
        self.wtns_file = output_file

    # Sets up to generate proof. Scheme = proving scheme, ptau = previous powers of tau ceremony
    def setup(self, scheme, ptau, output_file=gen_zkey_file()):
        # TODO: check scheme is either plonk, fflonk, or groth
        proc = subprocess.run(["snarkjs", scheme, "setup", self.r1cs_file, ptau.ptau_file, output_file], capture_output=True)
        self.zkey_file = output_file

    def contribute_phase2(self, output_file=gen_zkey_file()):
        proc = subprocess.run(["snarkjs", "zkey", "contribute", self.zkey_file, output_file, "-v"], capture_output=True)
        self.zkey_file = output_file
        
    def prove(self, scheme, proof_out="proof.json", public_out="public.json"):
        proc = subprocess.run(["snarkjs", scheme, "prove", self.zkey_file, self.wtns_file, proof_out, public_out], capture_output=True)
        
    # TODO: Create a convenience function that handles compilation, setup, witness gen, and powers of tau for a circuit


if __name__ == "__main__":
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
    circuit.prove("plonk")