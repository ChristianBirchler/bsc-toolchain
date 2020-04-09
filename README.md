# BSC-TOOLCHAIN
This repository provides a automation script which enables you to run tests of maven-based software projects of specific git versions with a specified Java agent. In order to run this automation script you need to specify the projects, tests and versions in a `.csv` file.

# Requirements
- Python 3.6 (not tested with newer versions)

# Usage
```{bash}
$ ./toolchain.py
```
Please consolidate the `toolchain.py` for further details about the configuration. The main configuration are set by global variables in the `if __name__ == "__main__":` section.

