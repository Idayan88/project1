#!/bin/bash
git clone -b Denis_Liveness_ssl https://github.com/Idayan88/project1.git
cd int0924/system/create_deb_package
dpkg-deb --build systeminfo_deb_package
mv systeminfo_deb_package.deb systeminfo.deb
echo "systeminfo.deb package is ready."
sudo apt -y install ./systeminfo.deb