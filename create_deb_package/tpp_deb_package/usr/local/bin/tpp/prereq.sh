
if [ ! -f /etc/tpp/control ]; then
    sudo apt -y update
    sudo apt -y install python3 python3-pip
    cd /usr/local/bin/tpp
    apt -y install python3.12-venv
    python3 -m venv /usr/local/bin/tpp/venv
    source /usr/local/bin/tpp/venv/bin/activate
    sudo pip3 install -r /etc/tpp/requirements.txt 
    sudo touch /etc/tpp/control
fi
