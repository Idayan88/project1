#!/bin/bash
git clone -b Denis_Liveness_ssl https://github.com/Idayan88/project1.git
echo "The clone op Done"
cd project1/create_deb_package
echo "cd done"
dpkg-deb --build tpp_deb_package
mv tpp_deb_package.deb tpp.deb
echo "tpp.deb package is ready."
sudo apt -y install ./tpp.deb