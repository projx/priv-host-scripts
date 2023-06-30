import sys, platform
from pathlib import Path
from pprint import pprint

mount_points = {
    "cntrs-svr":
        {"remote_path":"nas-01:/volume1/CNTRS-SVR/", "local_path":"/store/nas_data", "options":"nfs nfsvers=4,rw,auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0" },
    "downloads":
        {"remote_path":"nas-01:/volume2/Downloads/", "local_path":"/store/downloads", "options":"nfs nfsvers=4,rw,auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0"},
    "tv":
        {"remote_path":"nas-01:/volume2/TV/", "local_path":"/store/tv", "options":"nfs nfsvers=4,rw,auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0"},
    "movies":
        {"remote_path":"nas-01:/volume2/Movies/","local_path":"/store/movies","options":"nfs nfsvers=4,rw,auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0"},
    "books":
        {"remote_path":"nas-01:/volume2/Books/","local_path":"/store/books","options":"nfs nfsvers=4,rw,auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0"},
    "youtube":
        {"remote_path":"nas-01:/volume2/YouTube/","local_path":"/store/youtube","options":"nfs nfsvers=4,rw,auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0"},
    "music":
        {"remote_path":"as-01:/volume2/Music/", "local_path":"/store/music", "options":"nfs nfsvers=4,rw,auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0"},
    "gfs":
        {"remote_path": "{}:/kube-svr/", "local_path": "/store/gfs", "options": "glusterfs defaults,_netdev,backupvolfile-server={},transport=tcp  0 0"}
}


gfs_mount = "{}:/kube-svr/ /store/gfs glusterfs defaults,_netdev,backupvolfile-server={},transport=tcp  0 0"
gfs_hosts = {
    "ks-01": {"PRIMARY":"kube-gfs-03", "BACKUP":"kube-gfs-02"},
    "ks-02": {"PRIMARY":"kube-gfs-02", "BACKUP":"kube-gfs-01"},
    "ks-03": {"PRIMARY":"kube-gfs-01", "BACKUP":"kube-gfs-03"},
    "ks-04": {"PRIMARY":"kube-gfs-03", "BACKUP":"kube-gfs-02"},
    "ks-05": {"PRIMARY":"kube-gfs-02", "BACKUP":"kube-gfs-01"},
    "ks-06": {"PRIMARY":"kube-gfs-01", "BACKUP":"kube-gfs-03"}
}

def get_gfs_primary(hostname, which):
    return gfs_hosts[hostname][which]
    # return gfs_mount.format(gfs_hosts[hostname]["PRIMARY"], gfs_hosts[hostname]["BACKUP"])

def get_gfs_backup(hostname):
    return gfs_hosts[hostname]["BACKUP"]

def make_mount_point(base_dir, mount_dir):
        ddir = base_dir + mount_dir
        Path(ddir).mkdir(parents=True, exist_ok=True)


### Prod
hostname = platform.node()
stab_path = "/etc/fstab"
base_dir = ""

print(hostname)
print("******************************************")
#### Test
if "MBP14.local" in hostname:
    print("Currently running on MBP14... Setting up test environment")
    hostname = "ks-01"
    stab_path = "./test/fstab"
    base_dir = "./test/"


mount_points["gfs"]["remote_path"] = mount_points["gfs"]["remote_path"].format( get_gfs_primary(hostname, "PRIMARY"))
mount_points["gfs"]["options"] =mount_points["gfs"]["options"].format(get_gfs_primary(hostname, "BACKUP"))

mount_list = []
for key, mount in mount_points.items():
    print("{} - creating path {}".format(key, mount["local_path"]))
    make_mount_point(base_dir, mount["local_path"])
    merged = mount["remote_path"] + "     " + mount["local_path"] + "      " + mount["options"]
    print("{} - Inserting into /etc/fstab: {}".format(key, merged))
    mount_list.append(merged)

fh = open(stab_path, 'a')
fh.write("\n".join(mount_list))
fh.close()

