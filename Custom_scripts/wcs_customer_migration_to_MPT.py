import powercode_manager


PC = powercode_manager.PowercodeManager()


def read_customer_equipment():
    list_of_address_v4_ranges  = PC.custom_function("readAddressRanges")
    print(list_of_address_v4_ranges)


def update_equipment(list_of_equipment_ids):
    for id in list_of_equipment_ids:
        ids = PC.update_equipment(equipment_id=id, address_range_v4=10241, snmp_version=1)
        print(ids)


list_of_equipment_pop_060 = [6902,7329,5804,6743,12642,12956,9728,13269]
list_of_equipment_pop_180 = [13942,16198,12396]
list_of_equipment_pop_300 = [13697,13390,8880,12541,10696,10306,14965,7860,11836]

# update_equipment([16482, 16483])

update_equipment(list_of_equipment_pop_060)
update_equipment(list_of_equipment_pop_180)
update_equipment(list_of_equipment_pop_300)


def search_customers(self, search_string):
    url = self.powercode_management_url + ':444/api/1/index.php'

    data = {
        "apiKey": self.powercode_api_key,
        "action": "searchCustomers",
        "searchString": search_string
    }

    try:
        response = requests.post(url, data, verify=False)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle exceptions, e.g., connection errors
        print(f"Error: {e}")
        return None


def custom_function(self, name_of_cust_func):
    url = self.powercode_management_url + ':444/api/1/index.php'

    data = {
        "apiKey": self.powercode_api_key,
        "action": name_of_cust_func,
    }

    try:
        response = requests.post(url, data, verify=False)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle exceptions, e.g., connection errors
        print(f"Error: {e}")
        return None


