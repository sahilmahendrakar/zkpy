# Contributing to zkpy
## Environment Setup
To get started with developing on zkpy, run the following steps:
1. Clone zkpy from git
```
git clone https://github.com/sahilmahendrakar/zkpy.git
cd zkpy
```
2. Create and load a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```
3. Install snarkjs
```
npm install -g snarkjs
```
4. Install circom. Instructions [here](https://docs.circom.io/getting-started/installation/)
5. Install dev dependencies
```
make develop
```

## Issues
If you spot a problem, check if an issue already exists. If no issues exist for the problem you see, feel free to open an issue.

Feel free to look through existing issues to find problems that need to be fixed. You are welcome to open a PR to fix open issues.

## Pull Requests
Please feel encouraged to make pull requests for changes and new features! Before making a pull request, ensure the following works:
1. All tests pass
```
make test
```
2. Lint passes
```
make lint
```
If needed, run 
```
make fix
```
3. Ensure all checks pass on Github