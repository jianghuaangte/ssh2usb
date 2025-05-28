# Dockerfile
FROM ubuntu:22.04

# 一次性完成系统级配置
RUN set -eux; \
    # 设置时区
    export TZ=Asia/Shanghai; \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone; \
    # 更换镜像源
    sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g; s@//.*ports.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list; \
    # 安装基础依赖并清理
    apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        usbutils \
        udev \
        socat \
        android-tools-adb \
        libimobiledevice6 \
        libimobiledevice-utils \
        libusbmuxd-tools \
        ifuse \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean autoclean

# Python 依赖安装
RUN pip3 install --no-cache-dir tomli toml \
    -i https://pypi.mirrors.ustc.edu.cn/simple/

COPY default-config.toml /APP/
COPY scripts/* /APP/scripts/
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh  # 确保可执行权限

CMD ["/entrypoint.sh"]
