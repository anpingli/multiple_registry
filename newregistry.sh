version=${1:-31}
port=${2:-5000}
reg_name="registry${port}"
share_dir="127.0.0.1:/var/export/$reg_name"
volume_dir="/root/data/${reg_name}"
mkdir -p $volume_dir
mount $share_dir $volume_dir
docker run -d -p $port:5000 --restart=always --name $reg_name -v $volume_dir:/var/lib/registry registry:2
