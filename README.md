## bind 配置dlz 支持

### bind编译安装,并支持Percona Server

```
https://www.isc.org/bind-9-11-arm/
yum -y install  gcc GeoIP GeoIP-update GeoIP-devel openssl-devel
wget -O bind-9.11.2.tar.gz  https://www.isc.org/downloads/file/bind-9-11-2/
 ./configure --prefix=/opt/bind --with-dlz-mysql=/opt/Percona-Server-5.7.17-11-Linux.x86_64.ssl101  --with-geoip=yes --enable-querytrace --enable-getifaddrs --enable-epoll  --enable-openssl-hash --enable-largefile --enable-threads=no  --with-dlopen=yes --with-openssl=yes --enable-openssl-hash=yes --with-python
cd /usr/include;ln -s /opt/Percona-Server-5.7.17-11-Linux.x86_64.ssl101/include mysql
sed -i '/DLZDRIVER_LIBS/s/mysql//;s/lmysqlclient/lperconaserverclient/' bin/named/Makefile
sed -i 's/lmysqlclient/lperconaserverclient/g' configure contrib/dlz/modules/mysql/Makefile contrib/dlz/modules/mysqldyn/Makefile contrib/dlz/config.dlz.in
sed -i '/MYSQL_LIBS=/s/=/=-L\/opt\/Percona-Server-5.7.17-11-Linux.x86_64.ssl101\/lib  /' contrib/dlz/modules/mysqldyn/Makefile
make && make install
echo "/opt/Percona-Server-5.7.17-11-Linux.x86_64.ssl101/lib" > /etc/ld.so.conf.d/mysql.conf
```

## 安装

```
pip instatll -r requirements.txt

修改默认配置bindmanager/config/app.cfg
```

## 数据库

```
导入bind.sql
mysql < bind.sql
```

## 运行

```
nohup python runserver.py &>>access_log 
```

## 登录

```
默认登录用户名和密码
admin 0123456789
```

## 功能概览

![首页](https://user-images.githubusercontent.com/7885342/92895683-4cb86200-f44e-11ea-9fc5-83260b200ee2.png)
![域名管理](https://user-images.githubusercontent.com/7885342/92895697-4fb35280-f44e-11ea-8d5d-535f6e47158a.png)
![用户管理](https://user-images.githubusercontent.com/7885342/92895701-5215ac80-f44e-11ea-8ad2-20dff4f769b2.png)
