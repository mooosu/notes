udo adduser --system --shell /bin/bash --gecos 'git version control' --group --disabled-password --home /home/git git
sudo su git
gl-setup admin.pub
git clone git@localhost:gitolite-admin.git
