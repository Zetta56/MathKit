# MathKit

A set of math problem solvers and graphers used to better understand mathematical concepts. This project includes explanations and proofs in the source files' comments to give readers a more in-depth look into how each operation/function works. However, this isn't intended to be a full-fledged mathematical library for large projects. Other libraries, like [NumPy](https://numpy.org/), [SciPy](https://www.scipy.org/), and [SymPy](https://www.sympy.org/en/index.html), are more suited to this role.

## Installation
1. Run `git clone https://github.com/Zetta56/MathKit` in your desired folder
2. (Optional) Run `python -m venv <virtual_env_name>` to create a virtual environment that isolates your cloned project's dependencies from the rest of your system
3. (Optional) Run `.\<virtual_env_name>\Scripts\activate` to activate your virtual environment
4. Run `pip install -r requirements.txt` to install necessary dependencies

## Usage
After fully installing this project, you can call now math solvers and graphers in the `main.py` file and then run them with `python .\main.py`.

For more info about specific solvers/graphers, check out the following documentation:
- [Triangle](/docs/markdown/triangle.md)
- [Matrix](/docs/markdown/matrix.md)

## Testing

To test a file, run `python -m unittest test.<module_name>` 
- ex. `python -m unittest test.test_matrix`

To test all files, run `python -m unittest discover test`