"""
{
   "message":"Address Range List",
   "statusCode":0,
   "ranges":[
      {
         "addressRangeID":"-1",
         "name":"Floating MAC Hold",
         "range":"0.0.0.0 - 0.0.0.0",
         "freeIPs":1
      },
      {
         "addressRangeID":"10044",
         "name":"GN-LINKS",
         "range":"10.10.0.1 - 10.10.5.254",
         "freeIPs":1412
      },
      {
         "addressRangeID":"10045",
         "name":"GN-PUBLIC_MGMT",
         "range":"216.166.168.1 - 216.166.168.254",
         "freeIPs":254
      },
      {
         "addressRangeID":"10049",
         "name":"GN-PRIVATE_MGMT",
         "range":"172.31.0.1 - 172.31.7.254",
         "freeIPs":2030
      },
      {
         "addressRangeID":"10056",
         "name":"GN-LOOPBACKS-254",
         "range":"10.0.254.0 - 10.0.254.254",
         "freeIPs":205
      },
      {
         "addressRangeID":"10066",
         "name":"LTE-BZN-BWT-UE",
         "range":"172.21.20.1 - 172.21.23.254",
         "freeIPs":1022
      },
      {
         "addressRangeID":"10078",
         "name":"v_BZN-BSL-CPEMGMT",
         "range":"172.22.12.31 - 172.22.15.254",
         "freeIPs":960
      },
      {
         "addressRangeID":"10083",
         "name":"BZN-BF-BUS-MGMT",
         "range":"172.25.12.2 - 172.25.15.252",
         "freeIPs":831
      },
      {
         "addressRangeID":"10085",
         "name":"BZN-BF-BUSDED-MGMT",
         "range":"172.25.20.2 - 172.25.23.252",
         "freeIPs":1012
      },
      {
         "addressRangeID":"10089",
         "name":"BZN-BF-BUS-CUST_1",
         "range":"216.166.171.66 - 216.166.171.124",
         "freeIPs":0
      },
      {
         "addressRangeID":"10091",
         "name":"BZN-BF-BUSDED-CUST",
         "range":"216.166.171.130 - 216.166.171.188",
         "freeIPs":52
      },
      {
         "addressRangeID":"10095",
         "name":"BZN-USBSVC-MGMT",
         "range":"172.26.0.2 - 172.26.3.252",
         "freeIPs":1005
      },
      {
         "addressRangeID":"10096",
         "name":"BZN-USBSVC-CUST",
         "range":"216.166.169.18 - 216.166.169.28",
         "freeIPs":2
      },
      {
         "addressRangeID":"10097",
         "name":"GN-LOOPBACKS-253",
         "range":"10.0.253.0 - 10.0.253.254",
         "freeIPs":255
      },
      {
         "addressRangeID":"10098",
         "name":"v_HLN-MHM-SITEGEAR",
         "range":"172.22.172.2 - 172.22.172.30",
         "freeIPs":4
      },
      {
         "addressRangeID":"10100",
         "name":"BZN-CNR-Mimosa-MGMT",
         "range":"172.22.16.1 - 172.22.19.254",
         "freeIPs":1013
      },
      {
         "addressRangeID":"10101",
         "name":"BZN-CNR-Mimosa-CUST-1",
         "range":"216.166.169.34 - 216.166.169.62",
         "freeIPs":15
      },
      {
         "addressRangeID":"10120",
         "name":"v_BTE-BTC-SITEGEAR",
         "range":"172.22.144.2 - 172.22.144.30",
         "freeIPs":21
      },
      {
         "addressRangeID":"10121",
         "name":"v_BTE-BTC-CPEMGMT",
         "range":"172.22.144.31 - 172.22.147.254",
         "freeIPs":924
      },
      {
         "addressRangeID":"10123",
         "name":"v_GN-CUST-PUBLICS-175-ZAYO",
         "range":"216.166.175.2 - 216.166.175.252",
         "freeIPs":78
      },
      {
         "addressRangeID":"10124",
         "name":"v_BZN-PVD-SITEGEAR",
         "range":"172.22.80.2 - 172.22.80.30",
         "freeIPs":20
      },
      {
         "addressRangeID":"10125",
         "name":"v_BZN-PVD-CPEMGMT",
         "range":"172.22.80.31 - 172.22.83.254",
         "freeIPs":925
      },
      {
         "addressRangeID":"10126",
         "name":"v_GN-CUST-NATS-POOL1",
         "range":"172.17.0.2 - 172.17.7.252",
         "freeIPs":681
      },
      {
         "addressRangeID":"10127",
         "name":"v_BZN-PHR-SITEGEAR",
         "range":"172.22.40.2 - 172.22.40.30",
         "freeIPs":21
      },
      {
         "addressRangeID":"10128",
         "name":"v_BZN-PHR-CPEMGMT",
         "range":"172.22.40.31 - 172.22.43.254",
         "freeIPs":964
      },
      {
         "addressRangeID":"10130",
         "name":"v_HLN-APR-SITEGEAR",
         "range":"172.22.164.2 - 172.22.164.30",
         "freeIPs":20
      },
      {
         "addressRangeID":"10131",
         "name":"v_HLN-APR-CPEMGMT",
         "range":"172.22.164.31 - 172.22.167.254",
         "freeIPs":980
      },
      {
         "addressRangeID":"10132",
         "name":"v_BZN-EBL-SITEGEAR",
         "range":"172.22.0.2 - 172.22.0.30",
         "freeIPs":6
      },
      {
         "addressRangeID":"10133",
         "name":"v_BZN-EBL-CPEMGMT",
         "range":"172.22.0.31 - 172.22.3.254",
         "freeIPs":806
      },
      {
         "addressRangeID":"10134",
         "name":"v_BZN-YCC-SITEGEAR",
         "range":"172.22.100.2 - 172.22.100.30",
         "freeIPs":15
      },
      {
         "addressRangeID":"10135",
         "name":"v_BZN-YCC-CPEMGMT",
         "range":"172.22.100.31 - 172.22.103.254",
         "freeIPs":963
      },
      {
         "addressRangeID":"10136",
         "name":"v_BZN-GPR-SITEGEAR",
         "range":"172.22.104.2 - 172.22.104.30",
         "freeIPs":22
      },
      {
         "addressRangeID":"10137",
         "name":"v_BZN-GPR-CPEMGMT",
         "range":"172.22.104.31 - 172.22.107.254",
         "freeIPs":982
      },
      {
         "addressRangeID":"10138",
         "name":"v_BZN-SPR-SITEGEAR",
         "range":"172.22.4.2 - 172.22.4.30",
         "freeIPs":13
      },
      {
         "addressRangeID":"10139",
         "name":"v_BZN-SPR-CPEMGMT",
         "range":"172.22.4.31 - 172.22.7.254",
         "freeIPs":938
      },
      {
         "addressRangeID":"10140",
         "name":"v_BZN-i90-SITEGEAR",
         "range":"172.22.56.2 - 172.22.56.30",
         "freeIPs":19
      },
      {
         "addressRangeID":"10141",
         "name":"v_BZN-i90-CPEMGMT",
         "range":"172.22.56.31 - 172.22.59.254",
         "freeIPs":863
      },
      {
         "addressRangeID":"10142",
         "name":"v_BZN-SIL-SITEGEAR",
         "range":"172.22.52.2 - 172.22.52.30",
         "freeIPs":8
      },
      {
         "addressRangeID":"10143",
         "name":"v_BZN-SIL-CPEMGMT",
         "range":"172.22.52.31 - 172.22.55.254",
         "freeIPs":813
      },
      {
         "addressRangeID":"10144",
         "name":"v_BZN-THR-SITEGEAR",
         "range":"172.22.32.2 - 172.22.32.30",
         "freeIPs":10
      },
      {
         "addressRangeID":"10145",
         "name":"v_BZN-THR-CPEMGMT",
         "range":"172.22.32.31 - 172.22.35.254",
         "freeIPs":876
      },
      {
         "addressRangeID":"10146",
         "name":"BZN-BF-BUS-CUST_2",
         "range":"216.166.171.194 - 216.166.171.252",
         "freeIPs":2
      },
      {
         "addressRangeID":"10147",
         "name":"v_BZN-TSD-SITEGEAR",
         "range":"172.22.28.2 - 172.22.28.30",
         "freeIPs":12
      },
      {
         "addressRangeID":"10148",
         "name":"v_BZN-TSD-CPEMGMT",
         "range":"172.22.28.31 - 172.22.31.254",
         "freeIPs":841
      },
      {
         "addressRangeID":"10149",
         "name":"v_BZN-MAT-SITEGEAR",
         "range":"172.22.24.2 - 172.22.24.30",
         "freeIPs":0
      },
      {
         "addressRangeID":"10150",
         "name":"v_BZN-MAT-CPEMGMT",
         "range":"172.22.24.31 - 172.22.27.254",
         "freeIPs":842
      },
      {
         "addressRangeID":"10151",
         "name":"v_BZN-CMP-SITEGEAR",
         "range":"172.22.68.2 - 172.22.68.30",
         "freeIPs":17
      },
      {
         "addressRangeID":"10152",
         "name":"v_BZN-CMP-CPEMGMT",
         "range":"172.22.68.31 - 172.22.71.254",
         "freeIPs":952
      },
      {
         "addressRangeID":"10153",
         "name":"v_GTF-GTA-SITEGEAR",
         "range":"172.22.204.2 - 172.22.204.30",
         "freeIPs":23
      },
      {
         "addressRangeID":"10154",
         "name":"v_GTF-GTA-CPEMGMT",
         "range":"172.22.204.31 - 172.22.207.254",
         "freeIPs":990
      },
      {
         "addressRangeID":"10155",
         "name":"v_BZN-BCC-SITEGEAR",
         "range":"172.22.60.2 - 172.22.60.30",
         "freeIPs":16
      },
      {
         "addressRangeID":"10156",
         "name":"v_BZN-BCC-CPEMGMT",
         "range":"172.22.60.31 - 172.22.63.254",
         "freeIPs":948
      },
      {
         "addressRangeID":"10157",
         "name":"v_HLN-RBT-SITEGEAR",
         "range":"172.22.168.2 - 172.22.168.30",
         "freeIPs":12
      },
      {
         "addressRangeID":"10158",
         "name":"v_HLN-RBT-CPEMGMT",
         "range":"172.22.168.31 - 172.22.171.254",
         "freeIPs":959
      },
      {
         "addressRangeID":"10159",
         "name":"v_HLN-MHM-CPEMGMT",
         "range":"172.22.172.31 - 172.22.175.254",
         "freeIPs":860
      },
      {
         "addressRangeID":"10160",
         "name":"v_GN-CUST-PUBLICS-172-ZAYO",
         "range":"216.166.172.2 - 216.166.172.252",
         "freeIPs":70
      },
      {
         "addressRangeID":"10161",
         "name":"v_BZN-BSL-SITEGEAR",
         "range":"172.22.12.2 - 172.22.12.30",
         "freeIPs":14
      },
      {
         "addressRangeID":"10162",
         "name":"v_BZN-BCH-SITEGEAR",
         "range":"172.22.36.2 - 172.22.36.30",
         "freeIPs":21
      },
      {
         "addressRangeID":"10163",
         "name":"v_BZN-BCH-CPEMGMT",
         "range":"172.22.36.31 - 172.22.39.254",
         "freeIPs":983
      },
      {
         "addressRangeID":"10164",
         "name":"v_BZN-ELD-SITEGEAR",
         "range":"172.22.44.2 - 172.22.44.30",
         "freeIPs":25
      },
      {
         "addressRangeID":"10165",
         "name":"v_BZN-ELD-CPEMGMT",
         "range":"172.22.44.31 - 172.22.47.254",
         "freeIPs":985
      },
      {
         "addressRangeID":"10166",
         "name":"v_BZN-GRF-SITEGEAR",
         "range":"172.22.72.2 - 172.22.72.30",
         "freeIPs":24
      },
      {
         "addressRangeID":"10167",
         "name":"v_BZN-GRF-CPEMGMT",
         "range":"172.22.72.31 - 172.22.75.254",
         "freeIPs":989
      },
      {
         "addressRangeID":"10168",
         "name":"v_BZN-HFL-SITEGEAR",
         "range":"172.22.48.2 - 172.22.48.30",
         "freeIPs":13
      },
      {
         "addressRangeID":"10169",
         "name":"v_BZN-HFL-CPEMGMT",
         "range":"172.22.48.31 - 172.22.51.254",
         "freeIPs":852
      },
      {
         "addressRangeID":"10170",
         "name":"v_BZN-RMR-SITEGEAR",
         "range":"172.22.84.2 - 172.22.84.30",
         "freeIPs":22
      },
      {
         "addressRangeID":"10171",
         "name":"v_BZN-RMR-CPEMGMT",
         "range":"172.22.84.31 - 172.22.87.254",
         "freeIPs":961
      },
      {
         "addressRangeID":"10172",
         "name":"v_GTF-EGL-SITEGEAR",
         "range":"172.22.192.2 - 172.22.192.30",
         "freeIPs":25
      },
      {
         "addressRangeID":"10173",
         "name":"v_GTF-EGL-CPEMGMT",
         "range":"172.22.192.31 - 172.22.195.254",
         "freeIPs":987
      },
      {
         "addressRangeID":"10174",
         "name":"v_GTF-HSE-SITEGEAR",
         "range":"172.22.196.2 - 172.22.196.30",
         "freeIPs":22
      },
      {
         "addressRangeID":"10175",
         "name":"v_GTF-HSE-CPEMGMT",
         "range":"172.22.196.31 - 172.22.199.254",
         "freeIPs":978
      },
      {
         "addressRangeID":"10176",
         "name":"v_GTF-SKY-SITEGEAR",
         "range":"172.22.208.2 - 172.22.208.30",
         "freeIPs":22
      },
      {
         "addressRangeID":"10177",
         "name":"v_GTF-SKY-CPEMGMT",
         "range":"172.22.208.31 - 172.22.211.254",
         "freeIPs":964
      },
      {
         "addressRangeID":"10178",
         "name":"v_GTF-HFT-SITEGEAR",
         "range":"172.22.212.2 - 172.22.212.30",
         "freeIPs":23
      },
      {
         "addressRangeID":"10179",
         "name":"v_GTF-HFT-CPEMGMT",
         "range":"172.22.212.31 - 172.22.215.254",
         "freeIPs":976
      },
      {
         "addressRangeID":"10180",
         "name":"v_BZN-ERS-SITEGEAR",
         "range":"172.22.64.2 - 172.22.64.30",
         "freeIPs":24
      },
      {
         "addressRangeID":"10181",
         "name":"v_BZN-ERS-CPEMGMT",
         "range":"172.22.64.31 - 172.22.67.254",
         "freeIPs":972
      },
      {
         "addressRangeID":"10182",
         "name":"v_BZN-DCR-SITEGEAR",
         "range":"172.22.76.2 - 172.22.76.30",
         "freeIPs":16
      },
      {
         "addressRangeID":"10183",
         "name":"v_BZN-DCR-CPEMGMT",
         "range":"172.22.76.31 - 172.22.79.254",
         "freeIPs":942
      },
      {
         "addressRangeID":"10184",
         "name":"v_BZN-TFB-SITEGEAR",
         "range":"172.22.88.2 - 172.22.88.30",
         "freeIPs":23
      },
      {
         "addressRangeID":"10185",
         "name":"v_BZN-TFB-CPEMGMT",
         "range":"172.22.88.31 - 172.22.91.254",
         "freeIPs":985
      },
      {
         "addressRangeID":"10186",
         "name":"v_BZN-PRC-SITEGEAR",
         "range":"172.22.108.2 - 172.22.108.30",
         "freeIPs":4
      },
      {
         "addressRangeID":"10187",
         "name":"v_BZN-PRC-CPEMGMT",
         "range":"172.22.108.31 - 172.22.111.254",
         "freeIPs":740
      },
      {
         "addressRangeID":"10188",
         "name":"v_BTE-LAG-SITEGEAR",
         "range":"172.22.136.2 - 172.22.136.30",
         "freeIPs":22
      },
      {
         "addressRangeID":"10189",
         "name":"v_BTE-LAG-CPEMGMT",
         "range":"172.22.136.31 - 172.22.139.254",
         "freeIPs":938
      },
      {
         "addressRangeID":"10190",
         "name":"GN-OOKLA_SERVER",
         "range":"216.166.169.97 - 216.166.169.98",
         "freeIPs":2
      },
      {
         "addressRangeID":"10191",
         "name":"v_BZN-CWT-SITEGEAR",
         "range":"172.22.112.2 - 172.22.112.30",
         "freeIPs":19
      },
      {
         "addressRangeID":"10192",
         "name":"v_BZN-CWT-CPEMGMT",
         "range":"172.22.112.31 - 172.22.115.254",
         "freeIPs":972
      },
      {
         "addressRangeID":"10193",
         "name":"v_BTE-MTB-SITEGEAR",
         "range":"172.22.132.2 - 172.22.132.30",
         "freeIPs":15
      },
      {
         "addressRangeID":"10194",
         "name":"v_BTE-MTB-CPEMGMT",
         "range":"172.22.132.31 - 172.22.135.254",
         "freeIPs":944
      },
      {
         "addressRangeID":"10195",
         "name":"v_BTE-POM-SITEGEAR",
         "range":"172.22.140.2 - 172.22.140.30",
         "freeIPs":21
      },
      {
         "addressRangeID":"10196",
         "name":"v_BTE-POM-CPEMGMT",
         "range":"172.22.140.31 - 172.22.143.254",
         "freeIPs":957
      },
      {
         "addressRangeID":"10197",
         "name":"v_BZN-RIV-SITEGEAR",
         "range":"172.22.8.2 - 172.22.8.30",
         "freeIPs":2
      },
      {
         "addressRangeID":"10198",
         "name":"v_BZN-RIV-CPEMGMT",
         "range":"172.22.8.31 - 172.22.11.254",
         "freeIPs":841
      },
      {
         "addressRangeID":"10199",
         "name":"v_BZN-BWT-SITEGEAR",
         "range":"172.22.20.2 - 172.22.20.30",
         "freeIPs":1
      },
      {
         "addressRangeID":"10200",
         "name":"v_BZN-BWT-CPEMGMT",
         "range":"172.22.20.31 - 172.22.23.254",
         "freeIPs":796
      },
      {
         "addressRangeID":"10201",
         "name":"v_BZN-MDV-SITEGEAR",
         "range":"172.22.92.2 - 172.22.92.30",
         "freeIPs":18
      },
      {
         "addressRangeID":"10202",
         "name":"v_BZN-MDV-CPEMGMT",
         "range":"172.22.92.31 - 172.22.95.254",
         "freeIPs":978
      },
      {
         "addressRangeID":"10203",
         "name":"v_HLN-PIT-SITEGEAR",
         "range":"172.22.184.2 - 172.22.184.30",
         "freeIPs":24
      },
      {
         "addressRangeID":"10204",
         "name":"v_HLN-PIT-CPEMGMT",
         "range":"172.22.184.31 - 172.22.187.254",
         "freeIPs":959
      },
      {
         "addressRangeID":"10205",
         "name":"v_HLN-SCR-SITEGEAR",
         "range":"172.22.180.2 - 172.22.180.30",
         "freeIPs":23
      },
      {
         "addressRangeID":"10206",
         "name":"v_HLN-SCR-CPEMGMT",
         "range":"172.22.180.31 - 172.22.183.254",
         "freeIPs":959
      },
      {
         "addressRangeID":"10207",
         "name":"v_GN-CUST-PUBLICS-104-CGNT",
         "range":"154.27.104.2 - 154.27.104.252",
         "freeIPs":3
      },
      {
         "addressRangeID":"10208",
         "name":"v_GN-CUST-PUBLICS-105-CGNT",
         "range":"154.27.105.2 - 154.27.105.252",
         "freeIPs":73
      },
      {
         "addressRangeID":"10209",
         "name":"v_GN-CUST-PUBLICS-106-CGNT",
         "range":"154.27.106.2 - 154.27.106.252",
         "freeIPs":71
      },
      {
         "addressRangeID":"10210",
         "name":"v_GN-CUST-PUBLICS-107-CGNT",
         "range":"154.27.107.2 - 154.27.107.252",
         "freeIPs":80
      },
      {
         "addressRangeID":"10211",
         "name":"v_HLN-SPK-SITEGEAR",
         "range":"172.22.176.2 - 172.22.176.30",
         "freeIPs":0
      },
      {
         "addressRangeID":"10212",
         "name":"v_HLN-SPK-CPEMGMT",
         "range":"172.22.176.31 - 172.22.179.254",
         "freeIPs":862
      },
      {
         "addressRangeID":"10213",
         "name":"v_HLN-ICT-SITEGEAR",
         "range":"172.22.160.2 - 172.22.160.30",
         "freeIPs":21
      },
      {
         "addressRangeID":"10214",
         "name":"v_HLN-ICT-CPEMGMT",
         "range":"172.22.160.31 - 172.22.163.254",
         "freeIPs":992
      },
      {
         "addressRangeID":"10215",
         "name":"v_GTF-DAD-SITEGEAR",
         "range":"172.22.200.2 - 172.22.200.30",
         "freeIPs":22
      },
      {
         "addressRangeID":"10216",
         "name":"v_GTF-DAD-CPEMGMT",
         "range":"172.22.200.31 - 172.22.203.254",
         "freeIPs":992
      },
      {
         "addressRangeID":"10217",
         "name":"BZN-BF-BUS-CUST_3",
         "range":"216.166.171.2 - 216.166.171.60",
         "freeIPs":7
      },
      {
         "addressRangeID":"10218",
         "name":"v_BZN-EEW-SITEGEAR",
         "range":"172.22.96.2 - 172.22.96.30",
         "freeIPs":19
      },
      {
         "addressRangeID":"10219",
         "name":"v_BZN-EEW-CPEMGMT",
         "range":"172.22.96.31 - 172.22.99.254",
         "freeIPs":931
      },
      {
         "addressRangeID":"10220",
         "name":"v_GN-DEDBUS-PUBLICS-169.128-ZAYO",
         "range":"216.166.169.130 - 216.166.169.188",
         "freeIPs":54
      },
      {
         "addressRangeID":"10221",
         "name":"v_GN-CUST-PUBLICS-110-CGNT",
         "range":"154.27.110.2 - 154.27.110.252",
         "freeIPs":80
      },
      {
         "addressRangeID":"10222",
         "name":"v_BZN-CHE-SITEGEAR",
         "range":"172.22.116.2 - 172.22.116.30",
         "freeIPs":23
      },
      {
         "addressRangeID":"10223",
         "name":"v_BZN-CHE-CPEMGMT",
         "range":"172.22.116.31 - 172.22.119.254",
         "freeIPs":957
      },
      {
         "addressRangeID":"10224",
         "name":"BZN-BF-BUS-CUST_4",
         "range":"154.27.109.2 - 154.27.109.60",
         "freeIPs":28
      },
      {
         "addressRangeID":"10225",
         "name":"v_GN-CUST-PUBLICS-174-ZAYO",
         "range":"216.166.174.2 - 216.166.174.252",
         "freeIPs":75
      },
      {
         "addressRangeID":"10226",
         "name":"USB.DC01.AGG01-TRANSIT-CNR_w",
         "range":"100.126.1.66 - 100.126.1.67",
         "freeIPs":2
      },
      {
         "addressRangeID":"10227",
         "name":"USB.DC01.AGG01-TRANSIT-HFL_w",
         "range":"100.126.1.114 - 100.126.1.115",
         "freeIPs":0
      },
      {
         "addressRangeID":"10228",
         "name":"CGNAT-POOL1-VLAN-533-YF_Residential",
         "range":"100.80.0.2 - 100.80.7.252",
         "freeIPs":881
      },
      {
         "addressRangeID":"10229",
         "name":"CGNAT-POOL1-VLAN-633-YF_Business",
         "range":"100.80.8.2 - 100.80.15.252",
         "freeIPs":2042
      },
      {
         "addressRangeID":"10230",
         "name":"PUBLIC-CGNT162-VLAN-633-YF_Business",
         "range":"38.92.162.2 - 38.92.162.252",
         "freeIPs":204
      },
      {
         "addressRangeID":"10231",
         "name":"PUBLIC-CGNT163-VLAN-633-YF_Business",
         "range":"38.92.163.2 - 38.92.163.252",
         "freeIPs":249
      },
      {
         "addressRangeID":"10232",
         "name":"PUBLIC-CGNT165-VLAN-933-YF_VoIP",
         "range":"38.92.165.2 - 38.92.165.252",
         "freeIPs":250
      },
      {
         "addressRangeID":"10235",
         "name":"PUBLIC-CGNT167-VLAN-533-YF_Residential",
         "range":"38.92.167.2 - 38.92.167.252",
         "freeIPs":240
      },
      {
         "addressRangeID":"10236",
         "name":"MT.BZN.USB.DC01 Loopbacks",
         "range":"100.127.0.1 - 100.127.0.254",
         "freeIPs":253
      },
      {
         "addressRangeID":"10237",
         "name":"MT.BZN.USB.DC01 Core MGMT",
         "range":"100.112.0.2 - 100.112.0.254",
         "freeIPs":236
      },
      {
         "addressRangeID":"10238",
         "name":"v_BZN-CTR-SITEGEAR",
         "range":"172.22.124.2 - 172.22.124.30",
         "freeIPs":20
      },
      {
         "addressRangeID":"10239",
         "name":"v_BZN-CTR-CPEMGMT",
         "range":"172.22.124.31 - 172.22.127.254",
         "freeIPs":986
      },
      {
         "addressRangeID":"10240",
         "name":"v_BZN-MPT-SITEGEAR",
         "range":"172.22.224.2 - 172.22.224.30",
         "freeIPs":16
      },
      {
         "addressRangeID":"10241",
         "name":"v_BZN-MPT-CPEMGMT",
         "range":"172.22.224.31 - 172.22.227.254",
         "freeIPs":943
      },
      {
         "addressRangeID":"10243",
         "name":"KESTREL-TRANSPORT",
         "range":"154.27.108.73 - 154.27.108.78",
         "freeIPs":4
      },
      {
         "addressRangeID":"10244",
         "name":"MT.BZN.USB.DC01 Data Center MGMT",
         "range":"100.112.8.2 - 100.112.15.252",
         "freeIPs":2041
      },
      {
         "addressRangeID":"10245",
         "name":"v_BZN-TST-SITEGEAR",
         "range":"172.22.252.2 - 172.22.252.30",
         "freeIPs":29
      },
      {
         "addressRangeID":"10246",
         "name":"v_BZN-TST-CPEMGMT",
         "range":"172.22.252.31 - 172.22.255.254",
         "freeIPs":992
      },
      {
         "addressRangeID":"10247",
         "name":"v_GN-CUST-PUBLICS-169.240-ZAYO",
         "range":"216.166.169.242 - 216.166.169.254",
         "freeIPs":12
      },
      {
         "addressRangeID":"10248",
         "name":"v_BZN-TST-CGNAT",
         "range":"100.96.252.2 - 100.96.255.254",
         "freeIPs":1020
      },
      {
         "addressRangeID":"10249",
         "name":"CoB-TRANSPORT",
         "range":"154.27.108.89 - 154.27.108.94",
         "freeIPs":4
      }
   ]
}

"""