import json
import datetime
import os

from powercode_manager import PowercodeManager
from utopia_manager import UtopiaManager
from router_manager import RouterManager
from email_manager import EmailSender
from logger import log_message, log_message_short, log_message_whole


# Instantiate the RouterManager, PowercodeManager and UtopiaManager
powercode_manager = PowercodeManager()
utopia_manager = UtopiaManager()
router_manager = RouterManager()
email_manager = EmailSender()

# Configure logging
# Get the filename of the current script
filename = os.path.basename(__file__)
# Set the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize counters and error log
successful_leases = 0
unsuccessful_leases = 0
new_leases = 0
changed_leases = 0
error_messages = []


def start_app():
    log_message('info', "SCRIPT START", filename)
    try:
        # Step 2: Get dynamic DHCP leases from PC_Server-VLAN3815-DHCP-VLAN-533-YF_Residential
        # Attempt to connect to the router
        connected = router_manager.connect_to_router()
        # If connection failed, log an error and return from the function
        if not connected:
            log_error("Failed to connect to the router.")
            return

        leases = router_manager.get_dynamic_dhcp_leases()

        if leases:
            total_lease_amount = len(leases)
            for index, lease in enumerate(leases, start=1):
                process_lease(lease, index, total_lease_amount)  # Pass lease_number and total_lease_amount
                log_message("info", "\n", filename)

            log_message("info", f"Total successful leases: {successful_leases}", filename)
            log_message("info", f"Total unsuccessful leases: {unsuccessful_leases}", filename)
            log_message("info", f"Total new leases: {new_leases}", filename)
            log_message("info", f"Total changed leases: {changed_leases}", filename)
            log_message("info", "SCRIPT END", filename)

        else:
            log_message("info", "You're all caught up around here, best of luck", filename)

    except TimeoutError as e:
        log_error(f"Timeout error occurred while connecting to the router: {e}")
    except Exception as e:
        log_error(f"Error in start_app: %s {str(e)}")

    # Sending email
    send_summary_email()


def process_lease(lease, lease_number, total_lease_amount):
    global successful_leases, unsuccessful_leases
    # Step 2a: Get MAC and IP from each lease
    mac_address = lease.get('mac-address')
    ip_address = lease.get('address')

    log_message("info",
                f"PROCESSING LEASE [{lease_number} out of {total_lease_amount}]: MAC {mac_address}, IP {ip_address}", filename)

    # Step 3 and 3b: Verify MAC against Utopia and Get customer info from Utopia
    utopia_data = utopia_manager.verify_mac_against_utopia(mac_address)
    if utopia_data:
        success = handle_utopia_info(utopia_data, mac_address, ip_address)
        log_message("debug", f"Testing: in process_lease->if utopia_data>success {success}")
        if success:
            successful_leases += 1
        else:
            unsuccessful_leases += 1
    else:
        log_error(f"Couldn't verify MAC for IP: {ip_address}; MAC: {mac_address}")
        unsuccessful_leases += 1


def handle_utopia_info(utopia_siteid_mac_vlan, mac_address, ip_address):
    global successful_leases, unsuccessful_leases
    site_id = utopia_siteid_mac_vlan['site_id']

    # Get all macs connected to Eth1 on ONT
    macs = utopia_manager.get_apview_eth1_macs(site_id)

    if len(macs) == 1:
        log_message("info", f"Utopia customer has only one MAC {macs}", filename)
        # Step 5: Add equipment to PowerCode
        powercode_customer = powercode_manager.get_customer_by_external_id(site_id)
        if powercode_customer:
            success = process_powercode_customer(powercode_customer, mac_address, ip_address, site_id)
            if not success:
                log_message("debug", "Testing: In handle_utopia_info if not success returning False")
                return False
            log_message("debug", "Testing: In handle_utopia_info returning True")
            return True
        else:
            log_error(f"Customer with site ID {site_id} not found or incomplete information in Powercode")
            return False
    elif len(macs) > 1:
        log_error(f"Customer with site ID {site_id} has more than one MAC connected to GE1: {macs}")
        # show account in powercode
        powercode_manager.get_customer_by_external_id(site_id)
        return False
    else:
        log_error(f"No devices found for this site, error with ONT, MAC: {mac_address}")
        return False


