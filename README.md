That is restfull api server to controll mulitple version of docker registry for openshift v3 upgrade testing. 
===================
####To run this server in your machine, follow these steps:
  Install docker 
  yum install docker
  Enable EPEL Repo
  yum install python-pip
  pip install virtualenv
  git clone https://github.com/anpingli/multiple_registry
  cd multiple_registry
  virtualenv venv
  . venv/bin/activate
  pip install flask
  pip install flask-restful
  python multipleregistry.py
