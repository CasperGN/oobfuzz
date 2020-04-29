from subprocess import Popen, PIPE
from os import environ
from setuptools import setup, find_packages
from setuptools.command.install import install

with open('README.md', 'r') as desc:
    long_desc = desc.read()

class InstallDependencies(install):

    def run(self):
        
        # Install Go
        process = Popen(['/usr/bin/apt-get', 'install', 'golang', '-y'], stdout=PIPE)
        stdout = process.communicate()[0].decode('utf-8')

        # Get GAU dependency
        process = Popen(['/usr/bin/go', 'get', '-u', 'github.com/lc/gau'], stdout=PIPE)
        stdout = process.communicate()[0].decode('utf-8')

        install.run(self)

setup(
        name = 'OOB Fuzz',
        version = '0.0.1',
        author = 'Casper G. Nielsen',
        author_email = 'whopsec@protonmail.com',
        description = 'Conduct OOB Fuzzing of targets with payloads towards callback server',
        long_description = long_desc,
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/Entropy-Team/recon-oobfuzz',
        packages = find_packages(),
        install_requires=[
            'requests',
        ],
        data_files=[('/usr/bin/', [f'{environ["HOME"]}/go/bin/gau'])],
        cmdclass={'install': InstallDependencies},
        classifiers = [
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
        ],
        python_requires = '>=3.4',
)