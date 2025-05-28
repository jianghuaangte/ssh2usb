import toml
import os
import stat
from pathlib import Path

def generate_device_scripts(config_path):
    # 定义设备脚本模板
    ANDROID_TEMPLATE = """#!/usr/bin/env bash
# Android设备端口转发脚本
sleep 5s
/usr/bin/adb devices
/usr/bin/adb -s {device_serial} forward tcp:{local_port} tcp:{android_port}
/usr/bin/socat TCP-LISTEN:{socat_port},fork,reuseaddr,bind=0.0.0.0 TCP:127.0.0.1:{local_port} &
"""

    IOS_TEMPLATE = """#!/usr/bin/env bash
# iOS设备端口转发脚本
sleep 5s
/usr/bin/idevicepair -u {udid} pair
/usr/bin/iproxy -u {udid} -s 0.0.0.0 {local_port}:{ios_port} &
"""

    # 读取配置文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = toml.load(f)
    except Exception as e:
        print(f"配置文件读取失败: {str(e)}")
        return

    # 创建脚本目录
    script_dir = Path("/usr/local/scripts")
    try:
        script_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"错误: 无权限创建目录 {script_dir}，请使用sudo运行")
        return

    # 处理每个设备配置
    used_ports = set()  # 端口冲突检测
    for device in config.get('device', []):
        # 基础参数校验
        name = device.get('name', '').strip()
        dev_type = device.get('type', '').lower().strip()
        
        if not name or not dev_type:
            print(f"跳过无效配置: 设备名称或类型为空")
            continue

        try:
            # 端口冲突检测
            local_port = int(device['local_port'])
            if local_port in used_ports:
                raise ValueError(f"local_port {local_port} 已被占用")
            used_ports.add(local_port)

            # 按设备类型处理
            if dev_type == "android":
                # Android参数校验
                required_fields = ['device_serial', 'android_port', 'socat_port']
                socat_port = int(device['socat_port'])
                if socat_port in used_ports:
                    raise ValueError(f"socat_port {socat_port} 已被占用")
                used_ports.add(socat_port)
                
                content = ANDROID_TEMPLATE.format(
                    device_serial=device['device_serial'],
                    local_port=local_port,
                    android_port=device['android_port'],
                    socat_port=socat_port
                )

            elif dev_type == "ios":
                # iOS参数校验
                required_fields = ['udid', 'ios_port']
                content = IOS_TEMPLATE.format(
                    udid=device['udid'],
                    local_port=local_port,
                    ios_port=device['ios_port']
                )

            else:
                print(f"跳过设备 {name}: 不支持的类型 {dev_type}")
                continue

            # 检查必填字段
            for field in required_fields:
                if field not in device:
                    raise ValueError(f"缺少必要字段: {field}")

        except (KeyError, ValueError) as e:
            print(f"设备 {name} 配置错误: {str(e)}")
            continue
        except Exception as e:
            print(f"处理设备 {name} 时发生意外错误: {str(e)}")
            continue

        # 生成脚本文件
        script_path = script_dir / f"{name}.sh"
        try:
            with open(script_path, 'w') as f:
                f.write(content)
            script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)
            print(f"成功生成设备脚本: {script_path}")
        except PermissionError:
            print(f"权限不足，无法写入 {script_path}，请使用sudo运行")
        except Exception as e:
            print(f"生成 {script_path} 失败: {str(e)}")

if __name__ == "__main__":
    config_file = "/APP/config/config.toml"
    
    if not os.path.exists(config_file):
        print(f"错误: 配置文件不存在 - {config_file}")
        exit(1)
    
    generate_device_scripts(config_file)
