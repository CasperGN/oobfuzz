#!/usr/bin/python3
import requests
import sys, concurrent.futures, re
from PyIntruder import PyIntruder
from datetime import datetime
from subprocess import PIPE, Popen
from os import devnull, walk
from urllib.parse import quote


class OOBFuzz():

    def __init__(self, output, threads, target, targets):
        self.output = output
        self.threads = threads
        self.targets = []

        self.paramRE = re.compile(r'(([\w]+)=([^&]+)+)')
        
        self.payloads = []
        self.excludedParams = ['submit']

        self.id = str(datetime.now()).split(':')[0].replace(' ', 'T')

        (_, _, filenames) = next(walk('./payloads/'))
        for filename in filenames:
            with open(f'./payloads/{filename}', 'r') as f:
                tmpDict = {filename[:filename.index(".")]: []}
                for payload in f:                    
                    tmpDict[filename[:filename.index(".")]].append(quote(payload.rstrip().replace('.collabxyz.', f'.{self.id}.collabxyz.')))
            self.payloads.append(tmpDict)
        
        if targets:
            try:
                with open(f'{targets}', 'r') as targetsFile:
                    for targetName in targetsFile:
                        self.targets.append(targetName.rstrip())
            except (FileNotFoundError):
                print(f'Unable to open {targets}, ensure proper permissions or that the file exists..')
                sys.exit(1)
        else:
            self.targets.append(target)

        print("Status\tLength\tTime\tHost")
        print("---------------------------------")
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.threads)) as executor:
            worker = executor.map(self.run, [target for target in self.targets])
            for result in worker:
                pass                   

    def run(self, target):

        #print(f"{str(datetime.now())} - Gathering urls for {target}")
        with open(devnull, 'w') as dn:
            process = Popen(['/usr/bin/gau', '-subs', target], stdout=PIPE, stderr=dn)
        stdout = process.communicate()[0].decode("utf-8").split("\n")
        urls = [url for url in stdout if '=' in url]
        print(f"{str(datetime.now())} - Done: Gathering urls for {target}")

        urls = list(set(urls))
        result = []
        
        for url in urls:
            print(f"{str(datetime.now())} - Fuzzing params for {url}")
            matches = self.paramRE.findall(url)

            for match in matches:
                if str(match[1]).lower() in self.excludedParams:
                    continue
                value = match[2]
                for d in self.payloads:
                    for attack, payloadList in d.items():
                        intruder = PyIntruder(redir=True, save=False, out=False, url=url.replace(value, '$'), payload=payloadList)
                        for res in intruder.run():
                            print(f'{res[0]}\t{res[1]}\t{res[2]}\t{res[3]}')
                            result.append(res)
            #print(f"{str(datetime.now())} - Done: Fuzzing params for {url}")
        return result