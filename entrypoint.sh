#!/usr/bin/env bash

# 默认配置文件
bash /APP/scripts/copy-default-config.sh

# 定义配置文件路径
CONFIG_FILE="/APP/config/config.toml"

# 检查配置文件是否存在
if [ ! -f "$CONFIG_FILE" ]; then
  echo "错误：配置文件 $CONFIG_FILE 不存在"
  exit 1
fi


echo "配置端口映射..."
# 清理旧文件
# udev 规则
# 前置命令
# udev 中指定的执行文件
# 后置命令
bash /APP/scripts/clean.sh \
&& python3 /APP/scripts/udev_rules.py \
&& bash /APP/scripts/before_cmd.sh \
&& python3 /APP/scripts/executable.py \
&& bash /APP/scripts/after_cmd.sh

# 持久化运行
exec tail -f /dev/null
