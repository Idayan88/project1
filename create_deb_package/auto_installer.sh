#!/bin/bash
git clone -b Denis_Liveness_ssl https://github.com/Idayan88/project1.git
cd /home/ubuntu/project1/create_deb_package
dpkg-deb --build tpp_deb_package
mv tpp_deb_package.deb tpp.deb
echo "tpp.deb package is ready."
sudo apt -y install ./tpp.deb