#http://blog.countableset.ch/2012/04/29/ubuntu-12-dot-04-installing-gitolite-and-gitweb/
sudo adduser --system --shell /bin/bash --gecos 'git version control' --group --disabled-password --home /home/git git
sudo su git
gl-setup admin.pub
git clone git@localhost:gitolite-admin.git
