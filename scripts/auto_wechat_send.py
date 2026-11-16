# -*- coding: utf-8 -*-
"""
微信发送消息（v29 更新 ⭐⭐⭐⭐⭐）

v29 变更：
  - 移除搜索"永定携出预警群"的步骤
  - 直接使用桌面微信当前已打开的聊天窗口进行发送
  - 禁止搜索聊天、禁止导航通讯录、禁止切换聊天对象

已废弃：本脚本已由 wechat_send.py 统一脚本替代。
新代码请使用：
  python wechat_send.py --message-file "消息文件路径"
  python wechat_send.py --file "文件路径"
"""

import win32gui
import win32con
import win32clipboard
import win32api
import time

def set_clipboard_text(text):
    """设置剪贴板内容"""
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, text)
        win32clipboard.CloseClipboard()
        return True
    except Exception as e:
        print("剪贴板设置失败:", str(e))
        return False

def main():
    print("="*60)
    print("  微信发送消息（v29：直接使用当前聊天窗口）")
    print("="*60)

    # 准备消息（示例，实际使用时从文件读取）
    message = "【携号转网预警】\n\n请使用 wechat_send.py 统一脚本发送实际消息"

    # 1. 查找并激活微信窗口（v29：直接使用当前窗口，不搜索聊天）
    print("\n[1/3] 正在激活微信窗口...")
    from wechat_window_helper import find_wechat_window, activate_window
    windows = find_wechat_window()

    if not windows:
        print("✗ 未找到微信窗口")
        return

    activate_window(windows[0][0])
    print("✓ 微信窗口已激活（使用当前已打开的聊天窗口）")

    # 2. 粘贴消息（v29：移除搜索群聊步骤，直接粘贴发送）
    print("\n[2/3] 正在粘贴消息...")
    time.sleep(1)

    set_clipboard_text(message)
    win32api.keybd_event(0xA2, 0, 0, 0)  # Ctrl down
    win32api.keybd_event(0x56, 0, 0, 0)  # V down
    win32api.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)  # V up
    win32api.keybd_event(0xA2, 0, win32con.KEYEVENTF_KEYUP, 0)  # Ctrl up

    time.sleep(2)
    print("✓ 消息已粘贴")

    # 3. 按回车发送
    print("\n[3/3] 正在发送消息...")
    time.sleep(1)

    win32api.keybd_event(0x0D, 0, 0, 0)  # Enter down
    win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)  # Enter up

    time.sleep(2)

    print("\n" + "="*60)
    print("  ✓ 全部操作完成！")
    print("  - 使用当前已打开的聊天窗口发送（v29）")
    print("  - 已发送消息")
    print("="*60)
    print("\n  ⚠️ 提示：推荐使用 wechat_send.py 统一脚本：")
    print('  python wechat_send.py --message-file "消息文件路径"')
    print('  python wechat_send.py --file "文件路径"')

if __name__ == '__main__':
    main()