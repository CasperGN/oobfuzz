from sys import exit
from subprocess import Popen, PIPE
from os import environ
from setuptools import setup, find_packages
from setuptools.command.install import install

with open('README.md', 'r') as desc:
    long_desc = desc.read()

class InstallDependencies(install):

    def run(self):
        
        # Install Go
        try:
            # Debian based
            process = Popen(['/usr/bin/apt-get', 'install', 'golang', '-y'], stdout=PIPE)
        except IOError:
            # Fedora/Red hat 
            process = Popen(['/usr/bin/dnf', 'install', 'golang', '-y'], stdout=PIPE)
        process.communicate()[0].decode('utf-8')

        # Get GAU dependency
        process = Popen(['/usr/bin/go', 'get', '-u', 'github.com/lc/gau'], stdout=PIPE)
        process.communicate()[0].decode('utf-8')
        
        try:
            process = Popen(['/bin/cp', f'{environ["HOME"]}/go/bin/gau', '/usr/bin/gau'], stdout=PIPE)
        except EnvironmentError:
            print('This installer requires root permissions to copy Gau into /usr/bin/gau')
            exit(1)
        process.communicate()[0].decode('utf-8')

        install.run(self)

setup(
        name = 'OOB Fuzz',
        version = '0.1.0',
        author = 'Casper G. Nielsen',
        author_email = 'whopsec@protonmail.com',
        description = 'Conduct OOB Fuzzing of targets with payloads towards callback server',
        long_description = long_desc,
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/CasperGN/oobfuzz',
        cmdclass={'install': InstallDependencies},
        packages = find_packages(),            
        include_package_data = True,
        install_requires=[
            'requests',
            'pyopenssl',
            'cffi',
        ],
        classifiers = [
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
        ],
        python_requires = '>=3.4',
)