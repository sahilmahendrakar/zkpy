Usage and Examples
================================

Powers of Tau
---------------

Start by importing `PTau`::
    
    from zkpy.ptau import PTau

Here is an example use case walking through a powers of tau ceremony:

First, create PTau object::

    ptau = PTau()

Initialize powers of tau ceremony::

    ptau.start() 

Make first contribution::

    ptau.contribute()

Make second contribution with a name and specified entropy::

    ptau.contribute(name="second", entropy="random text") 

Apply beacon to finalize powers of tau ceremony::

    ptau.beacon()

Prepare for phase 2::

    ptau.prep_phase2()

The `PTau` object maintains an underlying powers of tau file throughout these operations. You can also import an existing ptau file::

    ptau = PTau(ptau_file="ptau_file.ptau")

At any stage, we can verify the powers of tau file is valid::

    ptau.verify()

Circuit
-----------

Start by importing `Circuit`::

    from zkpy.circuit import Circuit, PLONK

This class uses a circuit defined in a circom file to generate and verify zk proofs.

Here is an example scenario walking through compiling a circuit, generating witnesses, generating a proof, and verifying the proof:

First, create the circuit object::

    circuit = Circuit("./circuit.circom")

Compile the circuit::

    circuit.compile()

Get info about the circuit and print constraints::

    circuit.get_info()
    circuit.print_constraints()

Generate witness from an input file::

    circuit.gen_witness("./example_circuits/input.json")

Setup proof (this requires a previous powers of tau ceremony)::

    circuit.setup(PLONK, ptau)

Generate the proof::

    circuit.prove(PLONK)

Export verification key::

    circuit.export_vkey()

Verify proof::

    circuit.verify(PLONK, vkey_file="vkey.json", public_file="public.json", proof_file="proof.json")
