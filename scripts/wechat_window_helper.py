# -*- coding: utf-8 -*-
"""
微信窗口查找辅助模块（v28 新增 ⭐⭐⭐⭐⭐）

改进原因：
  新版微信（4.0+）将进程名从 WeChat.exe 改为 Weixin.exe，
  窗口类名也发生了变化，导致传统的 FindWindow 方式全部失效。
  
改进方案：
  统一使用 Process.GetProcessesByName("Weixin") + EnumWindows 方式查找微信窗口。
  不再依赖 FindWindow("微信") 或 FindWindow("WeChatMainWndForPC", null)。

用法：
  from wechat_window_helper import find_wechat_window, activate_window
  windows = find_wechat_window()
  if windows:
      hwnd, title = windows[0]
      activate_window(hwnd)
"""

import win32gui
import win32con
import win32process
import win32api
import subprocess
import time


def _get_wechat_pids():
    """获取所有微信进程的 PID（兼容 WeChat 4.0+ 的 Weixin.exe 和旧版 WeChat.exe）"""
    wechat_pids = set()
    try:
        result = subprocess.run(
            ['tasklist', '/fo', 'csv', '/nh'],
            capture_output=True, text=True, encoding='gbk'
        )
        for line in result.stdout.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            # 解析 CSV 格式: "Weixin.exe","1234","Console","1","12345 K"
            parts = line.strip('"').split('","')
            if len(parts) >= 2:
                proc_name = parts[0].lower()
                if proc_name in ('weixin.exe', 'wechat.exe'):
                    try:
                        wechat_pids.add(int(parts[1]))
                    except ValueError:
                        pass
    except Exception:
        pass
    return wechat_pids


def find_wechat_window():
    """
    查找微信主窗口（v28 改进版）
    
    查找策略：
    1. 通过 tasklist 获取所有 Weixin.exe / WeChat.exe 进程的 PID
    2. EnumWindows 遍历所有可见窗口
    3. 优先匹配 PID 属于微信进程且标题含"微信"的窗口
    4. 若 PID 匹配失败，回退到仅按标题匹配（兼容性兜底）
    
    Returns:
        list of (hwnd, title) tuples
    """
    wechat_pids = _get_wechat_pids()
    
    pid_matched = []
    title_matched = []
    
    def enum_windows_callback(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return
        if "微信" in title or "WeChat" in title:
            title_matched.append((hwnd, title))
            # v28 核心：通过 PID 匹配 Weixin.exe 进程
            if wechat_pids:
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    if pid in wechat_pids:
                        pid_matched.append((hwnd, title))
                except Exception:
                    pass
    
    win32gui.EnumWindows(enum_windows_callback, None)
    
    # 优先返回 PID 匹配的窗口，其次返回标题匹配的窗口
    if pid_matched:
        return pid_matched
    return title_matched


def activate_window(hwnd):
    """
    激活指定窗口（v28 改进版）
    
    使用 AttachThreadInput + SetForegroundWindow 组合方式，
    解决 Windows 10 前台窗口锁定机制导致 SetForegroundWindow 失败的问题。
    """
    try:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        
        # v28 改进：使用 AttachThreadInput 强制激活
        foreground_hwnd = win32gui.GetForegroundWindow()
        if foreground_hwnd != hwnd:
            foreground_tid, _ = win32process.GetWindowThreadProcessId(foreground_hwnd)
            target_tid, _ = win32process.GetWindowThreadProcessId(hwnd)
            current_tid = win32api.GetCurrentThreadId()
            
            try:
                win32process.AttachThreadInput(current_tid, target_tid, True)
                win32gui.SetForegroundWindow(hwnd)
                win32gui.BringWindowToTop(hwnd)
                win32process.AttachThreadInput(current_tid, target_tid, False)
            except Exception:
                win32gui.SetForegroundWindow(hwnd)
        
        time.sleep(1)
        return True
    except Exception as e:
        print(f"激活窗口失败: {e}")
        return False


if __name__ == '__main__':
    windows = find_wechat_window()
    print(f"找到 {len(windows)} 个微信窗口")
    for hwnd, title in windows:
        print(f"  窗口句柄: {hwnd}, 标题: {title}")