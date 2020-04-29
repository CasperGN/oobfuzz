import subprocess, os
from setuptools import setup, find_packages
from setuptools.command.install import install

with open('README.md', 'r') as desc:
    long_desc = desc.read()

class InstallGoDependencies(install):

    def run(self):
        # Set path
        self.pwd = os.path.dirname(os.path.realpath(__file__))

        # Install Go
        with open(os.devnull, 'w') as devnull:
            process = subprocess.Popen(['/usr/bin/apt-get', 'install', 'golang', '-y'], stdout=subprocess.PIPE, stderr=devnull)
        stdout = process.communicate()[0].decode('utf-8').split('\n')

        # Get GAU dependency
        with open(os.devnull, 'w') as devnull:
            process = subprocess.Popen(['/usr/bin/go', 'get', '-u', 'github.com/lc/gau'], stdout=subprocess.PIPE, stderr=devnull)
        stdout = process.communicate()[0].decode('utf-8').split('\n')

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
        data_files=[('/usr/bin/', [f'{os.environ["HOME"]}/go/bin/gau'])],
        cmdclass={
            'install': InstallGoDependencies,
        },
        classifiers = [
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
        ],
        python_requires = '>=3.4',
)
