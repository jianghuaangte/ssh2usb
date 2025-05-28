#!/usr/bin/env bash
# 重载配置和生效
/usr/bin/udevadm control --reload-rules && /usr/bin/udevadm trigger
