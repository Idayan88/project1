if [ ! -f /etc/tpp/control ]; then
    sudo apt -y update
    sudo apt -y install python3 python3-pip
    sudo pip3 install -r /etc/tpp/requirements.txt --break-system-packages # use --break-system-packages to install packages globally    
    sudo touch /etc/tpp/control
fi
