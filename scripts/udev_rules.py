import toml
import os

def generate_udev_rules(config_path):
    # 读取并解析TOML配置文件
    with open(config_path, 'r', encoding='utf-8') as f:
        config = toml.load(f)
    
    # 提取所有device配置块
    devices = config.get('device', [])
    
    for device in devices:
        # 获取必要参数
        name = device.get('name', '').strip()
        vendor_id = device.get('vendor_id', '').strip().lower()
        product_id = device.get('product_id', '').strip().lower()
        
        # 校验必要字段
        if not all([name, vendor_id, product_id]):
            print(f"警告: 跳过不完整设备配置 {device}")
            continue
        
        # 生成udev规则内容
        rule_content = (
            f'SUBSYSTEM=="usb", '
            f'ATTRS{{idVendor}}=="{vendor_id}", '
            f'ATTRS{{idProduct}}=="{product_id}", '
            f'ACTION=="add", '
            f'RUN+="/usr/local/scripts/{name}.sh"\n'
        )
        
        # 生成完整文件路径
        rules_dir = "/etc/udev/rules.d"
        filename = f"99-{name}.rules"
        file_path = os.path.join(rules_dir, filename)
        
        try:
            # 写入规则文件（需要sudo权限）
            with open(file_path, 'w') as f:
                f.write(rule_content)
            print(f"成功生成: {file_path}")
        except PermissionError:
            print(f"错误: 权限不足，请使用sudo运行脚本")
            break
        except Exception as e:
            print(f"写入文件 {file_path} 失败: {str(e)}")

if __name__ == "__main__":
    config_file = "/APP/config/config.toml"  # 注意原文件名的拼写错误
    
    # 检查配置文件是否存在
    if not os.path.exists(config_file):
        print(f"错误: 配置文件 {config_file} 不存在")
        exit(1)
    
    generate_udev_rules(config_file)
