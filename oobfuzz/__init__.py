#!/usr/bin/python3
import requests
import sys, concurrent.futures, re
from datetime import datetime
from subprocess import PIPE, Popen
from os import devnull, walk, path
from urllib.parse import quote
from urllib3 import disable_warnings
from random import choice
from time import sleep
from socket import gaierror
from OpenSSL import SSL
from base64 import b64encode

class OOBFuzz():

    def __init__(self, output, threads, target, targets, exclude, proxy, blocks, redir):

        disable_warnings()

        self.proxy = None
        if proxy:
            self.proxy = {"http": proxy, "https": proxy}
        self.output = output
        self.threads = threads
        self.targets = []
        self.blocks = blocks
        self.redir = redir

        if exclude:
            self.exclude = exclude.split(',')
        else:
            self.exclude = exclude

        self.paramRE = re.compile(r'(([\w]+)=([^&]+)+)')
        
        self.payloads = []
        self.excludedParams = ['submit']


        (_, _, filenames) = next(walk('./payloads/'))
        for filename in filenames:
            with open(f'./payloads/{filename}', 'r') as f:
                tmpDict = {filename[:filename.index(".")]: []}
                for payload in f:
                    tmpDict[filename[:filename.index(".")]].append(quote(payload.rstrip()))
            self.payloads.append(tmpDict)

        self.useragents = []
        pwd = path.dirname(path.realpath(__file__))
        with open(f'{pwd}/data/user-agents.txt', 'r') as agents:
            for useragent in agents:
                self.useragents.append(useragent.rstrip())

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
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            worker = executor.map(self.run, [target for target in self.targets])
            for result in worker:
                pass                   

    def run(self, target):

        with open(devnull, 'w') as dn:
            process = Popen(['/usr/bin/gau', '-subs', target], stdout=PIPE, stderr=dn)
        stdout = process.communicate()[0].decode("utf-8").split("\n")
        urls = [url for url in stdout if '=' in url]

        urls = list(set(urls))
        result = []
        
        for baseurl in urls:
            matches = self.paramRE.findall(baseurl)

            for match in matches:
                if str(match[1]).lower() in self.excludedParams:
                    continue
                value = match[2]
                for d in self.payloads:
                    for attack, payloadList in d.items():
                        for payload in payloadList:
                            if self.blocks == 0:
                                # We're out of luck, exit
                                break
                            user_agent = choice(self.useragents)
                            headers = {'User-Agent': user_agent}
                            payload = payload.strip('\n')
                            url = baseurl.replace(value, payload)
                            if '~~ID_BASE64~~' in payload:
                                url = url.replace('~~ID_BASE64~~', b64encode(bytes(url, encoding='utf-8')).decode('utf-8'))
                            try:
                                r = requests.get(url, headers=headers, allow_redirects=self.redir, proxies=self.proxy, verify=False)
                                # Here we attempt to circumvent rate limit and/or temporary blocks on our IP
                                # Often when 403 og 429 is returned because of a block a small html document
                                # is returned with that is len =~ 200
                                if r.status_code == 403 and len(r.content) < 200 or r.status_code == 429 and len(r.content) < 200:
                                    # Testing has shown that at least blocks from Akamai last around 2 minutes
                                    print(f"{str(datetime.now())} - Request was possibly blocked by WAF: Sleeping thread for 140 seconds for {self.target}")
                                    sleep(140)
                                    r = requests.get(url, headers=headers, allow_redirects=self.redir, proxies=self.proxy, verify=False)
                                    if r.status_code == 403 and len(r.content) < 200 or r.status_code == 429 and len(r.content) < 200:
                                        # At this point we just continue
                                        self.blocks -= 1
                                        continue
                            except (SSL.SysCallError, gaierror):
                                continue
                            result.append([r.status_code, len(r.content), str(r.elapsed.total_seconds()*1000)[:7], url])
                            print(f'{r.status_code}\t{len(r.content)}\t{str(r.elapsed.total_seconds()*1000)[:7]}\t{url}')
                            if r.status_code == 404:
                                # The url/endpoint is not working, lets just break out
                                break
                            '''if self.save_responses and len(r.content) != 0:
                                try:
                                    with open(f'{self.output_dir}/{str(datetime.now()).replace(" ", "T").replace(":", "-").split(".")[0]}-{self.payloaddata.index(payload)}', 'w') as f:
                                        f.write(f'{url}\n\n{r.status_code}\n\n{r.content}')
                                except:
                                    print(f'Error: could not write file {self.output_dir}/{str(datetime.now()).replace(" ", "T").replace(":", "-").split(".")[0]}-{self.payloaddata.index(payload)}')'''
                            sleep(0.5)                
        return result