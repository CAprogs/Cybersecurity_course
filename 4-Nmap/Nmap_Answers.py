import nmap
import json
import socket

class MyScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()

    def simple_discovery_scan(self, target_ips, mode="default"):
        self.nm.scan(hosts=target_ips, arguments='-sn')

        for host in self.nm.all_hosts():
            state = "up"
            hostname = socket.gethostbyaddr(host)[0].__str__()
            if mode == "default":
                print(f"Host: {host} is {state}")
            elif mode == "up-only":
                return hostname, state


    def detailed_port_scan(self, target_ip_port, mode="default"):
        self.nm.scan(hosts=target_ip_port, arguments='-p 1-1000 -sS', sudo=True)
        if target_ip_port in self.nm.all_hosts():
            try:
                if self.nm[target_ip_port]['tcp']:
                    open_ports = self.nm[target_ip_port]['tcp'].keys()
                    if mode == "default":
                        print(f"Open ports for {target_ip_port}: {', '.join(map(str, open_ports))}")
                    elif mode == "up-only":
                        ports = {}
                        print(f"Port Status:\nHost: {target_ip_port}")
                        for port in map(int, open_ports):
                            print(f" Port {port}: open")
                            ports[port] = "open"
                        return ports
                else:
                    print(f"No open ports found for {target_ip_port}")
            except KeyError as e:
                print(f"KeyError : {e}\nHost: {target_ip_port}")
        else:
            print(f"Target IP {target_ip_port} not found in scan results.")


    def service_and_NSE_scan(self, target_ip):
        datas = {}
        # Perform an advanced scan with service version detection (-sV) and executing default NSE scripts (--script=default)
        self.nm.scan(hosts=target_ip, arguments='-sV --script=default')

        # Iterate through all discovered hosts
        for host in self.nm.all_hosts():
            datas[host] = {"scripts": {}}
            
            # Print service versions for open TCP (Transmission Control Protocol) ports
            service_versions = self.nm[host]['tcp'].items().mapping.copy()
            datas[host]["services"] = service_versions

            # Check if NSE scripts results are available for the host
            if 'scripts' in self.nm[host]:
                for script_id, script_output in self.nm[host]['scripts'].items():
                    datas[host]["scripts"][script_id] = script_output
            else:
                datas[host]["scripts"] = None
        return datas


def save_scan_results(datas, target_ip, indent=2):
    if "/" in target_ip:
        target_ip = target_ip.replace("/", "_")
    filename = f"scan_results_{target_ip}.json"
    with open(filename, "w") as file:
        json.dump(datas, file, indent=indent)
        print(f"Scan results saved to:{filename}")


# Exercice 1
def exo_1():
    target_ips = "192.168.86.185 192.168.86.186 192.168.86.187"
    target_ip_port = "192.168.86.186"
    scanner = MyScanner()
    scanner.simple_discovery_scan(target_ips)
    scanner.detailed_port_scan(target_ip_port)


# Exercice 2
def exo_2():
    while True:
        try:
            target_ip = input("Enter target IP address or range (Ctrl+C to cancel):")
            scanner = MyScanner()
            datas = scanner.service_and_NSE_scan(target_ip)
            save_scan_results(datas, target_ip, 4)
        except KeyboardInterrupt:
            print("\nScan canceled. Exiting... ")
            break


# Exercice 3
def exo_3():
    datas = {}
    scanner = MyScanner()
    target_ip = input("Enter target IP address or range (Ctrl+C to exit):")
    hostname, state = scanner.simple_discovery_scan(target_ip, mode="up-only")
    ports = scanner.detailed_port_scan(target_ip, mode="up-only")
    datas[target_ip] = {"hostname": hostname, "state": state, "ports": ports}
    save_scan_results(datas, target_ip, 3)


if __name__ == "__main__":
    exo_1()  # enter your own IP addresses in target_ips and target_ip_port
    #exo_2() # try 8.8.8.8
    #exo_3() # try 8.8.8.8
