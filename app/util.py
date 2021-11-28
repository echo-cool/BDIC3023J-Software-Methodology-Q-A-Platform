from aip import AipContentCensor

""" 你的 APPID AK SK """
APP_ID = '11752086'
API_KEY = 'OfTS5Nkkbo3Qt9VuZlK0izao'
SECRET_KEY = 'sPUzVHGlHYCcqTxmcaZOINk2OOBMZlZI'

client = AipContentCensor(APP_ID, API_KEY, SECRET_KEY)
print(client.getVersion())

def check_text(text: str):
    """ 调用文本审核接口 """
    result = client.textCensorUserDefined(text)
    return result
