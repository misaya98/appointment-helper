import time
import warnings

import requests
import json

import urllib3

warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

# your params

param_dict = {
    "姓名": "",
    "部门": "",
    "工号": ""
}
reg_id = 'your_reg_id'
user_token = 'your_user_token'


def get_detail(reg_id, user_token):
    url = "https://reglist.uidev.tech/Appointment/Detail?bt=" + reg_id

    payload = json.dumps({
        "id": reg_id
    })
    headers = {
        'authority': 'reglist.uidev.tech',
        'scheme': 'https',
        'path': '/Appointment/Detail?bt=' + reg_id,
        'content-length': '23',
        'uiyee-bt': reg_id,
        'wechat-miniprogram-appid': 'wx349100408516a755',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30626',
        'content-type': 'application/json',
        'referer': 'https://servicewechat.com/wx349100408516a755/519/page-frame.html',
        'wechat-miniprogram-login-token': user_token,
        'client-time-zone-offset': '-480',
        'xweb_xhr': '1',
        'wechat-miniprogram-version': '',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    # print ("get_detail :" + str(response.json()))
    return response.json()


def get_params(reg_id, user_token):
    url = "https://reglist.uidev.tech/Register/Participant/ParamsV3?bt=" + reg_id

    payload = json.dumps({
        "registerId": reg_id,
        "sortOrder": -1,
        "isReadyParticipate": False
    })
    headers = {
        'uiyee-bt': reg_id,
        'wechat-miniprogram-appid': 'wx349100408516a755',
        'uiyee-request-id': '6891266984710010-7012484842790590-1691398484279',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30626',
        'content-type': 'application/json',
        'wechat-miniprogram-login-token': user_token,
        'wechat-miniprogram-version': '',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    return response.json()


def build_partinfo(params):
    part_infos = []
    for part_setting in params['data']['registerPartSettings']:
        part_info = {"registerId": part_setting['registerId'],
                     "registerPartSettingId": part_setting['id'],
                     "partSettingId": part_setting['partSettingId'],
                     "name": part_setting['name'],
                     "inputType": part_setting['inputType'],
                     "inputMode": part_setting['inputMode'],
                     "sortOrder": part_setting['sortOrder'],
                     "multiple": part_setting['multiple'],
                     "required": part_setting['required'],
                     "items": [],
                     "display": "",
                     "value": "",
                     "itemInputValues": [],
                     "isHide": part_setting['isHide'],
                     "isHideByLogic": False,
                     "isNucleicAcidTime": part_setting['isNucleicAcidTime']}
        if part_setting['name'] in param_dict:
            part_info['display'] = param_dict[part_setting['name']]
            part_info['value'] = param_dict[part_setting['name']]

        part_infos.append(part_info)
    return part_infos


def participate(reg_id, appointmentItemId, part_infos):
    class ParticipateRequest:
        def __init__(self, register_id, appointment_item_id, part_infos, remark="", reason="", template_ids=None):
            self.id = None
            self.registerId = register_id
            self.appointmentItemId = appointment_item_id
            self.sortOrder = -1
            self.active = True
            self.partInfos = part_infos
            self.remark = remark
            self.reason = reason
            self.templateIds = template_ids or []

    request = ParticipateRequest(reg_id, appointmentItemId, part_infos)
    url = "https://reglist.uidev.tech/Appointment/Participate?registerId=" + reg_id + "&bt=" + reg_id
    payload = json.dumps(request.__dict__)

    headers = {
        'uiyee-bt': reg_id,
        'wechat-miniprogram-appid': 'wx349100408516a755',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30626',
        'content-type': 'application/json',
        'wechat-miniprogram-login-token': user_token,
        'wechat-miniprogram-version': '',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    # print(response.text)
    return response.json()


def find_free_appointment(reg_id, user_token):
    waitlist = []
    detail = get_detail(reg_id, user_token)
    appointments = detail['data']['register']['appointmentItems']
    for item in appointments:
        if item['stock'] > item['participateCount'] and not item['isExpired']:
            print('appointmentId:' + str(item['id']) + '空闲')
            waitlist.append(item['id'])
    return waitlist


def main():
    start_time = time.time()
    freelist = find_free_appointment(reg_id, user_token)
    while len(freelist) == 0:
        print('无空闲')
        freelist = find_free_appointment(reg_id, user_token)
        time.sleep(5)
    print('空闲:  ' + str(freelist))

    params = get_params(reg_id, user_token)
    # print('params:  ' + json.dumps(params))
    part_infos = build_partinfo(params)
    for appointmentId in freelist:
        print("start to participate")
        res = participate(reg_id, appointmentId, part_infos)
        if res['state'] == 'OK':
            print("预约成功!!!" + str(appointmentId))
            time.sleep(5)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("代码执行耗时: {:.2f} 秒".format(elapsed_time))


if __name__ == '__main__':
    main()
