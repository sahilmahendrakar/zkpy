''' CLI Wrapper for SnarkJS Powers of Tau '''
import subprocess
import os

class PTau:
    def __init__(self, ptau_file="ptau.ptau"):
        self.ptau_file = ptau_file

    # TODO: Check return code of process
    # Begins a power of tau ceremony, curve is the curve to use 
    # and constraints is the number of constraints raised to the power of 2
    def start(self, curve='bn128', constraints='14'):
        proc = subprocess.run(['snarkjs', 'powersoftau', 'new', curve, constraints, self.ptau_file], capture_output=True)
        

    def test(self):
        proc = subprocess.run(['snarkjs', '--help'], capture_output=True)
        print(proc.stdout.decode('utf-8'))

    def testos(self):
        print(self.output_dir)
        print(os.getcwd())

ptau = PTau()
ptau.start()