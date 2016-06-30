That is restfull api server to controll mulitple version of images of docker registry for openshift v3 upgrade testing. 
-------
#### Design proposal
    The docker images are stored in nfs share folder. currently, we need three nfs share directory: /var/export/registry31  /var/export/registry32 /var/export/registry33
    To share these nfs storage, the nfs folder will be mounted to directory which will be mapped to docker storage by 'docker run -v /root/data/registry32:/var/lib/registry registry:2" 
    This server will handle the mount and docker task us.  
    By default, the server only create readonly registry. To create readwrite registry, please shell script newregistry.sh
       

####To run this server in your machine, follow these steps:
##### Export an NFS Volume
For the purposes of this training, we will just demonstrate the master exporting an NFS volume for use as storage by the database. You would almost certainly not want to do this in production. If you happen to have another host with an NFS export handy, feel free to substitute that instead of setting the following up on the master, and skip the remainder of the setup steps.<br>
<br>
Ensure that nfs-utils is installed (on all systems):<br>

    yum install nfs-utils

Then, as root on the master:<br>

    Create the directory we will export:

    mkdir -p /var/export/registry31
    mkdir -p /var/export/registry32
    mkdir -p /var/export/registry33
    chown nfsnobody:nfsnobody /var/export/registry*
    chmod 777 /var/export/registry*

    Edit /etc/exports and add the following line:

    /var/export/registry31 *(rw,sync,all_squash)
    /var/export/registry32 *(rw,sync,all_squash)
    /var/export/registry33 *(rw,sync,all_squash)

    Enable and start NFS services:

    systemctl enable rpcbind nfs-server
    systemctl start rpcbind nfs-server nfs-lock 
    systemctl start nfs-idmap
    
##### Config Docker
    yum install docker
    docker pull registry:2

##### Config python virtual server
    Enable EPEL Repo
    yum install python-pip
    pip install virtualenv

##### Config this tool

    git clone https://github.com/anpingli/multiple_registry
    cd multiple_registry
    virtualenv venv
    . venv/bin/activate
    pip install flask
    pip install flask-restful

##### Run this server
    python multipleregistry.py


#### Restfull APIs
    list a registry:
       curl http://registry.example.com
    create registry:
       curl http://registry.example.com -X post -d version=31
    get a registry:
       curl http://registry.example.com/registry5000
    change registry:
       curl http://registry.example.com/registry5000 -X put -d version=32
    delete registry:
       curl http://registry.example.com/registry5000 -X delete

