from scapy.all import sniff, IP, TCP, Raw
import ssl
import re

# Function to detect if a connection is HTTP (not HTTPS)
def is_http(packet):
    # If the packet is not encrypted (TCP port 80 usually means HTTP)
    if packet.haslayer(TCP) and packet[TCP].dport == 80:
        return True
    return False

# Function to simulate HSTS/SSL/HTTPS stripping
def ssl_https_stripping(packet):
    if packet.haslayer(Raw):
        payload = packet[Raw].load
        # Check if the payload contains an HTTP response
        if b"HTTP" in payload and b"200 OK" in payload:
            http_data = payload.decode(errors='ignore')
            # Strip out SSL or HTTPS-specific data and print it as readable text
            print(f"HTTP Response Detected (Stripped):\n{http_data}")
            return True
    return False

def packet_callback(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        proto = packet[IP].proto

        # Check for HTTP traffic (port 80) and handle it
        if is_http(packet):
            print(f"Source IP: {ip_src}, Destination IP: {ip_dst}, Protocol: HTTP")
            
            # Extract payload and print if it's human-readable
            if Raw in packet:
                payload = packet[Raw].load
                print(f"Payload: {payload.decode(errors='ignore')}")
            else:
                print("No HTTP Payload Detected")

        # Check for weak HTTPS traffic (port 443, but may have vulnerabilities)
        elif packet.haslayer(TCP) and packet[TCP].dport == 443:
            print(f"Source IP: {ip_src}, Destination IP: {ip_dst}, Protocol: HTTPS (Weak SSL/HTTPS Stripping Attempt)")
            
            # Try to strip SSL/TLS (only if we detect HTTP over HTTPS port)
            if ssl_https_stripping(packet):
                return  # Data already stripped and printed
            else:
                print("Unable to decrypt HTTPS. No weak SSL detected.")

        print('-' * 50)  # Just to separate each packet's data for better readability

def start_sniffing():
    print("Starting packet sniffing... Press CTRL+C to stop.")
    # Capture packets indefinitely, looking for HTTP (port 80) and HTTPS (port 443)
    sniff(prn=packet_callback, store=0, filter="ip", count=0)  # 'count=0' means infinite capture

if __name__ == "__main__":
    start_sniffing()
