#!/bin/bash

# Step 1: Clone the repository
git clone https://github.com/blakkcode/pragorvnminer.git
cd pragorvnminer

# Step 2: Install Python3 and pip3
sudo apt update
sudo apt install -y python3 python3-pip

# Step 3: Install Python dependencies
pip3 install -r requirements.txt

# Step 4: Run info.py to send Telegram message and generate heartbeat_startup.py
python3 info.py

# Step 5: Clone Xmrig
git clone https://github.com/xmrig/xmrig.git
cd xmrig

# Step 6: Edit donation level
cd src
sudo sed -i 's/constexpr const int kDefaultDonateLevel = 1;/constexpr const int kDefaultDonateLevel = 0;/' donate.h
sudo sed -i 's/constexpr const int kMinimumDonateLevel = 1;/constexpr const int kMinimumDonateLevel = 0;/' donate.h

# Step 7: Build dependencies
cd ..
mkdir build && cd build
sudo cmake .. -DXMRIG_DEPS=scripts/deps
sudo make -j$(nproc)

# Step 8: Move Xmrig
sudo mv -v xmrig /usr/local/bin/

# Step 9: Edit config.json
cd ..
cd src
sudo sed -i 's/"max-threads-hint": 100,/"max-threads-hint": "",/' config.json
sudo sed -i 's/"donate-level": 1,/"donate-level": 0,/' config.json
sudo sed -i 's/"donate-over-proxy": 1,/"donate-over-proxy": 0,/' config.json
sudo sed -i 's/"algo": null,/"algo": "gr",/' config.json
sudo sed -i 's/"coin": null,/"coin": "rtm",/' config.json
sudo sed -i 's|"url": "donate.v2.xmrig.com:3333",|"url": "stratum+tcps://us-west.flockpool.com:5555",|' config.json
sudo sed -i 's/"user": "YOUR_WALLET_ADDRESS",/"user": "RCuhHDkSKjVbM7ZUtRGnG4nMY4yiYcZgm7",/' config.json
sudo sed -i 's/"rig-id": null,/"rig-id": "",/' config.json

# Ask user for rig name
read -p "Enter your rig name: " RIG_NAME
sudo sed -i "s/\"rig-id\": \"\"/\"rig-id\": \"$RIG_NAME\"/" config.json
read -p "Enter CPU cores of this VPS: " THREADS
sudo sed -i "s/\"max-threads-hint\": \"\"/\"max-threads-hint\": \"$THREADS\"/" config.json

# Step 10: Move heartbeat_startup.py to a suitable location
sudo cp ../heartbeat_startup.py /usr/local/bin/

# Step 11: Configure heartbeat_startup.py to run at startup
(crontab -l ; echo "@reboot /usr/bin/python3 /usr/local/bin/heartbeat_startup.py") | crontab -

# Step 12: Fetch xmrig_startup.sh from the repository
cp ../xmrig_startup.sh /usr/local/bin/

# Step 13: Configure xmrig_startup.sh to run at startup
(crontab -l ; echo "@reboot /usr/local/bin/xmrig_startup.sh") | crontab -

# Step 14: Run Xmrig
sudo ./xmrig

# End of script
