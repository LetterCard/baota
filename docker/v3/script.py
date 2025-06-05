#!venv/bin/python
# -*- coding: utf-8 -*-

import os
import time
import subprocess

def get_env_input():
    data = {}
    data['port'] = os.getenv('PANEL_PORT', '8888')
    data['username'] = os.getenv('PANEL_USERNAME', 'username')
    data['password'] = os.getenv('PANEL_PASSWORD', 'password')
    data['login'] = os.getenv('PANEL_LOGIN', '')
    return data

def run_command(command, input_data):
    """
    执行外部命令，向其发送交互式输入，并打印输出结果。
    """
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate(input=input_data)

    if process.returncode == 0:
        print("命令输出：\n", stdout)
    else:
        print("命令错误输出：\n", stderr)

def set_admin_path(login):
    file_path = '/www/server/panel/data/admin_path.pl'
    
    # 将 "/" 和 login 变量值组合并写入文件
    login_path = f"/{login}"  # 前面添加 "/"
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(login_path)
    
    print(f"面板入口更改为: {login_path}")

def bt_init(port, username, password,login):
    print('正在设置面板端口')
    # 发送选择命令（8）和端口号
    run_command(["bt", "8"], "{0}\n".format(port))
    
    print('正在设置面板用户名')
    # 假设设置用户名的选项是6，后续需要替换成实际的选项代码
    run_command(["bt", "6"], "{0}\n".format(username))

    print('正在设置面板密码')
    # 假设设置密码的选项是5，后续需要替换成实际的选项代码
    run_command(["bt", "5"], "{0}\n".format(password))
    
    print('正在设置面板入口')
    # 如果 login 是默认值 'admin'，执行 bt 11，否则执行 bt 28
    if login == '':
        run_command(["bt", "11"], "")
    else:
        #run_command(["bt", "28"], "/{0}\n".format(login))
        set_admin_path(login)  # 调用新函数将环境变量值写入文件

def main():
    data = get_env_input()
    #检测端口是否合法
    try:
        port = int(data['port'])
        if 0 <= port <= 65535:
            port = str(port)
    except:
        print('您输入的端口号有误，请重新创建 Docker 容器并输入正确端口号')
        return False
    
    #检测用户名是否合法
    if len(data['username']) < 3:
        print('密码长度不能小于 3 位，请重新创建 Docker 容器并输入正确用户名')
        return False    
    #检测密码是否合法
    if len(data['password']) < 5:
        print('密码长度不能小于 5 位，请重新创建 Docker 容器并输入正确密码')
        return False
    
    #判断是否是第一次初始化
    if not os.path.isfile('/app/init.txt'):
        bt_init(data['port'], data['username'], data['password'], data['login'])
        os.system('touch /app/init.txt')
        print('初始化设置成功\n')
    os.system('/etc/init.d/bt restart')
    print('\n宝塔面板已启动\n')
    command = "ip addr | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | grep -E -v '^127\.|^255\.|^0\.' | head -n 1"
    process = os.popen(command)
    ip = process.read().strip()  # 读取输出并去除首尾空白字符
    print('面板链接: http://' + ip + ':' + data['port']+'/'+ data['login'])
    print('用户名: ' + data['username'])
    print('密码: ' + data['password'])

     #while True:
        #time.sleep(60 * 60 * 24 * 365 * 100)

if __name__ == '__main__':
    main()
