# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrant configuration standard version 2
Vagrant.configure("2") do |config|
  #config.vm.box = "bento/ubuntu-20.04"
  config.vm.box = "peru/ubuntu-20.04-desktop-amd64"

  #current folder will be shared in the vagrant VM
  config.vm.synced_folder ".", "/home/vagrant/shared"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = true
    vb.memory = "4096"
    vb.cpus = 4
    vb.customize ['modifyvm', :id, '--graphicscontroller', 'vmsvga']
    vb.customize ['modifyvm', :id, '--accelerate3d', 'on']
    vb.customize ['modifyvm', :id, '--vram', '128']
    vb.customize ['modifyvm', :id, '--vrde', 'off']
    #vb.customize ['modifyvm', :id, '--audiocontroller', 'hda']
    vb.customize ['modifyvm', :id, '--clipboard', 'bidirectional']
    vb.customize ['modifyvm', :id, '--draganddrop', 'bidirectional']
    # Make the DNS calls be resolved on host
    #vb.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y vim tmux flex bison build-essential libtk-img iperf
    ln -s /usr/bin/python3 /usr/bin/python
    cd /home/vagrant/shared/pimd-dense-2.1.0
  	./autogen.sh
	./configure --prefix=/usr/local
 	make
 	make install
    cd /home/vagrant/shared/smcroute-2.5.6
 	./autogen.sh
 	./configure --prefix=/usr/local
 	make
 	make install
 	cd /home/vagrant/shared
 	mkdir -p /home/vagrant/.core/myservices
	cp *.py /home/vagrant/.core/myservices
    chown -R vagrant:vagrant /home/vagrant
    cp mcsend /usr/local/bin
    cp mcrecv /usr/local/bin
  SHELL

end