def process_powercode_customer(powercode_customer, mac_address, ip_address, site_id):
    global new_leases, changed_leases, unsuccessful_leases

    # Step 4: Delete DHCP lease for verified MAC
    router_manager.remove_dynamic_dhcp_lease(client_ip=ip_address)

    # Check if customer has equipment on account
    list_of_equipment = powercode_manager.get_customer_equipment(powercode_customer["customerId"])
    # Log entry for existing equipment
    log_message("info",
                f"Equipment found on customer's #{powercode_customer['customerId']} account: {json.dumps(list_of_equipment, indent=3)}", filename)

    # Update equipment if exist
    if list_of_equipment:
        # counter for updated equipment
        changed_leases += 1
        handle_existing_equipment(list_of_equipment, mac_address, powercode_customer)
        return True
    # Creating equipment
    else:
        # Get Utopia customer name
        utopia_cust_name = utopia_manager.get_service(site_id)

        log_message(f"Utopia: {utopia_cust_name} | Powercode: {powercode_customer['companyName']}.", filename)
        log_message(f"Names matched:{utopia_cust_name == powercode_customer['companyName']}", filename)

        normalized_utopia = normalize_name(utopia_cust_name)
        normalized_powercode = normalize_name(powercode_customer['companyName'])

        # Compare Utopia customer name with Powercode name
        if normalized_utopia == normalized_powercode:
            # if matches then continue
            new_leases += 1
            created_equipment_id = powercode_manager.create_equipment(customer_id=powercode_customer["customerId"],
                                                                      name=powercode_customer[
                                                                               "companyName"] + " - Generated by DLR",
                                                                      mac_address=mac_address)
            # Check if equipment creation was successful
            if created_equipment_id:
                # log_message("info", f"Equipment successfully created: {created_equipment_id}", filename)
                # Get IP of new created equipment
                equipment_data = powercode_manager.read_equipment(created_equipment_id)
                ip_address = equipment_data.get("OriginalIpAddress")
                log_message("info", f"Equipment created: {created_equipment_id}, IP address from DB: {ip_address}",
                            filename)
            else:
                log_error(f"Equipment creation failed for site ID {site_id}, MAC: {mac_address}")
                # unsuccessful_leases += 1  # Increment unsuccessful_leases if creation fails
                return False

            # Activating account
            try:
                current_status = powercode_manager.read_customer(powercode_customer["customerId"])
                current_status = current_status["status"].lower()
                if current_status.lower() != "active":
                    powercode_manager.update_customer_status(powercode_customer["customerId"])
                else:
                    log_message("info", f"Customer status is {current_status}", filename)

                return True

            except Exception as e:
                log_error(f"Error with activating customer {powercode_customer['customerId']}: %s {str(e)}")
        else:
            # else fail, update unsuccessful_leases and send email
            # unsuccessful_leases += 1
            log_error(f"Equipment is not created for {utopia_cust_name} due to name mismatching: "
                                 f"Utopia: ({utopia_cust_name}) vs "
                                 f"Powercode: ({powercode_customer['companyName']})")

            return False


def handle_existing_equipment(existing_equipment, new_mac_address, powercode_customer):
    # Check if there is just one equipment entry
    if len(existing_equipment) == 1:
        # Extract the ID of the first equipment
        # Accessing the first equipment entry in the list
        equipment_entry = existing_equipment[0]

        # Accessing equipment ID and IP address
        equipment_id = equipment_entry['equipmentID']

        # equipment_id = existing_equipment["equipment"][0]["equipmentID"]
        equipment_name = powercode_customer["companyName"] + "- Updated by DLR"
        notes = f"Equipment Edited by Dynamic Lease Runner (DLR) {datetime.datetime.now().strftime('%H:%M:%S %m-%d-%Y')}"

        powercode_manager.update_equipment(
            equipment_id,
            name=equipment_name,
            mac_address=new_mac_address,
            notes=notes,
            snmp_version=1
        )
    else:
        # Log error if multiple entries found
        log_error(f"Multiple entries found for existing equipment - {existing_equipment}. Unable to proceed.")


def log_error(message):
    log_message("error", message, filename)
    error_messages.append(message)


def send_summary_email():
    formatted_datetime = datetime.datetime.now().strftime('%H:%M:%S %m-%d-%Y')

    # Format the successful and unsuccessful lease counts
    header = f"Summary of Lease Processing ({formatted_datetime}) \n\n"
    header += "\n" + "=" * 50 + "\n"
    header += f"{'Total successful leases:':<30} {successful_leases}\n"
    header += f"{'Total unsuccessful leases:':<30} {unsuccessful_leases}\n\n"
    header += f"{'Total new leases:':<30} {new_leases}\n"
    header += f"{'Total changed leases:':<30} {changed_leases}\n"
    header += "=" * 50 + "\n\n"

    # Format the errors list
    if error_messages:
        error_section = "Errors:\n" + "-" * 50 + "\n"
        for i, error in enumerate(error_messages, 1):
            error_section += f"{i}. {error}\n\n"
    else:
        error_section = "Errors: None\n"

    # Combine the sections
    body = header + error_section

    # Send the email with the formatted body
    email_manager.send_email_with_attachment(body)


def normalize_name(name):
    if not name:
        return ""
    return ' '.join(name.strip().split()).lower()


if __name__ == '__main__':
    start_app()

