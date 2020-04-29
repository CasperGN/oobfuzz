import setuptools

with open('README.md', 'r') as desc:
    long_desc = desc.read()

setuptools.setup(
        name = 'OOB Fuzz',
        version = '0.0.1',
        author = 'Casper G. Nielsen',
        author_email = 'whopsec@protonmail.com',
        description = 'Conduct OOB Fuzzing of targets with payloads towards callback server',
        long_description = long_desc,
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/Entropy-Team/recon-oobfuzz',
        packages = setuptools.find_packages(),
        classifiers = [
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
        ],
        python_requires = '>=3.4',
)
