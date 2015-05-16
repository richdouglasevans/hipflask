# -*- mode: ruby -*-

require File.join(File.dirname(__FILE__), 'vagrant/vagrant')

Vagrant::Config.run do |config|

  config.vm.box = "base"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.forward_port 27017, 27017  # MongoDB

  config.vm.provision :shell do |shell|
    vagrant_shell_scripts_configure( shell, File.dirname(__FILE__), 'vagrant/provision.sh' )
  end

  config.vm.share_folder "stuff", "/home/vagrant/shared", "vagrant/shared", :create=>true
end
