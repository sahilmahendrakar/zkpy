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
    def start(self, curve='bn128', constraints='14'):
        # snarkjs powersoftau new bn128 14 pot14_0000.ptau -v
        proc = subprocess.run(['snarkjs', 'powersoftau', 'new', curve, constraints, self.ptau_file, "-v"], capture_output=True)
        
    def contribute(self, name="", entropy=""):
        # If no random text is supplied, generate 100 random characters
        if entropy == "":
            entropy = ''.join(random.choices(string.ascii_lowercase, k=100))
        if entropy[-1] != "\n":
            entropy += "\n"
        new_ptau_file = str(uuid.uuid4())+".ptau"
        proc = subprocess.run(["snarkjs", "powersoftau", "contribute", self.ptau_file, new_ptau_file, f'--name="{name}"', "-v", f'-e={entropy}'], capture_output=True,)
        self.ptau_file = new_ptau_file
        print(proc.stdout.decode('utf-8'))

    # TODO: Handle import / export contributions from 3rd party software

    def test(self):
        proc = subprocess.run(['snarkjs', '--help'], capture_output=True)
        print(proc.stdout.decode('utf-8'))

    def testos(self):
        print(self.output_dir)
        print(os.getcwd())

ptau = PTau()
ptau.start()