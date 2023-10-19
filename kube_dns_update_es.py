
import socket
import fcntl
import struct
import subprocess

HOSTS_FILE = "/etc/hosts"

HOSTS_LIST = {
    ## Base hosts
    "127.0.0.1" : "localhost",
    "10.10.110.22" : "nas-01",
    "10.10.110.32" : "nas-02",

    ## Kube svr hosts
    "10.50.100.61" : "kes-01",

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

    print("Looking up host primary IP address...")
    ip = get_primary_ip()
    if ip in HOSTS_LIST:
        print("Found hostname: {} matches {}".format(ip, HOSTS_LIST[ip]))
        set_hostname(HOSTS_LIST[ip])
        hl = generate_host_list(HOSTS_LIST, ip)
    
        addr_str = "\n".join(hl)
        print("Dumping to file: \n" + HOSTS_FILE)
        
        fh = open(HOSTS_FILE, 'a')
        fh.write("\n\n"+addr_str)
        fh.close()
    else:
        print("** ABORTING **\n Failed to get the IP address of the first network interface.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()



