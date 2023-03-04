#!/usr/bin/env bash


# split installation into two parts
#  - part 1 - build VM and do initial provisioning; because PATH isn't immediately
#             available, a logout is required and installation continues in part 2
#  - part 2 - complete the remaining installation

# part 1 install
if [ ! -f ./release-7.5.2.tar.gz ]; then
    wget https://github.com/coreemu/core/archive/refs/tags/release-7.5.2.tar.gz
    tar -zxf release-7.5.2.tar.gz
fi
if [ ! -f pimd-dense-2.1.0.tar.gz ]; then
    wget https://github.com/troglobit/pimd-dense/releases/download/2.1.0/pimd-dense-2.1.0.tar.gz
    tar -zxf pimd-dense-2.1.0.tar.gz
fi
if [ ! -f smcroute-2.5.6.tar.gz ]; then
    wget https://github.com/troglobit/smcroute/releases/download/2.5.6/smcroute-2.5.6.tar.gz
    tar -zxf smcroute-2.5.6.tar.gz
fi

vagrant up

# part 2 install
vagrant ssh -c \
    "cd shared/core-release-7.5.2; \
    ./install.sh; \
    sudo sed -i 's/#custom\_services\_dir/custom\_services\_dir/g' /etc/core/core.conf; \
    sudo sed -i 's/username/vagrant/g' /etc/core/core.conf; \
    sudo systemctl enable core-daemon; \
    sudo systemctl start core-daemon; \
    "
