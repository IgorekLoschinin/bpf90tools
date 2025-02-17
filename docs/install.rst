Installation
============

To install bpf90tools, follow the steps below.

Install from PyPi
-----------------

Install from github
-------------------

1. Create a virtual environment::

    mkdir MyProject
    cd Myproject
    python -m venv .venv
    source .venv/bin/activate  # for Linux/macOS
    .venv\Scripts\activate     # for Windows

2. Clone project::

    git clone https://github.com/IgorekLoschinin/f90tools.git
    cd bpf90tools

3. Building the project::

    python3 -m pip install --upgrade pip
    pip install build

4. Install the package in the project environment::

    .venv/bin/python3 -m build
    pip install .

5. Deleting a repository from a project::

    cd ../bpf90tools
    rm ./f90tools
