#!/bin/bash
if [ ! -f "/etc/ssh/ssh_host_rsa_key" ];then
    ssh-keygen -t rsa -N '' -q -f /etc/ssh/ssh_host_rsa_key
fi
if [ ! -f "/root/.ssh/id_rsa_63322" ];then
    ssh-keygen -t rsa -N '' -q -f /root/.ssh/id_rsa_63322
    cat /root/.ssh/id_rsa_63322.pub >> /root/.ssh/authorized_keys
    _f1='{"username": "root", "pkey": "'
    _f2=$(sed s/$/'\\n'/ /root/.ssh/id_rsa_63322 | tr -d '\r\n')
    _f3='", "is_save": "1", "c_type": "True", "host": "127.0.0.1", "password": "", "port": 63322}'
    echo "${_f1}${_f2}${_f3}" | base64 | tr -d '\r\n '| od -An -tx1 | tr -d '\r\n ' > "/www/server/panel/config/t_info.json"
fi

/usr/sbin/sshd
/usr/sbin/cron
#for file in /etc/init.d/*; do
#    if [ -x "$file" ]; then 
#        "$file" restart
#    fi
#done
# 运行你的Python脚本
python3 /app/script.py &
# 执行宝塔面板的相关命令
#bt 3
/etc/init.d/nginx start
/etc/init.d/mysqld start
/etc/init.d/php-fpm-80 start
/etc/init.d/pure-ftpd start

# 保持容器运行
tail -f /dev/null
