#!/bin/sh
cd ..
git clone https://github.com/iden3/circom.git
cd circom
cargo build --release
cargo install --path circom
cd ../zkpy
npm install -g snarkjs