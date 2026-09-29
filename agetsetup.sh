sudo apt-get update 
sudo apt install git python3-pip -y 
sudo apt remove python3-blinker* -y
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.337.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.337.0/actions-runner-linux-x64-2.337.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.337.0.tar.gz

./config.sh --url https://github.com/prateekkumawat/azure-devops-github --token ADUJ52KT4N5EXD2IXWX6CT3KXOZZQ
cd actions-runner
sudo /.svc.sh install
sudo ./svc.sh start 

sudo apt install mysql*
sudo systemctl start mysql
sudo systemctl enable mysql 
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'NewStrongPassword123';"

sudo tee "/etc/systemd/system/flask-app.service" > /dev/null <<'EOF'
[Unit]
Description=Gunicorn Flask Application
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/app
ExecStart=gunicorn --workers 2 --bind 0.0.0.0:8000 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl start flask-app.service
sudo systemctl enable flask-app.service