import socket
import netifaces
import scapy
import scapy.all as scapy
import re

# Definition for making calculating cidr notations
def subnet_mask_to_cidr(netmask):
        binary_str = ""
        octets = netmask.split(".")
        for octet in octets: # Goes through each octet (up to 8 bits)
                binary_str += bin(int(octet))[2:].zfill(8)
        cidr = 0
        for bit in binary_str:
                if bit == "1": # If the current bit is 1, add one to CIDR. I think this formula works?
                        cidr += 1
        return cidr

ip = socket.gethostbyname(socket.gethostname())
print("Loopback IP: ", ip) # I have no idea why i'm keeping this, its basically just here to be here

interfaces = netifaces.interfaces()

wlan_interface = None # Checks if wlan is present in the ifconfig menu (not literally, but just for visualisation)
for iface in interfaces:
        if "wlan" in iface:
                wlan_interface = iface
                break

if wlan_interface:
        addrs = netifaces.ifaddresses(wlan_interface)
        w_ip = addrs[netifaces.AF_INET][0]["addr"]
        iface_addrs = addrs[netifaces.AF_INET]
        iface_dict = iface_addrs[0]
        netmask = iface_dict.get('netmask')
        print("Wlan0 Netmask: ", netmask)
        cidr = subnet_mask_to_cidr(netmask) # Using the CIDR formula from earler
        print("CIDR: ", cidr)
        print("Wlan0 IP: ", w_ip)
else:
        print("No WLAN Interface Detected.")

octets = w_ip.split(".") # Splits up octets so we can edit it like a dict

octets[-1] = "0" # Sets last octet to zero, so we can use it later


w_ip = ".".join(octets) # Joins it back together

target = (str(w_ip) + "/" + str(cidr))
print("==============================")
print("|| TARGET: ", target + " ||")
print("==============================")

while True:
        pattern = r'^(\d{1,3}\.){3}\d{1,3}/([1-2]?[0-9]|3[0-2])$'
        if re.match(pattern, target):
                print("XXXXXXXXXXXXXXXXXXXX")
                print("XXX Target Valid XXX")
                print("XXXXXXXXXXXXXXXXXXXX")
                arp_result = scapy.arping(target)
        break
else:
        print("No WLAN Interface to hit.")
