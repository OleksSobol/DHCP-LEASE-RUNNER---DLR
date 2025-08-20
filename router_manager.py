import json
import os

import ros_api

# Configure logging
from logger import log_message, log_message_short, log_message_whole
# Get the filename of the current script
filename = os.path.basename(__file__)



class RouterManager:
    def __init__(self, config_file="config.json"):
        self.config = self.get_config(config_file)
        self.router_ip = self.config["ROUTER_IP"]
        self.username = self.config["ROUTER_USERNAME"]
        self.password = self.config["ROUTER_PASSWORD"]
        self.api_port = int(self.config["ROUTER_API_PORT"])
        self.server_name = self.config["SERVER_NAME"]
        self.router = None  # Initialize the router connection variable

    @staticmethod
    def get_config(config_file):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file)
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config

    def connect_to_router(self):
        try:
            self.router = ros_api.Api(self.router_ip, user=self.username, password=self.password, verbose=False,
                                      use_ssl=False,
                                      port=self.api_port)
            log_message_whole('info',"Connected to the router successfully.", filename)
            return True
        except Exception as e:
            log_message_whole('error',f"Error connecting to the router: {str(e)}", filename)
            return False

    def get_dynamic_dhcp_leases(self):
        try:
            if not self.router:
                if not self.connect_to_router():
                    log_message_whole('error',"Failed to connect to the router.", filename)
                    return None

            # Get all dynamic DHCP leases served by the specified server
            lease_command = (
                f"/ip/dhcp-server/lease/print where \n?dynamic=yes\n?server={self.server_name}\n=.proplist=address,mac-address,.id")
            leases_data = self.router.talk(lease_command)
            lease_command = lease_command.replace("\n", "\\n")
            log_message_whole('api', f"API call: {lease_command}", filename)

            # Extract address and mac-address from the leases
            result = [{'address': lease['address'], 'mac_address': lease['mac-address']} for lease in leases_data]

            leases_data_beautify = json.dumps(leases_data, indent=3)
            log_message('info',f"All dynamic DHCP leases [{len(leases_data)}] served by {self.server_name}:\n{leases_data_beautify}", filename)

            return leases_data

        except Exception as e:
            log_message_whole('error',f"Error during API request: {str(e)}", filename)
            return None

    def remove_dynamic_dhcp_lease(self, client_ip):
        try:
            if not self.router:
                self.connect_to_router()

            # Get the lease ID for the specified client IP
            lease_id_command = f"/ip/dhcp-server/lease/print where \n?address={client_ip}\n=.proplist=address,mac-address,.id"
            # lease_id_command = f"/ip/dhcp-server/lease/print where \n?address={client_ip}"

            lease_id_data = self.router.talk(lease_id_command)
            lease_id_command = lease_id_command.replace('\n', "\\n")
            log_message_whole('api',f"API call: {lease_id_command}", filename)

            leases_data_beautify = json.dumps(lease_id_data, indent=3)
            log_message_whole('info',f"Lease ID for the specified client IP:\n{leases_data_beautify}", filename)

            if lease_id_data:
                # Search for the correct .id based on the IP address
                for lease in lease_id_data:
                    if lease['address'] == client_ip:
                        lease_id = lease['.id']

                        # Remove the dynamic DHCP lease using the extracted ID
                        remove_command = f"/ip/dhcp-server/lease/remove\n=.id={lease_id}"
                        remove_executed = self.router.talk(remove_command)
                        remove_command = remove_command.replace("\n", "\\n")
                        log_message_whole('api',f"API call: {remove_command}", filename)
                        log_message_whole('info',f"Dynamic DHCP lease removed for client IP {client_ip}", filename)
                        break
                else:
                    log_message('warning',f"No dynamic DHCP lease found for client IP {client_ip}", filename)

            else:
                log_message('warning',f"No dynamic DHCP lease found for client IP {client_ip}", filename)

        except Exception as e:
            log_message_whole('error',f"Error during DHCP lease removal: {str(e)}", filename)