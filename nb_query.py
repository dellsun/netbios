import socket


# This is the query
# *<00><00><00><00><00><00><00><00><00><00><00><00><00><00><00>
def make_packet():
    pkt = '\x00\x00'   # Doesnt matter, we are making it.
    pkt += "\x00\x00"  # Flags = None
    pkt +="\x00\x01"   # Questions = 1
    pkt +="\x00\x00"   # Answer RRs = 0
    pkt +="\x00\x00"   # Authority RRs = 0
    pkt +="\x00\x00"   # Additional RRs = 0
    pkt +="\x20\x43\x4b\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41" # Our query split on 2 lines
    pkt +="\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x00" # For readability
    pkt +="\x00\x21"   # Type = NBSTAT = 33
    pkt +="\x00\x01"   # Class = IN
    return pkt

sport = 3000
dport = 137
to_ip = "192.168.1.1"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', sport))

data = make_packet()
s.sendto(data, (to_ip, dport))
