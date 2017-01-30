# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "bento/ubuntu-16.04"
  # XXX: Version 2.3.1 of the box was broken so I've pinned it for now.
  config.vm.box_version = "< 2.3"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "512"
  end

  config.vm.define "web01" do |web|
    web.vm.network "private_network", ip: "10.1.2.3"
  end

  config.vm.provision "ansible" do |ansible|
    ansible.inventory_path = "./playbooks/development"
    # ansible.verbose = "vvvv"
    ansible.groups = {
      "dbservers" => ["web01"],
      "webservers" => ["web01"],
    }
    ansible.playbook = "playbooks/site.yml"
    ansible.raw_arguments = [
        "--private-key=./.vagrant/machines/web01/virtualbox/private_key"
    ]
  end
end
