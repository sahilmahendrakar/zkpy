''' CLI Wrapper for SnarkJS proving and verifying a circuit '''

import subprocess

# TODO: add ability to change working directory

class Circuit:
    def __init__(self, circ_file):
        self.circ_file = circ_file

    def test(self):
        proc = subprocess.run(["touch", "hello_world"], capture_output=True)

circuit = Circuit("test")
circuit.test()