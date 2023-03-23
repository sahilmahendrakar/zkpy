''' CLI Wrapper for SnarkJS and Circom; Handles compiling, proving, and verifying a circuit '''

import subprocess
import os
import uuid
from zkpy.ptau import PTau

GROTH = "groth16"
PLONK = "plonk"
FFLONK = "fflonk"

# These handle finding file paths of created files during circuit compilation
# assume output directory is same as working directory
# TODO: Might want to move these into their own utility file


def get_base(circ_file):
    return os.path.basename(circ_file).split('.')[0]


def get_r1cs_file(circ_file):
    return get_base(circ_file) + ".r1cs"


def get_sym_file(circ_file):
    return get_base(circ_file) + ".sym"


def get_js_dir(circ_file):
    return get_base(circ_file) + "_js"


def get_wasm_file(circ_file):
    return os.path.join(get_js_dir(circ_file), get_base(circ_file) + ".wasm")


def gen_rand_filename():
    return str(uuid.uuid4())


def gen_zkey_file():
    return gen_rand_filename() + ".zkey"


# TODO: Add checks if subprocess fails
# TODO: Add getters and setters
class Circuit:
    def __init__(
        self,
        circ_file,
        output_dir="./",
        working_dir="./",
        r1cs=None,
        sym_file=None,
        js_dir=None,
        wasm=None,
        witness=None,
        zkey=None,
        vkey=None,
    ):
        self.circ_file = circ_file
        self.output_dir = output_dir
        self.working_dir = working_dir
        self.r1cs_file = r1cs
        self.sym_file = sym_file
        self.js_dir = js_dir
        self.wasm_file = wasm
        self.wtns_file = witness
        self.zkey_file = zkey
        self.vkey_file = vkey

    def compile(self):
        subprocess.run(
            ["circom", self.circ_file, "--r1cs", "--sym", "--wasm", '-o', self.output_dir],
            capture_output=True,
            cwd=self.working_dir,
        )
        self.r1cs_file = os.path.join(self.output_dir, get_r1cs_file(self.circ_file))
        self.sym_file = os.path.join(self.output_dir, get_sym_file(self.circ_file))
        self.wasm_file = os.path.join(self.output_dir, get_wasm_file(self.circ_file))
        self.js_dir = os.path.join(self.output_dir, get_js_dir(self.circ_file))

    # TODO: make sure compile was run first or files exist before continuing
    def get_info(self):
        proc = subprocess.run(
            ["snarkjs", "r1cs", "info", self.r1cs_file], capture_output=True, cwd=self.working_dir, check=True
        )
        print(proc.stdout.decode())

    def print_constraints(self):
        proc = subprocess.run(
            ["snarkjs", "r1cs", "print", self.r1cs_file, self.sym_file],
            capture_output=True,
            cwd=self.working_dir,
            check=True,
        )
        print(proc.stdout.decode())

    # TODO: Export r1cs to json

    # TODO: handle filename conflict
    # Need to input an input.json file
    def gen_witness(self, input_file, output_file=None):
        if output_file is None:
            output_file = os.path.join(self.output_dir, "witness.wtns")
        if self.wasm_file is None and self.js_dir is not None:
            self.wasm_file = os.path.join(self.output_dir, get_wasm_file(self.circ_file))
        gen_wtns_file = os.path.join(self.js_dir, "generate_witness.js")
        proc = subprocess.run(
            ["node", gen_wtns_file, self.wasm_file, input_file, output_file],
            capture_output=True,
            cwd=self.working_dir,
            check=True,
        )
        print(proc.stdout.decode('utf-8'))
        print(proc.stderr.decode('utf-8'))
        self.wtns_file = output_file

    # Sets up to generate proof. Scheme = proving scheme, ptau = previous powers of tau ceremony
    def setup(self, scheme, ptau, output_file=None):
        if output_file is None:
            output_file = os.path.join(self.output_dir, gen_zkey_file())
        # TODO: check scheme is either plonk, fflonk, or groth
        proc = subprocess.run(
            ["snarkjs", scheme, "setup", self.r1cs_file, ptau.ptau_file, output_file],
            capture_output=True,
            cwd=self.working_dir,
            check=True,
        )
        print(proc.stdout.decode('utf-8'))
        self.zkey_file = output_file

    def contribute_phase2(self, entropy="", output_file=None):
        if output_file is None:
            output_file = os.path.join(self.output_dir, gen_zkey_file())
        proc = subprocess.run(
            [
                "snarkjs",
                "zkey",
                "contribute",
                self.zkey_file,
                output_file,
                "-v",
                f'-e={entropy}',
            ],
            capture_output=True,
            cwd=self.working_dir,
            check=True,
        )
        print(proc.stdout.decode('utf-8'))
        self.zkey_file = output_file

    def prove(self, scheme, proof_out=None, public_out=None):
        if proof_out is None:
            proof_out = os.path.join(self.output_dir, "proof.json")
        if public_out is None:
            public_out = os.path.join(self.output_dir, "public.json")
        proc = subprocess.run(
            ["snarkjs", scheme, "prove", self.zkey_file, self.wtns_file, proof_out, public_out],
            capture_output=True,
            cwd=self.working_dir,
            check=True,
        )
        self.proof_file = proof_out
        self.public_file = public_out
        print(proc.stdout.decode('utf-8'))

    def verify_zkey(self, ptau, zkey_file=None):
        if zkey_file is None:
            zkey_file = self.zkey_file
        proc = subprocess.run(
            ["snarkjs", "zkey", "verify", self.r1cs_file, ptau.ptau_file, zkey_file],
            capture_output=True,
            cwd=self.working_dir,
            check=True,
        )
        print(proc.stdout.decode('utf-8'))
        if proc.stderr:
            return False
        else:
            return True

    def export_vkey(self, zkey_file=None, output_file=None):
        if zkey_file is None:
            zkey_file = self.zkey_file
        if output_file is None:
            output_file = os.path.join(self.output_dir, gen_rand_filename() + '.json')
        subprocess.run(
            ["snarkjs", "zkey", "export", "verificationkey", zkey_file, output_file],
            capture_output=True,
            cwd=self.working_dir,
            check=True,
        )
        self.vkey_file = output_file

    def verify(self, scheme, vkey_file=None, public_file=None, proof_file=None):
        if vkey_file is None:
            vkey_file = self.vkey_file
        if public_file is None:
            public_file = self.public_file
        if proof_file is None:
            proof_file = self.proof_file
        proc = subprocess.run(
            ["snarkjs", scheme, "verify", vkey_file, public_file, proof_file],
            capture_output=True,
            cwd=self.working_dir,
            check=True,
        )
        print(proc.stdout.decode('utf-8'))
        if proc.stderr:
            return False
        else:
            return True

    # TODO: Create a convenience function that handles compilation, setup, witness gen, and powers of tau for a circuit


if __name__ == "__main__":
    ptau = PTau(working_dir="./tmp")
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
    print(ptau.ptau_file)

    circuit = Circuit("./example_circuits/circom.circom", output_dir="./tmp")
    circuit.compile()
    circuit.get_info()
    circuit.print_constraints()
    circuit.gen_witness("./example_circuits/input.json")
    circuit.setup("plonk", ptau)
    circuit.prove("plonk")
    circuit.export_vkey()
    circuit.verify("plonk")
