#!/bin/bash
git clone -b Denis_Liveness_ssl https://github.com/Idayan88/project1.git
echo "The clone op Done"
cd project1/create_deb_package
echo "cd done"
chmod 0775 /root/project1/create_deb_package/tpp_deb_package/DEBIAN/postinst
chmod 0775 /root/project1/create_deb_package/tpp_deb_package/DEBIAN/prerm
dpkg-deb --build tpp_deb_package
mv tpp_deb_package.deb tpp.deb
echo "tpp.deb package is ready."
sudo apt -y install ./tpp.deb