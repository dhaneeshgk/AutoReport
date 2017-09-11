'''
Created on 12-Jul-2017

@author: dhaneeshgk
'''

import requests
import json
import time


def start_vm(vm="wpva",Authorization=None):

    start_url = 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/virtualMachines/{vm}/start?api-version={apiVersion}'

    start_url = start_url.format(subscriptionId="cec3a9b2-740d-4391-9a47-1ba00d99bb1a",resourceGroup="DataScience",vm=vm,apiVersion="2016-04-30-preview")

    headers = {'Content-Type':'application/json','Authorization':Authorization}

    start_res = requests.post(url=start_url,headers=headers)
    print(start_res.content)
    print(start_res.status_code)
    if start_res.status_code == 200:
        return True
    else:
        return False

def stop_vm(vm="wpva",Authorization=None):

    stop_url = 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/virtualMachines/{vm}/powerOff?api-version={apiVersion}'
    stop_url = stop_url.format(subscriptionId="cec3a9b2-740d-4391-9a47-1ba00d99bb1a",resourceGroup="DataScience",vm=vm,apiVersion="2016-04-30-preview")

    headers = {'Content-Type':'application/json','Authorization':Authorization}

    stop_res = requests.post(url=stop_url,headers=headers)
    print(stop_res.content)
    print(stop_res.status_code)
    if stop_res.status_code == 202:
        return True
    else:
        return False


def stop_delocate_vm(vm="wpva",Authorization=None):
    stop_delocate_url = 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/virtualMachines/{vm}/deallocate?api-version={apiVersion}'
    stop_delocate_url = stop_delocate_url.format(subscriptionId="cec3a9b2-740d-4391-9a47-1ba00d99bb1a",resourceGroup="DataScience",vm=vm,apiVersion="2016-04-30-preview")

    headers = {'Content-Type':'application/json','Authorization':Authorization}


    stop_delocate_res = requests.post(url=stop_delocate_url,headers=headers)

    print(stop_delocate_res.content)
    print(stop_delocate_res.status_code)
    if stop_delocate_res.status_code == 202:
        return True
    else:
        return False

def get_vm_in_info(vm="wpva",Authorization=None):

    vm_info_url = 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/virtualMachines/{vm}?$expand=instanceView&api-version={apiVersion}'
    vm_info_url = vm_info_url.format(subscriptionId="cec3a9b2-740d-4391-9a47-1ba00d99bb1a",resourceGroup="DataScience",vm=vm,apiVersion="2016-04-30-preview")

    headers = {'Content-Type':'application/json','Authorization':Authorization}

    vm_info_res = requests.get(url=vm_info_url,headers=headers)

    res_jes = json.loads(vm_info_res.content.decode('utf-8'))
#     for i in res_jes:
#         print(i,res_jes[i])

    for i in res_jes['properties']['instanceView']:
        print(i,res_jes['properties']['instanceView'][i])
    print(vm_info_res.status_code)
    if vm_info_res.status_code == 202:
        return True
    else:
        return False

def get_in_info(vm="wpva",Authorization=None):
    vm_info_url = 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/virtualMachines/{vm}?$expand=instanceView&api-version={apiVersion}'
    vm_info_url = vm_info_url.format(subscriptionId="cec3a9b2-740d-4391-9a47-1ba00d99bb1a",resourceGroup="DataScience",vm=vm,apiVersion="2016-04-30-preview")

    headers = {'Content-Type':'application/json','Authorization':Authorization}

    vm_info_res = requests.get(url=vm_info_url,headers=headers)

    res_jes = json.loads(vm_info_res.content.decode('utf-8'))

    if vm_info_res.status_code == 200:
#         print(res_jes)
#         for i in res_jes['properties']:
#             print(i,res_jes['properties'][i])
#         for i in res_jes['properties']['instanceView']['statuses'][1]['displayStatus']:
#             print(i)
#
#         for i in res_jes['properties']['instanceView']['statuses']:
#             print(i)
        print('displayStatus',res_jes['properties']['instanceView']['statuses'][1]['displayStatus'])
        print(vm_info_res.status_code)
        return True
    else:
        print(res_jes)
        return False

def restart_vm(vm="wpva",Authorization=None):

    re_url = "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/virtualMachines/{vm}/restart?api-version={apiVersion}"
    re_url = re_url.format(subscriptionId="cec3a9b2-740d-4391-9a47-1ba00d99bb1a",resourceGroup="DataScience",vm=vm,apiVersion="2016-04-30-preview")
    headers = {'Content-Type':'application/json','Authorization':Authorization}


    stop_delocate_res = requests.post(url=re_url,headers=headers)

    print(stop_delocate_res.content)
    print(stop_delocate_res.status_code)
    if stop_delocate_res.status_code == 202:
        return True
    else:
        return False


def list_vms_rg(Authorization=None):

    list_vm_url = "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/virtualmachines?api-version={apiVersion}"
    list_vm_url = list_vm_url.format(subscriptionId="cec3a9b2-740d-4391-9a47-1ba00d99bb1a",resourceGroup="DataScience",apiVersion="2016-04-30-preview")
    headers = {'Content-Type':'application/json','Authorization':Authorization}

    list_vm_res = requests.post(url=list_vm_url,headers=headers)

    print(json.loads(list_vm_res.content.decode('utf-8')))
    print(list_vm_res.status_code)
    if list_vm_res.status_code == 202:
        return True
    else:
        return False

def user_login():

    auth_url = 'https://login.microsoftonline.com/fce50195-2315-47af-a684-ff91de5f9075/oauth2/token?api-version=1.0'

    data = {"grant_type":"client_credentials","resource":"https://management.azure.com/", "client_id":"900fc942-d1eb-4c89-a375-8bea0645c077", "client_secret":"P1nmhYAks/Mdd3ltspOn92AW/Zv0fpxLs1JqHhPDDg4=" }

    auth_res = requests.post(url=auth_url,data=data)

    if auth_res.status_code == 200:
        auth_j = json.loads(auth_res.content.decode('utf-8'))
        print(auth_j["token_type"]+" "+auth_j["access_token"])
        return auth_j["token_type"]+" "+auth_j["access_token"]
    else:
        return False

if __name__ == '__main__':
    authT = user_login()
    start_vm("wpva",Authorization=authT)
#     restart_vm(Authorization=authT)
#     stop_vm(Authorization=authT)
#     stop_delocate_vm("wpva",Authorization=authT)
#     get_vm_in_info()
#     time.sleep(3)
#     get_in_info("wpva",Authorization=authT)
#     list_vms_rg(Authorization=authT)

    pass
# 'Authorization':'a0aee855797c451badb68f7c40be957b'

# https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/virtualmachines-start
# https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/virtualmachines-stop
# https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines
# https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/virtualmachines-get
# https://docs.microsoft.com/en-us/rest/api/authorization/
# https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-rest-api
