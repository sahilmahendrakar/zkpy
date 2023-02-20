''' CLI Wrapper for SnarkJS Powers of Tau '''
import subprocess
import os
import random
import string
import uuid

PUBLIC_ENTROPY="0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"

def gen_ptau_file():
    return str(uuid.uuid4())+".ptau"

# TODO: add ability to change working directory

class PTau:
    def __init__(self, ptau_file=gen_ptau_file()):
        self.ptau_file = ptau_file

    # TODO: Check return code of process
    # Begins a power of tau ceremony, curve is the curve to use 
    # and constraints is the number of constraints raised to the power of 2
    def start(self, curve='bn128', constraints='12'):
        # snarkjs powersoftau new bn128 14 pot14_0000.ptau -v
        proc = subprocess.run(['snarkjs', 'powersoftau', 'new', curve, constraints, self.ptau_file, "-v"], capture_output=True)
        
    # Contributes randomness (entropy) to power of tau ceremony
    def contribute(self, name="", entropy="", output_file=gen_ptau_file()):
        # If no random text is supplied, generate 100 random characters
        if entropy == "":
            entropy = ''.join(random.choices(string.ascii_lowercase, k=100))
        if entropy[-1] != "\n":
            entropy += "\n"
        proc = subprocess.run(["snarkjs", "powersoftau", "contribute", self.ptau_file, output_file, f'--name="{name}"', "-v", f'-e={entropy}'], capture_output=True)
        self.ptau_file = output_file

    # TODO: Handle import / export contributions from 3rd party software

    # Finalizes phase 1 of the power of tau ceremony
    def beacon(self, output_file=gen_ptau_file(), public_entropy=PUBLIC_ENTROPY, iter=10):
        proc = subprocess.run(["snarkjs", "powersoftau", "beacon", self.ptau_file, output_file, public_entropy, str(iter)], capture_output=True)
        self.ptau_file = output_file

    def prep_phase2(self, output_file=gen_ptau_file()):
        proc = subprocess.run(["snarkjs", "powersoftau", "prepare", "phase2", self.ptau_file, output_file, "-v"], capture_output=True)
        self.ptau_file = output_file

    def verify(self):
        proc = subprocess.run(["snarkjs", "powersoftau", "verify", self.ptau_file], capture_output=True)
        print(proc.stdout.decode('utf-8'))    

    # TODO: Add way to cleanup files

if __name__ == "main":
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