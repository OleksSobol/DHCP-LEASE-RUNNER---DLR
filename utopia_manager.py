import json
import requests
import os


# Configure logging
from logger import log_message, log_message_short, log_message_whole
# Get the filename of the current script
filename = os.path.basename(__file__)


class UtopiaManager:
    def __init__(self, config_file="config.json"):
        self.config = self.get_config(config_file)
        self.api_key = self.config["UTOPIA_API_KEY"]

    @staticmethod
    def get_config(config_file):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file)
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config

    def get_utopia_site_id_by_mac(self, mac_address):
        JSON_REQUEST = {
            "apikey": self.api_key,
            "mac": mac_address,
        }

        response = requests.post("https://api.utopiafiber.com/spquery/macsearch", data=json.dumps(JSON_REQUEST))
        try:
            APView = response.json()["result"][0]['eth']['eth1']["macs"][0][:17]
            # print(APView)
            APView_full = response.json()
            # print(f"If you see this than something is working right\n {APView_full}")
            return APView_full
        except:
            APView = response.json()
            # APView = "No Mac Found"
            return APView

    def get_utopia_customer_mac(self, site_id):
        JSON_REQUEST = {
            "apikey": self.api_key,
            "siteid": site_id,
        }

        response = requests.post("https://api.utopiafiber.com/spquery/apview", data=json.dumps(JSON_REQUEST))
        log_message_whole('info', response.json(), filename)
        try:
            APView = response.json()["result"][0]['eth']['eth1']["macs"][0][:17]
            APView_full = response.json()
            # print(f"If you see this than something is working right\n {APView_full}")
        except:
            APView = response.json()
            # APView = "No Mac Found"
        return APView

    # Send GET request to UTOPIA API to check MAC address existence
    def check_mac_exists_in_utopia(self, mac_address):
        try:
            utopia_response = self.get_utopia_site_id_by_mac(mac_address)

            if 'status' in utopia_response and utopia_response['status'] == 'notfound':
                print(f"MAC Address not found in Utopia. MAC: {mac_address}")
                return False  # or some other error value

            site_id = utopia_response.get('siteid')

            if site_id:
                mac_from_utopia = self.get_utopia_customer_mac(site_id)
                cleaned_mac = self.clean_mac_address(mac_address)
                print(f"Site ID: {site_id}, MAC from Utopia: {cleaned_mac}")
                return mac_from_utopia
            else:
                print("Failed to retrieve site ID from Utopia.")
                return None  # or some other error value

        except Exception as e:
            print(f"Error in Utopia API: {e}")
            return None  # or some other error value

    def clean_mac_address(self, mac_address):
        # Remove colons and convert to lowercase
        cleaned_mac = ''.join(mac_address.split(':')).lower()
        return cleaned_mac

    def verify_mac_against_utopia(self, mac_address):
        JSON_REQUEST = {
            "apikey": self.api_key,
            "mac": mac_address,
        }
        try:
            # Make the API call to Utopia
            #response = requests.post("https://api.utopiafiber.com/spquery/macsearch", data=json.dumps(JSON_REQUEST))

            log_message_whole('api',  f"API call to UTOPIA: https://api.utopiafiber.com/spquery/macsearch {json.dumps(JSON_REQUEST)}", filename)

            response = requests.post("https://api.utopiafiber.com/spquery/macsearch", data=json.dumps(JSON_REQUEST))

            log_message_whole('api',  f"API call from UTOPIA: {response.json()}", filename)

            if response.status_code == 200:
                utopia_data = response.json()

                if utopia_data["status"] == "success":
                    # MAC exists in Utopia, retrieve customer information
                    site_id = utopia_data["siteid"]
                    customer_info = {
                        "status": utopia_data["status"],
                        "msg": utopia_data["msg"],
                        "site_id": site_id,
                        "mac_address": utopia_data["mac"],
                        "vlan": utopia_data["vlan"],
                    }
                    log_message = f"\nUtopia response:\n"

                    for key, value in customer_info.items():
                        log_message += f"{key}: {value}\n"

                    log_message_whole('info', "\n"+log_message+"\n", filename)

                    return customer_info
                elif utopia_data["status"] == "notfound":
                    log_message_whole('error', f"Utopia status: {utopia_data['status']}", filename)
                    return None
                else:
                    # Handle other Utopia response statuses if needed
                    return None
            else:
                # Handle non-200 status codes
                return None
        except Exception as e:
            # Handle exceptions
            print(f"Error during Utopia API request: {str(e)}")
            return None

    def get_customer_name(self, site_id):
        utopia_api_url = "https://api.utopiafiber.dev/spquery/macsearch"

        # Required Parameters
        params = {
            "apikey": self.api_key,
            "siteID": site_id
        }

        try:
            # Make the API call to Utopia
            response = requests.post(utopia_api_url, json=params)

            if response.status_code == 200:

                utopia_data = response.json()
                # utopia_data = {
                #     "status": "success",
                #     "msg": "0000006458 is assigned to siteid 111111",
                #     "siteid": 1111111,
                #     "mac": "4CD717361645",
                #     "vlan": "530",
                #     "lastseen": "2022-01-17 13:17:00 MST",
                #     "firstseen": "2022-01-04 16:45:06 MST",
                #     "lastseensec": "1642450620",
                #     "firstseensec": "1641339906"
                # }

                if utopia_data["status"] == "success":
                    # MAC exists in Utopia, retrieve customer information
                    site_id = utopia_data["siteid"]
                    customer_info = {
                        "site_id": site_id,
                        "mac_address": utopia_data["mac"],
                        "vlan": utopia_data["vlan"],
                    }
                    return customer_info
                elif utopia_data["status"] == "notfound":
                    log_message_whole('error', f"Utopia status: {utopia_data['status']}", filename)
                    return None
                else:
                    # Handle other Utopia response statuses if needed
                    return None
            else:
                # Handle non-200 status codes
                return None
        except Exception as e:
            # Handle exceptions
            log_message_whole('error', f"Error during Utopia API request: {str(e)}", filename)
            return None

    def get_apview_eth1_macs(self, site_id):
        """Return all MACs in GE1 port"""
        JSON_REQUEST = {
            "apikey": self.api_key,
            "siteid": site_id,
        }

        try:
            response = requests.post("https://api.utopiafiber.com/spquery/apview", data=json.dumps(JSON_REQUEST))
            response.raise_for_status()  # Raise exception for HTTP errors (4xx or 5xx)

            # Load JSON data
            data = response.json()

            # Check if the 'result' key exists
            if 'result' in data:
                # Check if the 'eth' key exists
                if 'eth' in data['result'][0]:
                    # Check if the 'eth1' key exists
                    if 'eth1' in data['result'][0]['eth']:
                        # Check if the 'macs' key exists
                        if 'macs' in data['result'][0]['eth']['eth1']:
                            # Extract the MAC addresses from 'eth1'
                            eth1_macs = data['result'][0]['eth']['eth1']['macs']
                            return eth1_macs
                        else:
                            # 'macs' key not found under 'eth1'
                            log_message_whole('error', data, filename)
                            return []
                    else:
                        # 'eth1' key not found under 'eth'
                        log_message_whole('error', data, filename)
                        return []
                else:
                    # 'eth' key not found under 'result'
                    log_message_whole('error', data, filename)
                    return []
            else:
                # 'result' key not found in the response
                log_message_whole('error', data, filename)
                return []
        except requests.RequestException as e:
            # Handle HTTP request exceptions (e.g., connection error)
            log_message_whole("error", f"HTTP request failed: {e}", filename)
            return []
        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            log_message_whole("error", f"Failed to parse JSON response: {e}", filename)
            return []

    def get_service(self, site_id):
        utopia_api_url = "https://api.utopiafiber.com/spquery/service"

        params = {
            "apikey": self.api_key,
            "siteid": site_id
        }

        try:
            response = requests.post(utopia_api_url, json=params)

            if response.status_code == 200:
                try:
                    utopia_data = response.json()
                except ValueError:
                    log_message_whole('error', "Failed to parse JSON from Utopia response", filename)
                    return None

                log_message_whole('info', f"Utopia raw response: {utopia_data}", filename)

                if "error" in utopia_data:
                    log_message_whole('error', f"Utopia API error: {utopia_data['error']}", filename)
                    return None

                if "data" in utopia_data and utopia_data["data"]:
                    customer_name = utopia_data["data"][0].get("customer", "")
                    return customer_name
                else:
                    log_message_whole('warning', f"Utopia API returned no data for siteid {site_id}", filename)
                    return None
            else:
                log_message_whole('error', f"Utopia returned non-200: {response.status_code} - {response.text}",
                                  filename)
                return None

        except Exception as e:
            log_message_whole('error', f"Exception during Utopia API request: {str(e)}", filename)
            return None

