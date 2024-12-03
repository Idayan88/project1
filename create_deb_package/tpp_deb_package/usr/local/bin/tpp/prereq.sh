
if [ ! -f /etc/tpp/control ]; then
    sudo apt -y update
    sudo apt -y install python3 python3-pip
    python3 -m venv venv
    source venv/bin/activate
    sudo pip3 install -r /etc/tpp/requirements.txt 
    sudo touch /etc/tpp/control
fi
