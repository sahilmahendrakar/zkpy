# zkpy
A Python library that allows for easy compiling/proving/verifying of zk circuits.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

![GitHub issues](https://img.shields.io/github/issues/sahilmahendrakar/zkpy)

## Overview
ZKPy is a Python library that allows for easy compiling/proving/verifying of zk circuits. It will be primarily implemented as a wrapper of Circom or SnarkJS, allowing developers to incorporate their features into Python projects.

Upcoming Features:
- Can perform trusted setup (Powers of Tau and Phase 2)
- Can generate proofs for circuits written in Circom
- Can verify proofs given witness file and verification key
- Implements both Groth16 and PLONK proving schemes

## Dependencies
zkpy requires [Circom](https://docs.circom.io/getting-started/installation/) and [snarkjs](https://github.com/iden3/snarkjs). You can find installation instructions [here](https://docs.circom.io/getting-started/installation/)