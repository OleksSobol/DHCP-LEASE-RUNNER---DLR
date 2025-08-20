# DLR - DHCP Lease Runner

This project automates the process of managing customers and equipment in Powercode and Utopia systems.

## Introduction

This project aims to streamline the process of managing customers and equipment by automating tasks related to Powercode and Utopia systems. It facilitates the synchronization of customer data between these systems and handles tasks such as creating equipment, activating customer accounts, and managing DHCP leases.

## Features

- Retrieves dynamic DHCP leases from routers
- Verifies MAC addresses against the Utopia system
- Creates and updates customer accounts in Powercode
- Manages equipment in Powercode
- Removes DHCP leases for verified MAC addresses
- Sends email notifications with logs attached

## Installation

1. Clone the repository: `git clone https://github.com/your/repository.git`
2. Install dependencies: `pip install -r requirements.txt`

## Usage

1. Ensure all configuration variables are set correctly in the respective manager classes (`PowercodeManager`, `UtopiaManager`, `RouterManager`, `EmailSender`).
2. Run the `start_app()` function in the `main.py` file.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
