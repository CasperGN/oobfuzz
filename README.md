# oobfuzz
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FCasperGN%2Foobfuzz.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FCasperGN%2Foobfuzz?ref=badge_shield)


Conduct OOB Fuzzing of targets with payloads towards callback server

*Brought to you with courtesey of **Team Entropy**, with :heart: from*  
[@ninposec](https://github.com/ninposec), [@mortensteenrasmussen](https://github.com/mortensteenrasmussen) & [@CasperGN](https://github.com/CasperGN)

## Installation

Run installation via setup:
```
$ sudo -H python3 -m pip install .
```

**Reasoning:**  
OOBFuzz requires [GAU](https://github.com/lc/gau) to run. As such, we need to `apt-get install golang` and fetch the binary with `go get` and move it into `/usr/bin`.
This requires root permissions (unless obscure suid perhaps?) in order to do so. 
If in doubt, please chech [setup.py](setup.py) to ensure that nothing malicious is happening.

## Run

Update the payloads folder containing your own payloads.

Most often want to run as such:  
```
$ python3 fuzzer.py --targets targets.txt --threads 17
```

## External libs and thanks
  
- [GAU](https://github.com/lc/gau)


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FCasperGN%2Foobfuzz.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FCasperGN%2Foobfuzz?ref=badge_large)