
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

curl https://pyenv.run | bash

sudo apt-get install libssl-dev libffi-dev

pyenv install 3.6.0
pyenv global 3.6.0

pip install -r requirements.txt
