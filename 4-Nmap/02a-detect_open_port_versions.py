"""
Service version detection (-sV) and executing default NSE (Nmap Scripting Engine) scripts (--script=default).
The purpose of the code is to scan a specified target (given as an IP address or range) and provide detailed 
information about the service versions running on the open ports of the target, along with the results of any
executed NSE scripts.
"""
"""
Détection de version du service (-sV) et exécution de scripts NSE (Nmap Scripting Engine) par défaut (--script=default).
Le but du code est d'analyser une cible spécifiée (donnée sous forme d'adresse IP ou de plage) et de fournir des informations détaillées,
des informations sur les versions de service exécutées sur les ports ouverts de la cible.
"""


import nmap

nm = nmap.PortScanner()

def advanced_scan(target):
        # Perform an advanced scan with service version detection (-sV) and executing default NSE scripts (--script=default)
        nm.scan(hosts=target, arguments='-sV --script=default')

        # Iterate through all discovered hosts
        for host in nm.all_hosts():
            # Print detailed results for each host
            print(f"Detailed results for {host}:")
            
            # Print service versions for open TCP (Transmission Control Protocol) ports
            print(f"Service versions: {nm[host]['tcp'].items()}")

if __name__ == "__main__":
    # Create an instance of the NmapScanner class with the target IP address '192.168.1.1' # using localhost for testing
    target = '127.0.0.1'
    # target = '45.33.32.156'
    advanced_scan(target)



