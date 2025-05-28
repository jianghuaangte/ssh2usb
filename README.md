## 支持架构
- x86_64
- arm64

## 构建

1 克隆项目

2 进入
```shell
cd ssh2usb
```

3 构建镜像
```shell
docker build -t ssh2usb:latest .
```


## 使用
支持 host 网络模式但连接时只能用主机自身进行连接
```shell
docker-compose up -d
```


先运行一次获取设备信息

获取 ID 信息

```shell
docker exec ssh2usb lsusb
```

唤醒 iOS 信任授权并查看 iOS 设备的 UDID

```shell
docker exec ssh2usb /usr/bin/idevicepair pair
```

唤醒 Android 设备授权

```shell
docker exec ssh2usb adb devices
```

把获取到的信息在配置文件中修改
```shell
/path/to/dir/config.toml
```

## Doceker 运行

```shell
version: '3.8'

services:
  your-app:
    image: freedomzzz/ssh2usb:latest
    container_name: ssh2usb
    working_dir: /APP
    restart: always
    privileged: true               # 需要特权模式访问 USB 设备
    volumes:
      - /path/to/dir:/APP/config   # 配置文件
      - /dev/bus/usb:/dev/bus/usb  # 挂载 USB 设备 必须要有这个
    ports:
      - "8067:8023"
      - "8068:8024"
    environment:
      - TZ=Asia/Shanghai
      - ENV=production
```

注意事项
- 只有配置信息填写正确才会触发插拨授权提示。手动也是可以的。
