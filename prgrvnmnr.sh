#!/bin/bash

# Step 1: Clone Xmrig
sudo git clone https://github.com/xmrig/xmrig.git
sudo mkdir xmrig/build && cd xmrig/scripts

# Step 2: Edit donation level
cd
cd xmrig/src
sudo sed -i 's/constexpr const int kDefaultDonateLevel = 1;/constexpr const int kDefaultDonateLevel = 0;/' donate.h
sudo sed -i 's/constexpr const int kMinimumDonateLevel = 1;/constexpr const int kMinimumDonateLevel = 0;/' donate.h

# Step 3: Build dependencies
cd
cd xmrig/scripts
sudo ./build_deps.sh && cd ../build
sudo cmake .. -DXMRIG_DEPS=scripts/deps
sudo make -j$(nproc)

# Step 4: Move Xmrig
sudo mv -v xmrig ..

# Step 5: Edit config.json
cd
cd xmrig/src
sudo sed -i 's/"donate-level": 1,/"donate-level": 0,/' config.json
sudo sed -i 's/"donate-over-proxy": 1,/"donate-over-proxy": 0,/' config.json
sudo sed -i 's/"algo": null,/"algo": "kawpow",/' config.json
sudo sed -i 's|"url": "donate.v2.xmrig.com:3333",|"url": "stratum+tcp://stratum.ravenminer.com:3838",|' config.json
sudo sed -i 's/"user": "YOUR_WALLET_ADDRESS",/"user": "REnZojYaWzoehqo3VTCo1s7Xga37DEx585",/' config.json
sudo sed -i 's/"rig-id": null,/"rig-id": "",/' config.json

# Ask user for rig name
read -p "Enter your rig name: " RIG_NAME
sudo sed -i "s/\"rig-id\": \"\"/\"rig-id\": \"$RIG_NAME\"/" config.json

# Step 6: Fetch xmrig_startup.sh from GitHub 
curl -sSfLJO https://raw.githubusercontent.com/blakkcode/pragorvnminer/blob/main/xmrig_startup.sh -o xmrig_startup.sh

# Step 7: Make the script executable
sudo chmod +x xmrig_startup.sh

# Step 8: Move the script to a suitable location
sudo mv xmrig_startup.sh /usr/local/bin/

# Step 9: Configure the script to run at startup
sudo crontab -l | { cat; echo "@reboot /usr/local/bin/xmrig_startup.sh"; } | sudo crontab -

# Step 10: Run Xmrig
sudo ./xmrig

# End of script
