import requests
from bs4 import BeautifulSoup
import re
import os

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
# 6.73mb/s
speed_pattern = r'\d+\.\d+[Mm][Bb]/s'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

if os.path.exists('speed.txt'):
    os.remove('speed.txt')

# 创建一个文件来存储IP地址
def extract_ips():
    result = {}
    # 目标URL列表
    urls = ['https://api.uouin.com/cloudflare.html','https://ip.164746.xyz']
    for url in urls:
        try:
            # 发送HTTP请求获取网页内容
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"请求网站 [{url}] 发生错误: {e}")
            continue

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://api.uouin.com/cloudflare.html' or url == 'https://ip.164746.xyz':
            elements = soup.find_all('tr')
        else:
            elements = soup.find_all('li')
        
        # 遍历所有元素,查找IP地址
        for element in elements:
            element_text = element.get_text()
            ip_matches = re.findall(ip_pattern, element_text)
            speed_matches = re.findall(speed_pattern, element_text)
            if len(ip_matches) > 0 and len(speed_matches) > 0:
                speed_matches = float(speed_matches[0].replace("MB/s", "").replace("mb/s", ""))
                if speed_matches > 3.0:
                    result[ip_matches[0]] = {
                        "url": url,
                        "speed": speed_matches
                        }
    return result

data = extract_ips()
with open('ip.txt', 'w') as file:
    for key, value in data.items():
        file.write(f"{key}\n")

with open('speed.txt', 'w') as file:
    for key, value in data.items():
        file.write(f"{value['url']}: {key} -- {value['speed']}mb/s\n")




print('IP地址已保存到ip.txt文件中。')
