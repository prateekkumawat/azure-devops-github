sudo apt-get update 
sudo apt install git python3-pip -y 
sudo apt remove python3-blinker* -y
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.337.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.337.0/actions-runner-linux-x64-2.337.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.337.0.tar.gz

./config.sh --url https://github.com/prateekkumawat/azure-devops-github --token ADUJ52KT4N5EXD2IXWX6CT3KXOZZQ
cd action-runner
sudo /.svc.sh install
sudo ./svc.sh start 