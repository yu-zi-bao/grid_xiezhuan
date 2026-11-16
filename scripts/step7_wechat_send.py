# -*- coding: utf-8 -*-
"""
第七步：微信发送携号转网预警（v29 更新 ⭐⭐⭐⭐⭐）

v29 变更：
  - 移除手动搜索"永定携出预警群"的操作指引
  - 直接使用桌面微信当前已打开的聊天窗口进行发送
  - 禁止搜索聊天、禁止导航通讯录、禁止切换聊天对象

已废弃：本脚本已由 wechat_send.py 统一脚本替代。
新代码请使用：
  python wechat_send.py --file "C:\\Users\\Administrator\\Desktop\\携转结果.xlsx"
  python wechat_send.py --message-file "D:\\携转查询\\grid_message.txt"
"""

import openpyxl
import os
import subprocess
import time

# 配置
OUTPUT_FILE = os.path.join(os.path.expanduser('~'), 'Desktop', '携转结果.xlsx')

def find_wechat_exe():
    """查找微信可执行文件（v28 改进：兼容 Weixin.exe 4.0+ 和旧版 WeChat.exe）"""
    wechat_paths = [
        r"C:\Program Files (x86)\Tencent\Weixin\Weixin.exe",
        r"C:\Program Files\Tencent\Weixin\Weixin.exe",
        r"%LOCALAPPDATA%\Tencent\Weixin\Weixin.exe",
        r"%USERPROFILE%\AppData\Local\Tencent\Weixin\Weixin.exe",
        r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe",
        r"C:\Program Files\Tencent\WeChat\WeChat.exe",
        r"%LOCALAPPDATA%\Tencent\WeChat\WeChat.exe",
        r"%USERPROFILE%\AppData\Local\Tencent\WeChat\WeChat.exe"
    ]

    for path in wechat_paths:
        path = os.path.expandvars(path)
        if os.path.exists(path):
            return path

    try:
        for exe_name in ['Weixin.exe', 'WeChat.exe']:
            result = subprocess.run(['where', '/r', 'C:\\', exe_name],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line and os.path.exists(line):
                        return line
    except:
        pass

    return None


def main():
    print("="*60)
    print("  第七步：微信发送携号转网预警（v29：直接使用当前聊天窗口）")
    print("="*60)

    print("\n  v29 更新说明：")
    print("  - 直接使用桌面微信当前已打开的聊天窗口")
    print("  - 不搜索聊天、不导航通讯录、不切换聊天对象")
    print("  - 不需要手动指定群名或聊天对象")

    print("\n" + "="*60)
    print("  推荐使用 wechat_send.py 统一脚本：")
    print("="*60)
    print()
    print("  # 发送 Excel 文件：")
    print('  python wechat_send.py --file "C:\\Users\\Administrator\\Desktop\\携转结果.xlsx"')
    print()
    print("  # 发送去重网格消息：")
    print('  python wechat_send.py --message-file "D:\\携转查询\\grid_message.txt"')
    print()
    print("  # 同时发送文件和消息：")
    print('  python wechat_send.py --file "携转结果.xlsx" --message-file "grid_message.txt"')
    print()

    # 检查微信是否运行
    wechat_exe = find_wechat_exe()
    if wechat_exe:
        print(f"  找到微信：{wechat_exe}")
    else:
        print("  ⚠️ 未找到微信安装路径，请确保微信已安装并已登录")

    print("\n" + "="*60)
    print("  v29 核心原则：")
    print("  1. 激活微信窗口（使用 wechat_window_helper 查找）")
    print("  2. 直接使用当前已打开的聊天窗口")
    print("  3. 复制文件/文本到剪贴板 → Ctrl+V 粘贴 → 回车发送")
    print("  4. 禁止搜索聊天、禁止导航通讯录、禁止切换聊天对象")
    print("="*60)

if __name__ == '__main__':
    main()