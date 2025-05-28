#!/usr/bin/env bash
# 清理旧的生成文件

# 定义需要处理的目录数组
directories=(
  "/etc/udev/rules.d"
  "/usr/local/scripts"
  "/APP/info/usb-list"
)

# 遍历所有目录进行处理
for dir in "${directories[@]}"; do
  # 判断目录是否存在
  if [[ -d "$dir" ]]; then
    echo "目录 $dir 已存在"

    # 检查目录是否非空
    if [[ $(ls -A "$dir") ]]; then
      echo "正在清理 $dir 中的内容..."
      # 安全删除目录内容（包括隐藏文件）
      find "$dir" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
      echo "已清除 $dir 下所有内容"
    else
      echo "$dir 是空目录，无需清理"
    fi
  else
    # 创建目录并设置权限（按需修改）
    echo "创建目录 $dir"
    mkdir -p "$dir"
    chmod 755 "$dir" # 示例权限设置，可根据实际需求调整
  fi
done

# 可选：添加权限验证
for dir in "${directories[@]}"; do
  if [[ ! -w "$dir" ]]; then
    echo "警告：当前用户对 $dir 没有写权限！"
    exit 1
  fi
done

echo "所有目录处理完成"
exit 0
