#!/usr/bin/env bash
for i in {1..10}; do
  /usr/sbin/usbmuxd
  if [ $? -eq 0 ]; then
    echo "usbmuxd 成功执行！"
    break # 如果成功就退出循环，继续执行后面的命令
  else
    echo "第 $i 次尝试失败，等待2秒..."
    sleep 3
  fi
done

if [ $? -ne 0 ]; then
  echo "命令执行失败，退出脚本。"
  exit 1
else
  echo "脚本继续执行..."
fi

/etc/init.d/udev restart
