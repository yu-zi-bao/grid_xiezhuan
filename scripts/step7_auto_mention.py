# -*- coding: utf-8 -*-
"""
第7步自动化发送微信消息（v29 更新 ⭐⭐⭐⭐⭐）

v29 变更：
  - 移除硬编码消息和@人员逻辑
  - 直接使用桌面微信当前已打开的聊天窗口进行发送
  - 禁止搜索聊天、禁止导航通讯录、禁止切换聊天对象

已废弃：本脚本已由 wechat_send.py 统一脚本替代。
"""

import time

def main():
    print("="*60)
    print("  第7步：微信发送消息（v29：直接使用当前聊天窗口）")
    print("="*60)
    print()
    print("  v29 更新：本脚本已废弃，请使用 wechat_send.py 统一脚本：")
    print()
    print("  # 发送文件：")
    print('  python wechat_send.py --file "C:\\Users\\Administrator\\Desktop\\携转结果.xlsx"')
    print()
    print("  # 发送文本消息：")
    print('  python wechat_send.py --message-file "D:\\携转查询\\grid_message.txt"')
    print()
    print("  # 同时发送文件和消息：")
    print('  python wechat_send.py --file "携转结果.xlsx" --message-file "grid_message.txt"')
    print()
    print("  v29 核心原则：")
    print("  1. 直接使用当前已打开的聊天窗口")
    print("  2. 不搜索聊天、不导航通讯录、不切换聊天对象")
    print("  3. 复制文件/文本到剪贴板 → Ctrl+V → 回车发送")
    print("="*60)

if __name__ == '__main__':
    main()