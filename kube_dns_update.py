
import socket
import fcntl
import struct
import subprocess


hosts = {
    ## Base hosts
    "127.0.0.1" : "localhost",
    "10.10.110.22" : "nas-01",
    "10.10.110.32" : "nas-02",

    ## GFS hosts
    "10.10.110.71": "kube-gfs-01",
    "10.10.110.72": "kube-gfs-02",
    "10.10.110.73": "kube-gfs-03",

    ## Kube svr hosts
    "10.10.40.51" : "ks-01",
    "10.10.40.52" : "ks-02",
    "10.10.40.53" : "ks-03",
    "10.10.40.54" : "ks-05",
    "10.10.40.55" : "ks-05",
    "10.10.40.56" : "ks-06",

    ## Kube mgr hosts
    "10.10.40.61" : "km-01",
    "10.10.40.62" : "km-02",
    "10.10.40.63" : "km-03",
    "10.10.40.64" : "km-04",
    "10.10.40.65" : "km-05"
}


def get_primary_ip():
    try:
        # Get the list of network interfaces
        interfaces = socket.if_nameindex()

        for _, interface_name in interfaces:
            # Get the IP address of the interface
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                ip_address = socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', interface_name.encode('utf-8')[:15])
                )[20:24])

            # Check if the IP address is not localhost (127.0.0.1)
            if ip_address != '127.0.0.1':
                return ip_address

        return None  # No non-localhost NIC found
    except Exception as e:
        print("An error occurred:", e)
        return None


def set_hostname(new_hostname):
    try:
        # Run the hostnamectl command to set the new hostname
        subprocess.run(['sudo', 'hostnamectl', 'set-hostname', new_hostname], check=True)
        print(f"Hostname set to '{new_hostname}' successfully.")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        print("Failed to set the hostname.")
    except Exception as e:
        print("An unexpected error occurred:", e)

def generate_host_list(dns_list, host_ip):
    output = []
    for ip, host in dns_list.items():
        if ip != host_ip:
            output.append("{} {}".format(ip, host))
        else:
            output.append("{} {}".format("127.0.0.1", host))
        
    return output

def main():
    host_file = "./test_hosts"

    print("Looking up host primary IP address...")
    ip = get_primary_ip()
    if ip in hosts:
        print("Found hostname: {} matches {}".format(ip, hosts[ip]))
        set_hostname(hosts[ip])
        hl = generate_host_list(hosts, ip)
    
        addr_str = "\n".join(hl)
        print("Dumping to file: \n" + host_file)
        
        fh = open(host_file, 'a')
        fh.write("\n\n"+addr_str)
        fh.close()
    else:
        print("** ABORTING **\n Failed to get the IP address of the first network interface.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()



