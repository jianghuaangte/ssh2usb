#!/usr/bin/env bash

# 配置路径参数
CONFIG_DIR="/APP/config"
TARGET_FILE="${CONFIG_DIR}/config.toml"
SOURCE_FILE="/APP/default-config.toml"

# 创建配置目录（如果不存在）
if [ ! -d "$CONFIG_DIR" ]; then
  mkdir -p "$CONFIG_DIR"
  echo "已创建配置目录: $CONFIG_DIR"
fi

# 初始化默认配置文件（如果不存在）
if [ ! -f "$TARGET_FILE" ]; then
  if cp "$SOURCE_FILE" "$TARGET_FILE"; then
    echo "已初始化默认配置文件: $TARGET_FILE"
  else
    echo "错误: 无法创建配置文件" >&2
    exit 1
  fi
fi
