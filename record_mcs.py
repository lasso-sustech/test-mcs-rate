#!/usr/bin/env python3
import re
import subprocess as sp
import sys
import time

SHELL_RUN = lambda x: sp.run(x, stdout=sp.PIPE, stderr=sp.PIPE, check=True, shell=True)
TX_RATE_FILTER = re.compile('.*tx bitrate:\s*(\S*)\s*MBit.*')
TX_BYTES_FILTER = re.compile('.*tx bytes:\s*(.*).*')

INTERVAL = 0.001#s
MAX_TIME = int(sys.argv[1])#s

def get_tx_stat():
    iw_output = SHELL_RUN('iw dev wlp0s20f3 station dump').stdout.decode()
    tx_rate    = float( TX_RATE_FILTER.findall(iw_output)[0] )
    tx_bytes = int( TX_BYTES_FILTER.findall(iw_output)[0] )
    return (tx_rate, tx_bytes)


_, last_bytes = get_tx_stat()
init_time = time.time()
results = list()

while time.time() - init_time < MAX_TIME:
    tx_rate, tx_bytes = get_tx_stat()
    if tx_bytes > last_bytes:
        last_bytes = tx_bytes
        results.append( tx_rate )
    time.sleep(INTERVAL)

print( sum(results) / len(results) )
