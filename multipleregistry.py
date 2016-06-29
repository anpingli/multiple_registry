from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
import commands
import re

APP = Flask(__name__)
API = Api(APP)

TODOS = {}
REG_DATA_DIR="/root/data"


def find_a_nfs_folder(version):
   if version==31:
       reg_share_dir="/var/export/registry31"
   if version==32:
        reg_share_dir="/var/export/registry32"
   if version==33:
       reg_share_dir="/var/export/registry33"
   return reg_share_dir

def find_a_port():
    selected_port="5000"
    avaible=False

    reg_dict=list_registy("ancestor=registry:2")

    for i in range(5000, 6000):
        cur_port=str(i)
        avaible=True
        for key in reg_dict.keys():
            if cur_port == reg_dict[key]["port"]:
                avaible=False
                break
        if avaible==True:
            selected_port=cur_port
            break
    print "selected port->" + selected_port
    return selected_port

def list_registy(filter_str):
    rows=exec_shell_cmd("docker ps -f '"+filter_str+"'").split('\n')
    top_dict={}
    for j in range(1,len(rows)):
        print str(j)+"->j->"+rows[j]
        cols=re.split("\s{2,}",rows[j])
        m = re.search(r':(.*)->5000', cols[5])
        port="unknow"
        if m:
            port=m.group(1) 
        tmp_dict={"name": cols[6],"id":cols[0],"port":port}
        #get the mount info
        mount_info = exec_shell_cmd("mount |grep "+cols[6])
        n = re.search(r'registry(\d+)\s+', mount_info)
        version="unkown"
        if n:
             version= n.group(1)
        tmp_dict["version"]=version
        top_dict[j]=tmp_dict
    return top_dict

def list_registy_by_name(reg_name):
    return  list_registy("name="+reg_name)


def exec_shell_cmd(cmd_str):
    print "exec:"+cmd_str
    (status, output)=commands.getstatusoutput(cmd_str)
    print output
    return output


class Registry_List(Resource):
    def get(self):
        return list_registy("ancestor=registry:2")

    def post(self):
        version = request.form['version']
        parser = reqparse.RequestParser()
        parser.add_argument('version', type=int, help='version should be 31 32 or 33')
        args = parser.parse_args()
        reg_port=find_a_port()
        reg_share_dir=find_a_nfs_folder(args['version'])
        reg_name="registry" + reg_port
        reg_volume=REG_DATA_DIR+"/"+reg_name
        exec_shell_cmd("mkdir -p "+reg_volume)
        exec_shell_cmd("mount 127.0.0.1:"+reg_share_dir+" "+reg_volume)
        exec_shell_cmd("docker run -d -p "+reg_port+":5000 --restart=always --name "+reg_name+" -v "+reg_volume+":/var/lib/registry:ro registry:2")
        reg_info=list_registy_by_name(reg_name)
        return reg_info


class Registry(Resource):
    def get(self, todo_id):
        reg_name=todo_id
        reg_info=list_registy_by_name(reg_name)
        return reg_info

    def put(self, todo_id):
        version = request.form['version']
        parser = reqparse.RequestParser()
        parser.add_argument('version', type=int, help='version should be 31 32 or 33')
        args = parser.parse_args()
        reg_name=todo_id
        reg_volume=REG_DATA_DIR+"/"+reg_name
        reg_port=reg_name[8:13]
        reg_share_dir=find_a_nfs_folder(args['version'])

        exec_shell_cmd("umount "+reg_volume)
        exec_shell_cmd("docker rm -f -v "+reg_name)
        exec_shell_cmd("mount 127.0.0.1:"+reg_share_dir+" "+reg_volume)
        exec_shell_cmd("docker run -d -p "+reg_port+":5000 --restart=always --name "+reg_name+" -v "+reg_volume+":/var/lib/registry registry:2")
        reg_info=list_registy_by_name(reg_name)
        return reg_info

    def delete(self, todo_id):
        reg_name=todo_id
        reg_port=reg_name[8:13]
        reg_volume=REG_DATA_DIR+"/"+reg_name
        exec_shell_cmd("umount "+reg_volume)
        return exec_shell_cmd("docker rm -f -v "+reg_name)


API.add_resource(Registry_List, '/', '/registry')
API.add_resource(Registry, '/registry/<todo_id>')

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=80, debug=True) 
