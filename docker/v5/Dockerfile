# 使用debian 11作为基础镜像
FROM debian:11

# 维护者和其他元数据标签
LABEL maintainer="Ruoyer" version="5.0" description="Baota9.0.0LTS"

# 替换镜像源（可选）
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list

# 安装基础依赖和工具
RUN apt-get update && apt-get install -y dos2unix wget openssh-server openssh-client curl python3 python3-pip cron iproute2 iputils-ping \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir /app

# 创建必要的目录和符号链接
RUN mkdir -p /www/letsencrypt /www/init.d /www/wwwroot /run/sshd \
    && ln -s /www/letsencrypt /etc/letsencrypt \
    && mv /etc/init.d /etc/init.d.bak \
    && ln -s /www/init.d /etc/init.d

# 设置环境变量
ENV PANEL_PORT=8888

# 安装 Python包和宝塔面板
RUN pip3 install psutil \
    && echo 'Port 63322' > /etc/ssh/sshd_config \
    && wget -O install.sh https://downlts.bt.sb/install/install_lts.sh \
    && echo y | bash install.sh \
    && rm -f install.sh \
    && apt-get clean

# 运行设置脚本并配置宝塔面板
RUN cd /app \
    # 修复网页终端
    && echo '["linuxsys", "webssh"]' > /www/server/panel/config/index.json
# 安装基础环境
RUN cd /app \
    && bash /www/server/panel/install/install_soft.sh 0 install php 8.0 \
    && bash /www/server/panel/install/install_soft.sh 0 install nginx 1.24 \
    && bash /www/server/panel/install/install_soft.sh 0 install mysql 5.7 \
    && apt-get clean
# 安装扩展环境
RUN cd /app \    
    && bash /www/server/panel/install/install_soft.sh 1 install pureftpd 1.0 \
    && bash /www/server/panel/install/install_soft.sh 1 install phpmyadmin 5.1 || true 

# 复制并转换脚本格式
COPY script.py /app/script.py
COPY entrypoint.sh /app/entrypoint.sh
RUN dos2unix /app/entrypoint.sh \
    && dos2unix /app/script.py \
    && chmod +x /app/entrypoint.sh \
    && chmod +x /app/script.py

# 设置工作目录并暴露端口
WORKDIR /www/wwwroot
EXPOSE $PANEL_PORT 888 21 20 443 80 63322

# 容器启动时运行的命令
CMD ["/app/entrypoint.sh"]
HEALTHCHECK --interval=5s --timeout=3s CMD curl -fs http://localhost:$PANEL_PORT/ || exit 1