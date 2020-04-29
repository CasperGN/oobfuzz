# recon-oobfuzz

Conduct OOB Fuzzing of targets with payloads towards callback server

*Brought to you with courtesey of **Team Entropy**, with love from*  
[@ninposec](https://github.com/ninposec), [@mortensteenrasmussen](https://github.com/mortensteenrasmussen) & [@CasperGN](https://github.com/CasperGN)

## Installation

Run installation via setup:
```
$ pip3 install -e git+https://github.com/CasperGN/PyIntruder#egg=PyIntruder; sudo -H python3 -m pip install .
```

**Reasoning:**  
The packaged `PyIntruder` is for Python2.7 and wont install under pip3.
OOBFuzz requires [GAU](https://github.com/lc/gau) to run. As such, we need to `apt-get install golang` and fetch the binary with `go get` and move it into `/usr/bin`.
This requires root permissions (unless obscure suid perhaps?) in order to do so. 
If in doubt, please chech [setup.py](setup.py) to ensure that nothing malicious is happening.

## External libs and thanks
  
- [GAU](https://github.com/lc/gau)
- [PyIntruder](https://github.com/sirpsycho/PyIntruder)