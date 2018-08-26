# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "bento/ubuntu-18.04"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
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
