## 宝塔面板Docker镜像说明

因于2024年6月以后Centos7系统官方已停止维护，故更新基础镜像为debian11；

该镜像基于Debian11构建，使用宝塔Linux正式版 7.7.0官方纯净版和宝塔面板9.0.0LTS稳定版制作；

多种不同版本(含开心版)，适配x86和arm双架构。

### 特别说明
1. 纯脚本构建，中间无人工参与，纯净无残留，无后门；
2. 利用环境变量可以自定义设置端口，用户名及密码；
3. 数据可以持久化存储，具体方法参照下面步骤；
4. 本质为自用存档，是否使用取决于自己。

### Debian11版本

#### debian11.v1.0:无环境优化版
1. 基于宝塔面板7.7.0，纯净无插件、无环境；
2. 可以使用环境变量自定义端口，用户名和密码；
3. 屏蔽手机号，取消强制绑定账号手机；
4. 优化去除面板日志与绑定域名上报；
5. 可去除登录安全入口，或通过环境变量自定义；
6. 修复SSH，可正常开启WEB终端；

#### debian11.v2.0:lnmp基础版
1. 在v1.0版本基础上增加lnmp环境；
2. Nginx1.22.1；
3. MySQL5.7.44；
4. PHP7.4；
5. Pure-Ftpd 1.0.49；
6. phpMyAdmin 5.0
debian11.v3.0:lnmp解锁版

1. 基于v2.0lnmp环境版；
2. 已解锁专业及企业版插件；
3. 版本原因，无法安装第三方插件。
4. 解锁方案为脚本自动修改特定文件达成。
debian11.v4.0:lnmp开心版

1. 使用成熟的开心版成品脚本构建；
2. 安装的环境同v2.0；
3. 此开心版为业界知名的解决方案（bt.sb）。
debian11.v5.0:lnmp稳定版

1. 基于9.0.0LTS稳定版成熟的开心版成品脚本构建；
2. 安装的环境Nginx1.24|MySQL5.7|PHP8.0|Pure-Ftpd 1.0|phpMyAdmin 5.0；
3. 此开心版为业界知名的解决方案（bt.sb）。
4. 新版无法取消入口，默认入口/admin,可通过环境变量自定义。
debian11.v6.0:lnmp官方版

1. 基于官方9.0.0LTS稳定版脚本构建；
2. 安装的环境Nginx1.24|MySQL5.7|PHP8.0|Pure-Ftpd 1.0|phpMyAdmin 5.0；
3. 官方脚本，放心无后门。
4. 新版无法取消入口，默认入口/admin，,可通过环境变量自定义。
提示：

v1.0-v3.0：采用宝塔面板7.7.0官方版构建，放心无后门；

v4.0: 采用bt.sb的7.7.0 企业版【纪念版】构建；

v5.0: 采用bt.sb的9.0.0 LTS 稳定版构建，是否使用自行决定

v6.0: 采用官方9.0.0 LTS 稳定版构建，需登录自己宝塔账号。

Centos7版本（不再维护）：
base基础版

1. 宝塔面板7.7，无插件；2. 无启动项，只作为迭代基础镜像使用
v1:基础优化版

1. 增加环境变量用于自定义端口，用户名和密码；2. 屏蔽手机号，取消强制绑定账号手机；3. 已去除登录安全入口；4. 修复SSH。可正常开启WEB终端；
v2:安装环境（lnmp）

1. 基于v1镜像构建；2. 安装lnmp环境：Nginx1.22|MySQL5.7|PHP7.4|Pure-Ftpd 1.0|phpMyAdmin 4.8；
v3:最新开心版

基于V2环境版升级到最新的8.05开心版
### 宝塔面板Docker镜像部署

## 一、简单化部署
```bash
docker run -itd \
--name=baota \
--privileged=true \
-p 8888:8888 \
-e "PANEL_PORT=8888" \
-e "PANEL_USERNAME=username" \
-e "PANEL_PASSWORD=password" \
-e "PANEL_LOGIN=admin" \
bugseeker/baota
默认账号:username，密码：password，入口：/admin

二、 标准化部署（数据持久化）
为了避免数据丢失，可以将容器内的文件映射到宿主机的目录中（之后安装的 Nginx、MySQL 等服务均会挂载到宿主机目录）。该方法是 Docker 部署宝塔面板的最优方案，可以在生产环境中运行。

数据持久化操作过程

/www为宝塔面板程序目录(内部包括/sever软件安装目录等), 如果想持久化, 第一次运行docker时不要映射/www, 因为映射的/www没有系统需要的文件会报错.

1、 转移文件

第一种方法：（容器内转移）

先将宿主机持久化目录如/mnt/appdata/baota/www映射到容器内临时目录如/www1 (容器内会自动'新建'/www1)；

docker run -itd \
--name baota \
--privileged=true \
-p 8888:8888 \
-v /mnt/appdata/baota/www:/www1 \
bugseeker/baota:amdv5
等docker成功运行后, 在容器中将/www内所有文件复制到/www1 (也就是复制到了宿主机/mnt/appdata/baota/www内);

cp -a /www/* /www1
然后重新拉取容器, 并添加/mnt/appdata/baota/www => /www的映射, 实现/www文件的持久化

第二种方法（宿主机命令转移）

首先按最简方案创建一个测试容器（为保存宝塔文件到宿主机目录中）
docker run -itd \
--name baota \
--privileged=true \
-p 8888:8888 \
bugseeker/baota:amdv5
将 Docker 容器中需持久化的文件拷贝至宿主机
#CP命令使用方法：
docker cp -a 容器名称:容器内的路径 宿主机路径
# 网站数据目录（新装可不执行此条）
docker cp -a -L baota:/www/wwwroot /mnt/appdata/baota/wwwroot
# 宝塔程序目录
docker cp -a -L baota:/www /mnt/appdata/baota
2、删除测试容器

拷贝完成后删除创建的测试容器

docker stop baota && docker rm baota
3、创建容器

创建宝塔面板容器，并将宿主机目录映射至容器中（自行输入面板的 端口号、用户名 和 密码 后即可完成部署）

docker run -itd \
--name=baota \
--restart=always \
--privileged=true \
-p 8888:8888 \
-p 443:443 \
-p 80:80 \
-e "PANEL_PORT=8888" \
-e "PANEL_USERNAME=username" \
-e "PANEL_PASSWORD=password" \
-e "PANEL_LOGIN=admin" \
-e TZ="Asia/Shanghai" \
-v /mnt/appdata/baota/www:/www \
-v /mnt/appdata/baota/www/wwwroot:/www/wwwroot \
bugseeker/baota:amdv5
注意：

不设置环境变量的情况下默认的账号：username,密码：password,入口地址：/admin
8888端口要和环境变量的端口对应
登陆地址: https://服务器的ip地址:您输入的端口号/入口地址
首次启动多等会，如果无法登录切换http或https

部署成功！