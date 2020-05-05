import argparse, sys, re
from oobfuzz import OOBFuzz

parser = argparse.ArgumentParser(prog='OOBFuzz')
parser.add_argument('--output', type=str, help='File to output result to')
parser.add_argument('--threads', type=int, help='Number of threads to fuzz (default: 5)')
parser.add_argument('--target', type=str, help='Single target to run against')
parser.add_argument('--targets', type=str, help='File with newline seperator including several targets')
parser.add_argument('--exclude', type=str, help='String of response codes seperated by "," (example 404,401,403) to exclude from printing')
parser.add_argument('--proxy', type=str, help='Proxy to route through (example "http://localhost:8080")')
parser.add_argument('--blocks', type=int, help='Amount of blocks registered to exit (default: 5). This means that if 5 blocks are registered the fuzzer will exit')
parser.add_argument('--redir', help='Allow HTTP redirects', action="store_true")
parser.add_argument('--urls', type=str, help='file with newline seperator including endpoints. This will skip fetch through Gau')
parser.add_argument('--stdin-targets', nargs=argparse.REMAINDER)
parser.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin)



if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

if not sys.stdin.isatty():
    stdin_targets = parser.parse_args().stdin.read().splitlines()
else:
    stdin_targets = None


if args.proxy:
    proxyMatch = re.findall('(http(?:s)?://[a-zA-Z0-9\.-]+:[\d]{1,5})', args.proxy)
    if len(proxyMatch) <= 0:
        parser.print_help(sys.stderr)
        exit(1)

output = args.output if args.output else None
threads = args.threads if args.threads else 5
target = args.target if args.target else None
targets = args.targets if args.targets else None
exclude = args.exclude if args.exclude else None
proxy = args.proxy if args.proxy else None
blocks = args.blocks if args.blocks else 5
redir = args.redir if args.redir else False
urls = args.urls if args.urls else None

oobfuzz = OOBFuzz(output, threads, target, targets, exclude, proxy, blocks, redir, urls, stdin_targets)