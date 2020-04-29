#!/usr/bin/python3
# External libs
import PyIntruder
import requests


class OOBFuzz():

    def __init__(self, output, callback, target, targets):
        self.output = output
        self.callback = callback
        self.target = target
        
        if targets:
            self.targets = []
            try:
                with open(f'{targets}', 'r') as targetsFile:
                    for targetName in targetsFile:
                        self.targets.append(targetName.rstrip())
            except (FileNotFoundError):
                print(f'Unable to open {targets}, ensure proper permissions or that the file exists..')
                sys.exit(1)


    def run(self):
        print(self.output)
        print(self.callback)
        print(self.target)
        print(self.targets)


'''
#!/bin/bash
printf "%s - %s\n" "$(date)" "Starting Entropy Blind OOB Fuzzer"
#
# Set variables prior
#
date=$(date +%Y-%m-%d-%H)
loop_format="%s - %s\n"
payload=( "openredir.txt" "ssrf.txt" )
while read target; do
	mkdir -p $target
	#
	# Gather URL Endpoints from Wayback and CommonCrawler
	#
	printf "$loop_format" "$(date)" "Gathering $target URL Endpoints"
	urls=$(echo $target | gau -subs | grep -e "=" | sort -u | tee -a $target/waybackurl_params.txt)
	printf "$loop_format" "$(date)" "Collected $(wc -l $target/waybackurl_params.txt | cut -d ' ' -f1) URL Passive Parameters"
    sleep 5
	#
	# Insert Payload placeholder in all URL Endpoint Parameter Input
	#
	printf "$loop_format" "$(date)" "Dropping Payload placeholder"
	drop=$(cat $target/waybackurl_params.txt | sed -E 's,=([^&]+),=$,g' | tee -a $target/waybackurls-$payload.txt | sort -u > $target/waybackurls-sorted-$payload)
	printf "$loop_format" "$(date)" "Payload placeholder injected into all URL parameters in $target - $(wc -l $target/waybackurls-sorted-$payload | cut -d ' ' -f1) URLs will be fuzzed"
    sleep 5
	#
	# Execute and fuzz against all URL Endpoints found passively
	#
    printf "$loop_format" "$(date)" "Fuzzing against all URL Endpoints found passively for $target" 
    while read i; do   
       while read p; do
       fuzz=$(pyintruder -rs "$i" "$p" | tee -a $target/fuzz-$payload.log)
       done < $payload
    done < $target/waybackurls-sorted-$payload
    printf "$loop_format" "$(date)" "All URLs fuzzed with Blind OOB Paloads - Check Slack notifications or callbackserver for active callbacks"
done < targets
#
printf "%s - %s\n" "$(date)" "Done dropping payloads and fuzzing...."
'''