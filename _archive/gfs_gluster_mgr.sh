#!/bin/bash

gluster peer probe kube-gfs-01
gluster peer probe kube-gfs-02
gluster peer probe kube-gfs-03

gluster volume create kube-mgr replica 3 kube-gfs-01:/gfs/kube-mgr kube-gfs-02:/gfs/kube-mgr kube-gfs-03:/gfs/kube-mgr force
gluster volume start kube-mgr

gluster volume bitrot  kube-mgr enable
gluster volume bitrot  kube-mgr scrub-frequency daily
gluster volume heal  kube-mgr enable
#gluster volume set  kube-mgr auth.allow 10.10.110.81,10.10.110.82,10.10.110.83,10.10.110.84,10.10.110.85,10.10.110.86

# gluster volume create kube-mgr replica 3 gfs-01:/gfs/kube-mgr gfs-02:/gfs/kube-mgr gfs-03:/gfs/kube-mgr
# gluster volume start kube-mgr

# gluster volume bitrot  kube-mgr enable
# gluster volume bitrot  kube-mgr scrub-frequency daily
# gluster volume heal  kube-mgr enable

# gluster volume set kube-mgr auth.allow 10.10.110.51,10.10.110.52,10.10.110.53