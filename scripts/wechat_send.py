# -*- coding: utf-8 -*-
"""
微信发送统一脚本（v29 新增 ⭐⭐⭐⭐⭐）

v29 核心变更：
  - 直接使用桌面微信当前已打开的聊天窗口进行发送
  - 禁止搜索聊天、禁止导航通讯录、禁止切换聊天对象
  - 不需要人工指定群名或聊天对象
  - 统一文件发送和文本消息发送流程

用法：
  # 发送文件
  python wechat_send.py --file "C:\\Users\\Administrator\\Desktop\\携转结果.xlsx"

  # 发送文本消息（直接指定文本）
  python wechat_send.py --message "测试消息"

  # 发送文本消息（从文件读取）
  python wechat_send.py --message-file "D:\\携转查询\\grid_message.txt"

  # 同时发送文件和文本消息（先发文件，再发消息）
  python wechat_send.py --file "C:\\path\\to\\file.xlsx" --message-file "C:\\path\\to\\message.txt"
"""

import sys
import os
import time
import struct
import argparse
import win32gui
import win32con
import win32clipboard
import win32api

# 添加脚本目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from wechat_window_helper import find_wechat_window, activate_window


def set_clipboard_text(text):
    """设置剪贴板文本内容（CF_UNICODETEXT）"""
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, text)
        win32clipboard.CloseClipboard()
        return True
    except Exception as e:
        print(f"剪贴板文本设置失败: {e}")
        return False


def set_clipboard_file(file_path):
    """设置剪贴板文件内容（CF_HDROP 格式，用于文件复制粘贴）"""
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return False

    try:
        # DROPFILES 结构: pFiles(4) + pt.x(4) + pt.y(4) + fNC(4) + fWide(4) = 20 bytes
        # 文件列表: 宽字符，每个路径以 \x00 结尾，整个列表以额外 \x00\x00 结尾
        files = file_path + '\x00\x00'
        data = struct.pack('IIIII', 20, 0, 0, 0, 1) + files.encode('utf-16-le')

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_HDROP, data)
        win32clipboard.CloseClipboard()
        return True
    except Exception as e:
        print(f"剪贴板文件设置失败: {e}")
        return False


def send_key(vk_code, down_time=0.05, up_time=0.05):
    """发送单个按键"""
    win32api.keybd_event(vk_code, 0, 0, 0)
    time.sleep(down_time)
    win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(up_time)


def send_ctrl_v():
    """发送 Ctrl+V 粘贴"""
    win32api.keybd_event(0xA2, 0, 0, 0)  # Ctrl down
    time.sleep(0.05)
    win32api.keybd_event(0x56, 0, 0, 0)  # V down
    time.sleep(0.05)
    win32api.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)  # V up
    time.sleep(0.05)
    win32api.keybd_event(0xA2, 0, win32con.KEYEVENTF_KEYUP, 0)  # Ctrl up
    time.sleep(0.5)


def send_enter():
    """发送回车键"""
    send_key(0x0D, 0.05, 0.5)


def activate_wechat():
    """激活微信窗口（v29：直接使用当前已打开的窗口，不搜索聊天）"""
    windows = find_wechat_window()
    if not windows:
        print("✗ 未找到微信窗口，请确保微信已登录并运行")
        return False

    if not activate_window(windows[0][0]):
        print("✗ 微信窗口激活失败，终止发送")
        return False
    
    # 二次确认：检查微信是否确实在前台
    time.sleep(0.5)
    fg = win32gui.GetForegroundWindow()
    fg_title = win32gui.GetWindowText(fg)
    if "微信" not in fg_title and "WeChat" not in fg_title:
        print(f"✗ 前台窗口不是微信（当前前台: {fg_title}），终止发送")
        return False
    
    print(f"✓ 微信窗口已激活：{fg_title}")
    return True


def send_file(file_path):
    """
    发送文件到当前微信聊天窗口

    流程：激活微信 → 复制文件到剪贴板 → Ctrl+V 粘贴 → 回车发送
    """
    print(f"\n[发送文件] {file_path}")

    # 1. 激活微信窗口
    if not activate_wechat():
        return False

    # 2. 复制文件到剪贴板
    if not set_clipboard_file(file_path):
        print("✗ 文件复制到剪贴板失败")
        return False
    print("✓ 文件已复制到剪贴板")

    # 3. Ctrl+V 粘贴文件
    time.sleep(0.5)
    send_ctrl_v()
    time.sleep(2)  # 等待微信处理文件

    # 4. 按回车发送
    send_enter()
    time.sleep(2)

    print("✓ 文件发送完成")
    return True


def send_text_message(message_text):
    """
    发送文本消息到当前微信聊天窗口

    流程：激活微信 → 复制文本到剪贴板 → Ctrl+V 粘贴 → 回车发送
    """
    print(f"\n[发送文本消息] 消息长度: {len(message_text)} 字符")

    # 1. 激活微信窗口
    if not activate_wechat():
        return False

    # 2. 复制文本到剪贴板
    if not set_clipboard_text(message_text):
        print("✗ 文本复制到剪贴板失败")
        return False
    print("✓ 文本已复制到剪贴板")

    # 3. Ctrl+V 粘贴文本
    time.sleep(0.5)
    send_ctrl_v()
    time.sleep(1)

    # 4. 按回车发送
    send_enter()
    time.sleep(1)

    print("✓ 文本消息发送完成")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='微信发送统一脚本（v29：直接使用当前聊天窗口，不搜索不导航）'
    )
    parser.add_argument('--file', help='要发送的文件路径')
    parser.add_argument('--message', help='要发送的文本消息（直接指定）')
    parser.add_argument('--message-file', help='包含要发送文本消息的文件路径')

    args = parser.parse_args()

    print("=" * 60)
    print("  微信发送统一脚本（v29：直接使用当前聊天窗口）")
    print("  - 不搜索聊天、不导航通讯录、不切换聊天对象")
    print("  - 直接使用桌面微信当前已打开的聊天窗口")
    print("=" * 60)

    if not args.file and not args.message and not args.message_file:
        print("✗ 请指定要发送的文件或消息")
        parser.print_help()
        return

    success = True

    # 先发送文件
    if args.file:
        if not send_file(args.file):
            success = False

    # 再发送文本消息
    if args.message:
        if not send_text_message(args.message):
            success = False

    if args.message_file:
        if not os.path.exists(args.message_file):
            print(f"✗ 消息文件不存在: {args.message_file}")
            success = False
        else:
            with open(args.message_file, 'r', encoding='utf-8') as f:
                message = f.read()
            if not send_text_message(message):
                success = False

    print("\n" + "=" * 60)
    if success:
        print("  ✓ 全部发送完成！")
    else:
        print("  ✗ 部分发送失败，请检查日志")
    print("=" * 60)


if __name__ == '__main__':
    main()