''' CLI Wrapper for SnarkJS Powers of Tau '''
import subprocess
import os
import random
import string
import uuid

class PTau:
    def __init__(self, ptau_file=str(uuid.uuid4())+".ptau"):
        self.ptau_file = ptau_file

    # TODO: Check return code of process
    # Begins a power of tau ceremony, curve is the curve to use 
    # and constraints is the number of constraints raised to the power of 2
    def start(self, curve='bn128', constraints='12'):
        # snarkjs powersoftau new bn128 14 pot14_0000.ptau -v
        proc = subprocess.run(['snarkjs', 'powersoftau', 'new', curve, constraints, self.ptau_file, "-v"], capture_output=True)
        
    # Contributes randomness (entropy) to power of tau ceremony
    def contribute(self, name="", entropy="", output_file=str(uuid.uuid4())+".ptau"):
        # If no random text is supplied, generate 100 random characters
        if entropy == "":
            entropy = ''.join(random.choices(string.ascii_lowercase, k=100))
        if entropy[-1] != "\n":
            entropy += "\n"
        proc = subprocess.run(["snarkjs", "powersoftau", "contribute", self.ptau_file, output_file, f'--name="{name}"', "-v", f'-e={entropy}'], capture_output=True,)
        self.ptau_file = output_file
        print(proc.stdout.decode('utf-8'))

    # TODO: Handle import / export contributions from 3rd party software


ptau = PTau()
ptau.start()