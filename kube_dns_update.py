from pathlib import Path
import platform
from pprint import pprint


class HostBase():
    def host_addresses(self):
        return [
                "127.0.0.1 localhost",
                "10.10.110.22 nas-01",
                "10.10.110.32 nas-02"
        ]

class KubeHosts(HostBase):

    def host_addresses(self, host):
        host_list = super().host_addresses()

        hosts = [
                 "10.10.110.71 kube-gfs-01",
                 "10.10.110.72 kube-gfs-02",
                 "10.10.110.73 kube-gfs-03",

                 "10.10.40.81 ks-01",
                 "10.10.40.82 ks-02",
                 "10.10.40.83 ks-03",
                 "10.10.40.84 ks-05",
                 "10.10.40.85 ks-05",
                 "10.10.40.86 ks-06",

                 "10.10.40.91 km-01"
        ]

        for v in hosts:
            if host not in v:
                print("Adding: {}".format(v))
                host_list.append(v)
            else:
                entry = "127.0.1.1 " + host
                print("Adding local: {}".format(entry))
                host_list.append(entry)

        return host_list


hostname = platform.node()
host_file = "/etc/hosts"

print("Current hostname is: " + hostname)

addr_list = KubeHosts().host_addresses(hostname)
addr_str = "\n".join(addr_list)
print("Dumping to file: \n" + host_file)

fh = open(host_file, 'a')
fh.write("\n\n"+addr_str)
fh.close()
print("\n\n"+addr_str)
