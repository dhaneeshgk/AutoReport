import requests
import json
import config

url = config.config['api_url']
headers = {"Content-Type":"application/json"}

def set_up():
    res = requests.get(url=url+"setup")
    con = res.content.decode('utf-8')
    # print(con)
    return json.loads(con)

def login(email_=None,password_=None):
    res = requests.post(url=url+"user_login",headers=headers,
    data = json.dumps({"email":email_,"password":password_}))
    con = res.content.decode('utf-8')
    return json.loads(con)

def validate_auth(access_token=None):
    res = requests.post(url=url+"validate_auth",headers=headers,
    data = json.dumps({"access_token":access_token}))
    con = res.content.decode('utf-8')
    return json.loads(con)

def logout(access_token=None):
    res = requests.post(url=url+"logout",headers=headers,
    data = json.dumps({"access_token":access_token}))
    con = res.content.decode('utf-8')
    return json.loads(con)

def get_users(access_token=None):
    headers.update({'Authorization':access_token})
    res = requests.get(url=url+"manage_users",headers=headers)
    con = res.content.decode('utf-8')
    return json.loads(con)

def add_user(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.post(url=url+"manage_users",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)

def update_user(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.put(url=url+"manage_users",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)

def delete_user(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.delete(url=url+"manage_users",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)

def get_scheduled_tasks(access_token=None,data=None):
    headers.update({'Authorization':access_token})

    if data and "task" in data:
        res = requests.get(url=url+"schedule_vms?task={0}".format(data["task"]),headers=headers)
    elif data and "environment" in data:
        res = requests.get(url=url+"schedule_vms?env={0}".format(data["environment"]),headers=headers)
    else:
        res = requests.get(url=url+"schedule_vms",headers=headers)
    con = res.content.decode('utf-8')
    return json.loads(con)

def add_schedules_tasks(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.post(url=url+"schedule_vms",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)

def update_scheduled_tasks(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.put(url=url+"schedule_vms",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)

def delete_schedules_tasks(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.delete(url=url+"schedule_vms",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)

def get_vms(access_token=None,available=False):
    headers.update({'Authorization':access_token})
    if available:
        res = requests.get(url=url+"manage_vms",headers=headers,data=json.dumps({"status":"Y"}))
    else:
        res = requests.get(url=url+"manage_vms",headers=headers)
    con = res.content.decode('utf-8')
    return json.loads(con)

def add_vms(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.post(url=url+"manage_vms",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)

def update_vms(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.put(url=url+"manage_vms",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)

def delete_vms(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.delete(url=url+"manage_vms",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    # print(con)
    return json.loads(con)

def get_test_suites(access_token=None):
    headers.update({'Authorization':access_token})
    res = requests.get(url=url+"test_suites",headers=headers)
    con = res.content.decode('utf-8')
    # print(con)
    return json.loads(con)

def add_test_suites(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.post(url=url+"test_suites",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)

def update_test_suites(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.put(url=url+"test_suites",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)

def delete_test_suites(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.delete(url=url+"test_suites",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)

def upload_doc(access_token=None,files=None):
    headers = {'Authorization':access_token}
    res = requests.post(url=url+"docs",headers=headers,files=files)
    con = res.content.decode('utf-8')
    return json.loads(con)

def download_doc(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.post(url=url+"docs",headers=headers,data=json.dumps(data))
    con = res.content
    return con

def delete_doc(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.delete(url=url+"docs",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)

def get_envs(access_token=None):
    headers.update({'Authorization':access_token})
    res = requests.get(url=url+"envs",headers=headers)
    con = res.content.decode('utf-8')
    return json.loads(con)

def add_environemt(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.post(url=url+"envs",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    # print(con)
    return json.loads(con)

def update_environment(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.put(url=url+"envs",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    # print(con)
    return json.loads(con)

def delete_environment(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.delete(url=url+"envs",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)


def get_updates(access_token=None):
    headers.update({'Authorization':access_token})
    res = requests.get(url=url+"update",headers=headers)
    con = res.content.decode('utf-8')
    return json.loads(con)

def add_vm(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.post(url=url+"update",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    return json.loads(con)


def updates(access_token=None,data=None):
    headers.update({'Authorization':access_token})
    res = requests.put(url=url+"update",headers=headers,data=json.dumps(data))
    con = res.content.decode('utf-8')
    # print(con)
    return json.loads(con)

if __name__=="__main__":
    # print(login("aab@aa.com","welcome123"))
    res_u = updates("Q0Lvyw$oPqXPoXvxRd#C",data={"vm":"wpva","stop_vm":"Y"})
    print(res_u)
