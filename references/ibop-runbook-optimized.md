# IBOP-OA 携号转网查询 全流程操作手册（v9 · 2026-11-05 第九次修订）

> 本文档沉淀 2026-10-27 至 2026-11-05 九轮全流程实操的全部优化经验。
> 下次执行时直接按"标准操作路径"走，再对照"避坑清单"逐条检查。
> 配套：`references/ibop-oa-control.md`（IBOP_OA 控件定位细节）。
>
> **v8 修订要点（第八次执行新增）**:
> - **微信发送核心优化**：**直接使用桌面微信当前已打开的窗口进行发送**，禁止搜索聊天、禁止导航通讯录、禁止切换聊天对象
> - **发送方式统一用回车键**：文件和消息粘贴后都按回车键（Return）发送，不点击发送按钮
> - **避坑记录**：搜索微信聊天会误入通讯录页面，导致丢失当前聊天窗口；切换聊天对象会发送到错误窗口
> - **文本编辑器**：使用 `deepin-editor` 打开临时文件
>
> **v10 修订要点（2026-11-02 新增）**:
> - **Windows"保存下载文件"弹窗处理**：导出下载流程中可能弹出系统级文件保存对话框（文件名 CocExportMnpindex_*.xls），**一律点击"取消"**（非"保存"），文件已通过 fetch+HTTP 中转服务保存，此弹窗为冗余
> - **携转结果排序**：生成《携转结果.txt》时，所有记录按第2列"最近一次申请时间"**倒序排列（从新到旧）**，最新申请记录排在最前面
>
> **v12 修订要点（2026-11-02 新增）**:
>
> **v15 修订要点（2026-11-03 新增 ⭐⭐⭐⭐⭐）**:
> - **携转结果.txt 保存路径固化**：始终保存到桌面 `C:\Users\Administrator\Desktop\携转结果.txt`，不存放到其他目录
> - **截止小时取法变更**：去重网格消息中的"XX 时"**取程序执行开始时间的小时数**（而非最新申请时间）。例如：程序 16:20 开始执行，消息标题为"截至 16 时"
>
> **v20 修订要点（2026-11-03 新增 ⭐⭐⭐⭐⭐）**:
> - **去重网格消息格式升级**：从简单一句话格式升级为**详细的分网格列表格式**——标题行 + 汇总行 + 每个网格的号码数量和号码列表 + 合计行
> - **消息内容包含具体号码**：每个网格下列出全部手机号码，号码间用顿号（、）连接
> - **消息结构**：第1行标题 → 第2行汇总 → 空行 → 网格明细行（每网格一行）→ 空行 → 末行合计
>
> **v16 修订要点（2026-11-03 新增 ⭐⭐⭐⭐⭐）**:
> - **自动关闭残留弹窗**：任务启动时，先检查页面是否存在"携号转网申请导出"弹窗（显示"处理完成"状态，带文件名如 `1.CocExportMnpindex_20261103085002`），若存在则**默认点击关闭按钮（X）**，避免上次任务残留弹窗干扰新任务执行
> - **弹窗处理顺序调整**：新增任务启动时专项检查，作为弹窗处理执行顺序的第一步
>
> **v17 修订要点（2026-11-03 新增 ⭐⭐⭐⭐⭐）**:
> - **任务结束刷新页面**：第八步全部完成后，**自动刷新 IBOP-OA 当前页面**（`browser_navigate` 的 `action=reload`），清除查询状态、弹窗和临时数据，为下次执行准备干净环境
> - **刷新时机**：作为第九步执行，确保微信文件发送、消息发送全部完成后再刷新
> - **刷新目的**：避免下次任务启动时页面残留查询结果或弹窗状态
> **v18 修订要点（2026-11-03 新增 ⭐⭐⭐⭐⭐）**:
> - **取消截图发送功能**：第八步**只发送文件《携转结果.txt》和去重网格文字消息**，取消 Excel 截图发送功能
> - **移除 Excel 相关操作**：不再打开 Excel、不再截图、不再关闭 Excel
> - **简化微信发送**：从三个子步骤（8.1 文件 + 8.2 消息 + 8.3 截图）简化为两个子步骤（8.1 文件 + 8.2 消息）
>
> **v19 修订要点（2026-11-03 新增 ⭐⭐⭐⭐⭐）**:
> - **第七步新增 Excel 生成**：从《携转结果.txt》解析数据，使用 `scripts/generate_xlsx.py`（openpyxl）生成《携转结果.xlsx》，含"携转明细"和"网格统计"两个 Sheet，保存到桌面 `C:\Users\Administrator\Desktop\携转结果.xlsx`
> - **第八步微信发送改为 xlsx**：8.1 从发送《携转结果.txt》改为发送《携转结果.xlsx》，接收方可直接用 Excel 打开
> - **新增第十步：刷新后关闭弹窗**：第九步刷新页面后，自动检测并关闭所有弹窗（如"提示(sj-x86-int-web09)"对话框），点击"确认"按钮，循环检测直至无弹窗
>
>
> **v7 修订要点（第七次执行新增）**:
> - **第5步网格匹配全流程固化**：数据源明确为"从查询导出数据中提取手机号码"，固定4字段（手机号码/最近一次申请时间/申请内容/GRID_NAME），Tab分隔，保存到 `/data/home/cmcc/Desktop/携转结果.txt` **自动覆盖**
> - **第6步微信发送文件固化**：桌面文件管理器 Ctrl+C 复制 → 微信置顶第1个聊天窗口 Ctrl+V 粘贴 → 发送
> - **第6步去重网格消息固化**：截止小时取**程序执行开始时间的小时数**（v15 变更），格式升级为详细分网格列表（v20）：标题行+汇总行+每网格号码列表+合计行
> - **中文消息发送禁止 xdotool type**：必须文本编辑器中转（写文件→Ctrl+A→Ctrl+C→微信Ctrl+V）
>
> **v6 修订要点**:
> - **功能 iframe 索引从 `iframes[4]` 变为 `iframes[3]`**（iframe 数量变化导致索引偏移，下次执行需动态探测）
> - **携号转网申请查询链接 ID 修正为 `a#760010671252`**（非 `76001671252`）
> - **四宫格悬停实测不展开**：hover 后二级菜单链接 `visible:false`，但**直接 `dispatchEvent(click)` 可触发 `menuClick()` 加载页面**
> - **文件下载最终方案**：`systemd-run --user --no-block` 启动一次性 HTTP 接收服务 → 浏览器 `fetch` 下载 blob → POST 到 `127.0.0.1:18899` → 服务自动退出
> - **curl 方案已弃用**：IBOP 有 NLAPM JavaScript 保护，curl 下载返回 HTML 而非 XLS
> - **已登录跳过登录**：如 IBOP-OA 已登录（标题"中国移动客户关系管理系统"），直接从第 2 步开始
>
> **v3 修订要点**:
> - 时间赋值必须走 LigerUI API + jQuery val 双重设置，且在 `world:"main"` 中执行
> - 所有弹窗一律点击"确认"

---

## 0. 链路概览（一句话）

4A 门户（SIM KEY 登录）→ 点击 IBOP_OA 文本节点进入 IBOP-OA →
四宫格悬停 → 服务变更 → 携号转网申请查询 →
配置 龙岩/所有区县/当日 00:00:00-23:59:59 → 查询 →
导出走"异步工单弹窗"，循环【刷新】等"处理完成" →
浏览器 fetch 下载 → POST 到本地 HTTP 接收服务 → 保存 .xls 文件 →
**与客户网格归属CSV关联匹配 GRID_NAME → 生成《携转结果.txt》→ 微信发送文件+去重网格消息**

涉及的标签页关系：
- Tab A（4A 门户）：`https://4a.fjit.cmcc:30002/iam/v1/#/home/homeManage`
- Tab B（IBOP-OA 主框架）：`http://10.53.182.13:9900/ibop/sys/main_frame.jsp` ← 主要操作窗口
  - 功能内容区是 Tab B 内嵌的同源 iframe（下文统称"功能 iframe"，**索引不固定，需动态探测**，v6 实测为 `iframes[3]`）

---

## 1. 登录 4A 并进入 IBOP-OA

### 1.1 4A 登录

1. 打开 4A 门户 `https://4a.fjit.cmcc:30002/iam/v1/`，过 SSL 告警（高级 → 继续前往）。
2. 切"SIM KEY"标签 → 填手机号（**13950880770**）→ 点登录 → 等 SIM 认证（10-15s，需用户手机端确认）。
3. 登录成功后进入门户首页，标题"福建移动统一4A门户"，显示用户名（王村荣）。

> **弹窗规则**：执行过程中任何弹窗一律点击"确认"。
> ⚠️ **唯一例外（v10 新增）**：Windows 系统级"保存下载文件"对话框——**一律点击"取消"**。文件已通过 fetch+HTTP 中转服务保存，此弹窗为冗余。

### 1.2 进入 IBOP-OA

4. **IBOP_OA 文本节点在首页内嵌 iframe 中**（`appResource/v1/#/appResource/appResLogin`）：
   - 需穿透 iframe 搜索：遍历 `document.querySelectorAll('iframe')` → 在 `contentDocument` 中找 `div.appName_1` 且 textContent === 'IBOP_OA'
   - 直接 `.click()` 该文本节点即可触发单点登录
   - **不需要先点击「应用资源登录」Tab**，首页 iframe 已加载应用列表
5. 若出现"重复登录/会话"弹窗：在弹窗 iframe 内找「确认」链接并 `.click()` 即可（**一律点确认**）。
6. 结果：浏览器新开 Tab B，标题"中国移动客户关系管理系统"。

---

## 2. 主界面导航 — 菜单链接直点击方式（推荐 ⭐，v6 修正）

### 2.1 菜单链接直接点击（推荐，最稳定）

> **v6 重大修正**：四宫格悬停实测**不展开二级菜单**（链接 `visible:false`），
> 但链接 DOM 节点存在且有 `onclick` 夆用，**直接 `dispatchEvent(click)` 即可触发 `menuClick()` 加载页面**。
> 无需先 hover 展开，省去鼠标事件模拟的复杂性。

**关键机制**：`ul#menu_layout` 的一级菜单项内嵌二级链接，虽然 CSS `display:none` 隐藏，
但 `onclick` 复用 `menuClick(funcName, encodedUrl)` 仍可执行。

1. 定位菜单容器：`document.querySelector('#menu_layout')`（class=`newlayoutList`，14 个 `<li>`）。
2. **第 4 项 = "服务变更"**（`li:nth-child(4)`），内含三个携号转网链接：
   - `a#760010671250` = 携号转网号码查询
   - `a#760010671252` = 携号转网申请查询  ← **目标**
   - `a#760010671290` = 网上携号转网订单处理
3. 直接对 `a#760010671252` 派发 click 事件：
   ```js
   var link = document.getElementById('760010671252');
   link.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true, view:window}));
   ```
4. `menuClick()` 会在当前 tab 创建新 iframe（`page_index.jsp?url=...mnp_index_to_event...`）加载功能页面。
5. **动态探测功能 iframe**：遍历 `document.querySelectorAll('iframe')`，找到 `src` 含 `mnp_index_to_event` 或 `page_index.jsp` 且 `offsetParent !== null` 的 iframe。
6. 在该 iframe 的 `contentDocument` 中检查查询表单元素：`#history_TimeChooseStart`、`#history_TimeChooseEnd`、`#history_open_home_city`、`#history_queryBtn`、`#history_exportBtn`。

**菜单元素特征**：
| 层级 | 元素 | 特征 |
|------|------|------|
| 一级菜单 | `ul#menu_layout > li:nth-child(4)` | 文本"服务变更" |
| 二级链接 | `a#760010671252` | 文本"携号转网申请查询"，`onclick=menuClick(...)` |

> ⚠️ **禁用搜索框**（`#search_val` + `#search`），实测搜索按钮被 SPAN 遮挡，无法可靠点击。
> ⚠️ **功能 iframe 索引不固定**，不要硬编码 `iframes[3]` 或 `iframes[4]`，必须动态探测。

### 2.2 搜索框方式（已弃用 ❌）

> **v5 弃用**：搜索按钮 `#search` 实测被 SPAN 元素遮挡（`INPUT_TARGET_OBSCURED`），
> 且 native setter + change 事件方式也无法可靠提交搜索。
> **不再使用此方式导航**，一律走四宫格悬停。

---

## 3. 查询参数配置（功能 iframe 内）

### 3.1 控件 ID 与期望值

| 条件 | 控件 ID | 期望值 | 备注 |
|------|---------|--------|------|
| 归属地市 | `history_open_home_city` | 597 (龙岩) | 通常已默认选中 |
| 归属区县 | `history_open_home_county` | "" (所有) | value="" 即所有区县 |
| 申请类型 | `history_index_id` | -1 (所有) | |
| 申请状态 | `history_online_bi_status` | -1 (所有) | |
| 起始时间 | `history_TimeChooseStart` | 当日 00:00:00 | 必须修改，初值为历史日期 |
| 结束时间 | `history_TimeChooseEnd` | 当日 23:59:59 | 必须修改，初值为当前时刻 |
| 每页条数 | `select[name="rp"]` | 30 | 可选 10/15/20/30 |

### 3.2 时间赋值（v3 关键优化 ⭐⭐）

> **必须**在 `world:"main"` 中执行，isolated world 无法访问 jQuery/liger。
> **必须**同时设置 LigerUI 控件值和 jQuery val，后端查询函数实际读取 jQuery val。

```js
// 在 main world 中执行，需动态探测功能 iframe
var iframe = document.querySelectorAll('iframe')[3]; // v6: 索引可能变化，需动态探测
var iwin = iframe.contentWindow;
var idoc = iframe.contentDocument;

var today = new Date();
var dateStr = today.getFullYear() + '-' + 
  String(today.getMonth()+1).padStart(2,'0') + '-' + 
  String(today.getDate()).padStart(2,'0');

// 方法1：通过 LigerUI API
iwin.liger.get('history_TimeChooseStart').set('value', dateStr + ' 00:00:00');
iwin.liger.get('history_TimeChooseEnd').set('value', dateStr + ' 23:59:59');

// 方法2：通过 jQuery val（查询函数实际读取此值）
iwin.$('#history_TimeChooseStart').val(dateStr + ' 00:00:00');
iwin.$('#history_TimeChooseEnd').val(dateStr + ' 23:59:59');

// 设置区县为"所有"
idoc.getElementById('history_open_home_county').value = '';
```

> **YYYY-MM-DD 每天动态取当天**（get_current_time 或系统时钟），绝不复用昨天日期。

### 3.3 执行查询

- 查询按钮：`<a id="history_queryBtn" class="btn">`（注意是 `<a>` 不是 `<button>`）
- 点击后等待 3-4s，检查分页信息中的「共N条」确认结果

### 3.4 查询按钮触发机制（v3 发现）

- 查询按钮的 click 事件绑定：`sellers_table_list.clearAll(); sellers_table_list.loadData();`
- `loadData()` 触发 grid 的 `onGetDataDIY` 回调 → 调用 `qryCocElecChnl(param)`
- **直接调用 `qryCocElecChnl({page:1})` 不会加载数据到 grid**，因为缺少 grid 提供的 callback
- 正确做法：`sellers_table_list.clearAll(); sellers_table_list.loadData();`

---

## 4. 导出：异步工单机制 + 文件下载

### 4.1 导出机制

- 导出按钮：`<a id="history_exportBtn" class="btn">`（同样是 `<a>` 标签）
- 点击后弹出 **LigerDialog**（标题"携号转网申请导出"），内嵌 iframe `cocibopexcept.jsp`
- 后端队列处理：等待处理 → 正在处理 → 处理完成
- 弹窗内唯一按钮：`<a id="nextBtn">` 文本"刷新"

### 4.2 轮询刷新（v5 加速 ⭐）

```js
// 每 1.5~2 秒点击刷新按钮，直至出现下载链接（v5：不再死等 5s/30s）
// 穿透路径：功能 iframe → .l-dialog → inner iframe(#except_blind_area_prepare) → contentDocument
// 退出条件：iframe 内出现 <a href*="CocRemoteFileDownload"> 下载链接
// 状态判断：step_3 绿色(cfig_step_green_3) = 处理完成
```

- **v5 优化**：轮询间隔从 5s 缩短为 **1.5~2s**，实测后端处理十几秒内完成
- **v6 实测**：导出仅 2 次轮询（约 3 秒）即完成
- 下载链接格式：`/ibop/CocRemoteFileDownload.do?fileid=CocExportMnpindex_<yyyyMMddHHmmss>&upload_type=cocdefault&format=xls`

### 4.3 文件下载方案（v22 最终方案 ⭐⭐⭐⭐⭐）

> **问题**：
> - `curl` 即使携带 Cookie 也无法下载（IBOP 有 NLAPM JavaScript 保护，返回 HTML 而非 XLS）
> - 浏览器原生 `<a download>` 点击下载不生效（Electron 环境限制）
> - ~~v6 方案：`systemd-run --user --no-block` 启动 HTTP 中转服务~~（Linux 专用，Windows 不适用）
> - ~~v10 方案：Windows 保存弹窗点取消~~（弹窗仍出现阻塞流程，治标不治本）
> - **v22 方案**：`browser_execute_js` 直接 XHR fetch → ArrayBuffer → base64 返回 → Python 解码保存。**零弹窗、零中转服务、零平台依赖**
>
> **v22 核心优势**：
> - 完全绕过浏览器原生下载机制 → **Windows"保存下载文件"弹窗不再出现**
> - 不需要 HTTP 中转服务 → 不需要 `recv_once.py`、不需要 `127.0.0.1:18899` 端口监听
> - 不需要 `systemd-run`（Linux 专用命令）→ **Windows 原生兼容**
> - 文件直接保存到工作区目录 → 路径可控、便于后续处理

**步骤 1：`browser_execute_js` fetch 下载链接 + base64 返回**

```javascript
// 在 browser_execute_js 中执行（world: main, awaitPromise: true, effect: download）
return new Promise(function(resolve) {
    var downloadUrl = 'http://10.53.182.13:9900/ibop/CocRemoteFileDownload.do?fileid=CocExportMnpindex_xxxx&upload_type=cocdefault&format=xls';
    var xhr = new XMLHttpRequest();
    xhr.open('GET', downloadUrl, true);
    xhr.responseType = 'arraybuffer';
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var bytes = new Uint8Array(xhr.response);
                var binary = '';
                for (var i = 0; i < bytes.length; i += 8192) {
                    binary += String.fromCharCode.apply(null, bytes.subarray(i, Math.min(i + 8192, bytes.length)));
                }
                resolve(JSON.stringify({success: true, fileSize: bytes.length, base64: btoa(binary)}));
            } else {
                resolve(JSON.stringify({error: 'HTTP ' + xhr.status}));
            }
        }
    };
    xhr.onerror = function() { resolve(JSON.stringify({error: 'XHR网络错误'})); };
    xhr.send();
});
```

**步骤 2：Python 解码 base64 并保存到工作区**

```python
import base64, json

# js_result 为 browser_execute_js 返回的 JSON 字符串
data = json.loads(js_result)
raw = base64.b64decode(data['base64'])
save_path = r'D:\携转预警\CocExportMnpindex_xxxx.xls'  # 工作区目录
with open(save_path, 'wb') as f:
    f.write(raw)
print(f'Saved {len(raw)} bytes to {save_path}')
```

**步骤 2b：大文件兜底（>200KB，一般不需要）**

```javascript
// 第一次调用：下载并存储到 window.name
window.name = 'FILEDATA:' + base64String;
return JSON.stringify({success: true, fileSize: bytes.length, base64Length: base64String.length});

// 第二次调用：提取前半部分
var b64 = window.name.substring(9);
return b64.substring(0, 23000);

// 第三次调用：提取后半部分
var b64 = window.name.substring(9);
return b64.substring(23000);
```

**步骤 3：验证文件**

```python
import xlrd
wb = xlrd.open_workbook(save_path, ignore_workbook_corruption=True)
sh = wb.sheet_by_index(0)
print(f'Rows: {sh.nrows}, Cols: {sh.ncols}')  # 确认行数和列数
```

> ⚠️ **v22 废弃清单**：
> - `recv_once.py`（HTTP 中转服务脚本）→ **废弃**
> - `systemd-run --user --no-block` → **废弃**（Linux 专用）
> - `127.0.0.1:18899` 端口监听 → **废弃**
> - `/tmp/recv_once.py` → **废弃**（Linux 路径）
> - v10 "保存弹窗点取消"策略 → **降级为兜底**（v22 后弹窗不再出现）

### 4.4 导出数据完整性

- 导出文件包含 **全部记录**，可能略多于页面分页显示数
- **以导出文件行数为准**进行后续分析

### 4.5 导出文件字段

| 列序 | 字段名 | 说明 |
|------|--------|------|
| A | 事件ID | |
| B | 归属地市 | 龙岩 |
| C | 归属区县 | 新罗/永定/上杭/武平/长汀/连城/漳平 |
| D | 手机号码 | |
| E | 申请时间 | 格式 YYYY-MM-DD HH:MM:SS.0 |
| F | 申请类型 | 申请过授权码成功/查询过携转资失败等 |
| G | 申请状态 | |

---

## 5. 从查询数据提取手机号码 → 网格匹配 → 生成《携转结果.txt》（v7 固化 ⭐⭐⭐⭐⭐）

### 5.0 流程概述

> **数据源**：从第四步导出的携转申请查询结果（.xls 文件）中提取手机号码，不再笼统说"读取.xls"。
> **目标**：生成《携转结果.txt》，包含固定4字段，保存到桌面并自动覆盖。
> **v7 固化**：以下所有参数和逻辑为最终标准，下次启动技能时直接执行，无需重新确认。

### 5.1 数据源

| 数据 | 来源 | 编码 | 关键字段 |
|------|------|------|----------|
| 携转申请数据 | IBOP-OA 导出的 .xls | UTF-8 | 手机号码(D列)、申请时间(E列)、申请类型(F列) |
| 客户网格归属 | `/data/home/cmcc/Fuxiaozhi/客户网格归属.csv` | GBK | MSISDN、HOME_COUNTY、GRID_ID、GRID_NAME |

### 5.2 处理逻辑

```python
import xlrd, csv

# 1. 读取携转申请数据，按手机号码去重取最近一次申请
phone_latest = {}  # phone -> {time, type}
for r in range(1, sheet.nrows):
    phone = str(sheet.cell_value(r, 3)).strip()  # D列手机号码
    time_str = str(sheet.cell_value(r, 4)).strip()  # E列申请时间
    type_str = str(sheet.cell_value(r, 5)).strip()  # F列申请类型
    if phone not in phone_latest or time_str > phone_latest[phone]['time']:
        phone_latest[phone] = {'time': time_str, 'type': type_str}

# 2. 读取客户网格归属CSV（GBK编码）
phone_to_grid = {}
with open('/data/home/cmcc/Fuxiaozhi/客户网格归属.csv', 'r', encoding='gbk') as f:
    reader = csv.DictReader(f)
    for row in reader:
        phone_to_grid[row['MSISDN'].strip()] = row['GRID_NAME'].strip()

# 3. 关联匹配
results = []
for phone, info in phone_latest.items():
    grid_name = phone_to_grid.get(phone, '')
    results.append({
        'phone': phone,
        'time': info['time'].replace('.0', '').strip(),
        'type': info['type'],
        'grid': grid_name
    })

# 4. 按申请时间降序排列
results.sort(key=lambda x: x['time'], reverse=True)

# 5. 写入《携转结果.txt》，Tab分隔
with open('携转结果.txt', 'w', encoding='utf-8') as f:
    f.write('手机号码\t最近一次申请时间\t申请内容\tGRID_NAME\n')
    for r in results:
        f.write(f"{r['phone']}\t{r['time']}\t{r['type']}\t{r['grid']}\n")
```

### 5.3 输出文件规格

- 文件名：`携转结果.txt`
- 编码：UTF-8
- 分隔符：Tab（`\t`）
- **排序规则（v10 新增 ⭐）**：按第2列"最近一次申请时间"**倒序排列（从新到旧）**，即最新的申请记录排在最前面
- 字段（4列）：

| 列序 | 字段名 | 说明 |
|------|--------|------|
| 1 | 手机号码 | 去重后的独立号码 |
| 2 | 最近一次申请时间 | 同一号码多次申请取最新，格式 YYYY-MM-DD HH:MM:SS |
| 3 | 申请内容 | 申请类型（申请过授权码成功/查询过携转资失败等） |
| 4 | GRID_NAME | 匹配客户网格归属CSV，未匹配则为空 |

### 5.4 保存到桌面（v7 固化）

```bash
# 保存到桌面，自动覆盖原文件，不询问
cp 携转结果.txt /data/home/cmcc/Desktop/携转结果.txt -f
```

> ⚠️ **固定保存路径**：`/data/home/cmcc/Desktop/携转结果.txt`，**自动覆盖原文件，不询问**。
> v7 固化：此路径为最终标准，后续微信发送步骤从此路径复制文件。

---

## 6. 微信发送文件和去重网格消息（v8 固化 ⭐⭐⭐⭐⭐）

### 6.0 前置条件与目标窗口

- 桌面微信客户端已登录
- **置顶第1个聊天窗口就是目标发送窗口**，无需额外选择聊天对象（v7 固化）
- **v8 核心原则：直接使用桌面微信当前已打开的窗口进行发送**，禁止搜索聊天、禁止导航通讯录、禁止切换聊天对象
- **v28 窗口查找改进**：新版微信 4.0+ 进程名从 `WeChat.exe` 改为 `Weixin.exe`，窗口类名变化导致 `FindWindow` 失效
  - **统一方案**：`tasklist` 获取 `Weixin.exe`/`WeChat.exe` PID → `EnumWindows` + `GetWindowThreadProcessId` 匹配窗口
  - **共享模块**：`scripts/wechat_window_helper.py`，所有脚本调用 `find_wechat_window()` + `activate_window()`
  - **激活改进**：`AttachThreadInput` + `SetForegroundWindow` 组合，解决 Win10 前台锁定
  - 旧版 Linux 方式 `xdotool search --name "微信"` 已弃用
- 文件已保存到桌面 `C:\Users\Administrator\Desktop\携转结果.txt`

> ⚠️ **v8 避坑**：搜索微信聊天会误入通讯录页面，导致丢失当前聊天窗口；切换聊天对象会发送到错误窗口。**直接用当前窗口！**

### 6.1 发送《携转结果.txt》文件（v8 固化）

> **流程**：桌面文件管理器中 **Ctrl+C** 复制《携转结果.txt》→ **直接激活微信当前窗口** → **Ctrl+V** 粘贴文件 → 按回车键发送
> **v8 固化**：直接使用微信当前窗口，不搜索/不导航；发送用回车键。

```bash
export DISPLAY=${DISPLAY:-:0}

# 1. 打开桌面文件管理器
xdotool exec -- dde-file-manager /data/home/cmcc/Desktop &
sleep 2

# 2. 定位文件管理器窗口
FM_WID=$(xdotool search --name "桌面 — 文件管理器")

# 3. 在文件管理器中搜索定位文件
xdotool windowactivate $FM_WID
sleep 0.5
xdotool key ctrl+f        # 打开搜索
sleep 0.5
# 注意：中文输入可能被输入法干扰，建议用鼠标点击定位文件
# 或用 xdotool type --delay 50 "携转结果" 后检查搜索结果

# 4. 选中《携转结果.txt》文件（点击文件图标）
xdotool mousemove --window $FM_WID <x> <y>  # 文件图标坐标
xdotool click 1
sleep 0.5

# 5. Ctrl+C 复制文件
xdotool key ctrl+c
sleep 1

# 6. 切换到微信窗口
WECHAT_WID=$(xdotool search --name "微信" | head -1)
xdotool windowactivate $WECHAT_WID
sleep 1

# 7. 点击微信输入框区域
xdotool mousemove --window $WECHAT_WID 400 570
xdotool click 1
sleep 0.3

# 8. Ctrl+V 粘贴文件
xdotool key ctrl+v
sleep 2

# 9. 按回车键发送（v8 固化：不点击发送按钮）
xdotool key Return
sleep 1
```

### 6.2 发送去重网格文本消息（v8 固化，v20 优化消息格式 ⭐⭐⭐⭐⭐）

> **消息格式（v20 升级）**：详细分网格列表格式，详见 SKILL.md §8.2
> **XX** = **程序执行开始时间的小时数**（v15 变更，24小时制，如 17 时）
> **消息结构**：标题行 → 汇总行 → 空行 → 网格明细行（每网格一行，含号码列表）→ 空行 → 合计行
> **示例**：
> ```
> 【携号转网预警】龙岩今日携转异网事件统计（截至17时）
> 去重后共60个号码，涉及20个网格：
>
> 龙岩上杭古田网格：2个（15280828095、18359343108）
> 龙岩上杭城区网格：1个（13860242710）
> ...
>
> 合计60个号码
> ```
> **v7 固化**：grid_name 分组，号码间用顿号连接。
> **v8 固化**：直接激活微信当前窗口粘贴发送，不搜索/不导航；发送用回车键。

**文本输入避坑（v7 强调）**：`xdotool type` 输入中文**必须**被输入法干扰，**禁止直接使用**。

**唯一推荐方案：文本编辑器中转复制粘贴（v7 固化）**

> ⚠️ **必须文本编辑器中转**：写文件→Ctrl+A→Ctrl+C→微信Ctrl+V（**禁止 xdotool type**）
> ⚠️ **微信置顶第1个聊天窗口即为目标发送窗口**，无需额外选择聊天对象。

```bash
export DISPLAY=${DISPLAY:-:0}

# 1. 将消息写入临时文件
cat > /tmp/grid_message.txt << 'EOF'
【携号转网预警】龙岩今日携转异网事件统计（截至17时）
去重后共60个号码，涉及20个网格：

龙岩上杭古田网格：2个（15280828095、18359343108）
龙岩上杭城区网格：1个（13860242710）
...

合计60个号码
EOF

# 2. 用默认文本编辑器打开
xdotool exec -- xdg-open /tmp/grid_message.txt &
sleep 2

# 3. 在文本编辑器中 Ctrl+A 全选 → Ctrl+C 复制
EDITOR_WID=$(xdotool search --name "grid_message")
xdotool windowactivate $EDITOR_WID
sleep 0.5
xdotool key ctrl+a
sleep 0.2
xdotool key ctrl+c
sleep 0.5

# 4. 切到微信 → 点击输入框 → Ctrl+V 粘贴 → 点击发送
xdotool windowactivate $WECHAT_WID
sleep 0.5
xdotool mousemove --window $WECHAT_WID 400 570
xdotool click 1
sleep 0.3
xdotool key ctrl+v
sleep 0.5

# 5. 点击发送按钮
xdotool mousemove --window $WECHAT_WID 820 610
xdotool click 1
sleep 1

# 6. 关闭文本编辑器，清理临时文件
xdotool windowactivate $EDITOR_WID
xdotool key ctrl+q
rm -f /tmp/grid_message.txt
```

### 6.3 发送《携转结果.txt》Excel 截图（v12 新增 ⭐⭐⭐⭐⭐）

> **需求**：将《携转结果.txt》用 Excel 打开后截图，把图片也发送到微信群里，方便群成员直接查看无需下载文件。
> **执行环境**：Windows 桌面，当前系统为 Windows 10。

**步骤 1：用 Excel 打开《携转结果.txt》**

```cmd
start excel "C:\Users\Administrator\Desktop\携转结果.txt"
```

- 等待 Excel 完全加载（约 3~5 秒）
- ⚠️ 若弹出"文本导入向导"：步骤1选"分隔符号" → 步骤2勾选"Tab键" → 步骤3点"完成"
- 若未弹出向导直接打开为表格则继续

**步骤 2：调整显示（可选）**

- 全选（Ctrl+A）→ 自动调整列宽，确保数据可读
- 确保所有数据在可视区域内

**步骤 3：截图**

**方案一（推荐）：使用 `desktop_screenshot` 工具**

- 确保 Excel 窗口在前台
- 调用 `desktop_screenshot` 截取整个桌面
- 截图自动保存为工作区文件

**方案二：Python + pywin32 窗口截图**

```python
import win32gui, win32ui, win32con
from PIL import Image
import time

def find_excel():
    result = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if 'Excel' in title:
                result.append(hwnd)
    win32gui.EnumWindows(callback, None)
    return result[0] if result else None

hwnd = find_excel()
if hwnd:
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    hdesktop = win32gui.GetDesktopWindow()
    hdc = win32gui.GetWindowDC(hdesktop)
    mfcDC = win32ui.CreateDCFromHandle(hdc)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (left, top), win32con.SRCCOPY)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    img.save(r'D:\携转查询\携转结果截图.png')
    mfcDC.DeleteDC()
    saveDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hdc)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    print("截图已保存到 D:\\携转查询\\携转结果截图.png")
else:
    print("未找到 Excel 窗口")
```

**方案三（备选）：PowerShell 全屏截图**

```powershell
Add-Type -AssemblyName System.Windows.Forms
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
$bitmap.Save('D:\携转查询\携转结果截图.png')
$graphics.Dispose()
$bitmap.Dispose()
```


**步骤 4：关闭 Excel**

```cmd
taskkill /IM excel.exe /F
```

- 若弹出"是否保存"对话框：点击"不保存"

**步骤 5：发送截图到微信群**

```cmd
# 1. 打开文件管理器定位到截图所在目录
start explorer "D:\携转查询"

# 2. 选中 携转结果截图.png → Ctrl+C 复制
# 3. 激活微信当前窗口（不搜索/不导航）
# 4. 点击微信输入框 → Ctrl+V 粘贴图片 → 等待预览加载（1~2秒）→ 按回车键发送
```

> ⚠️ **截图发送遵循与 8.1/8.2 相同的微信窗口原则**：直接使用微信当前已打开的窗口，禁止搜索聊天、禁止导航通讯录、禁止切换聊天对象，粘贴后按回车键发送。
> ⚠️ **数据行数较多时**截图可能无法包含全部数据，截取可见区域即可，群成员可通过下载 txt 文件查看完整数据。
> ⚠️ **Excel 打开 .txt 可能弹出文本导入向导**：选"分隔符号"→勾选"Tab键"→点"完成"。

### 6.4 去重网格消息生成逻辑（v7 固化）

```python
# 从携转结果中提取去重 GRID_NAME 和截止小时
grid_names_set = set()
latest_time = "0000-00-00 00:00:00"

for r in results:
    if r['grid']:
        grid_names_set.add(r['grid'])
    if r['time'] > latest_time:
        latest_time = r['time']

hour = start_time[11:13]  # 提取程序执行开始时间的小时（v15 变更）

# v20: 按网格分组生成详细列表消息
from collections import OrderedDict
grid_groups = OrderedDict()  # 保持首次出现顺序
total_count = 0
for r in results:
    grid = r['grid'] if r['grid'] else '未匹配网格'
    if grid not in grid_groups:
        grid_groups[grid] = []
    grid_groups[grid].append(r['phone'])
    total_count += 1

lines = []
lines.append(f"【携号转网预警】龙岩今日携转异网事件统计（截至{hour}时）")
lines.append(f"去重后共{total_count}个号码，涉及{len(grid_groups)}个网格：")
lines.append("")
for grid_name, phones in grid_groups.items():
    phone_str = "、".join(phones)
    lines.append(f"{grid_name}：{len(phones)}个（{phone_str}）")
lines.append("")
lines.append(f"合计{total_count}个号码")
message = "\n".join(lines)
```

### 6.5 微信窗口定位参数（实测）

| 参数 | 值 | 说明 |
|------|----|------|
| 窗口标题 | 微信 | `xdotool search --name "微信"` |
| 窗口ID | 104857617 | 实测值，可能变化 |
| 窗口位置 | 644,192 | 屏幕坐标 |
| 窗口大小 | 880x640 | |
| 输入框中心 | (400, 570) | 相对窗口坐标 |
| 发送按钮 | (820, 610) | 相对窗口坐标，绿色按钮 |

> ⚠️ 窗口位置和大小可能因用户操作而变化，坐标仅供参考。建议每次执行前用 `xdotool getwindowgeometry` 确认。

---

## 7. 技术执行避坑清单

1. **IBOP_OA 在首页 iframe 内**：不需要先点击「应用资源登录」Tab，首页已加载应用列表 iframe，直接穿透搜索即可。
2. **四宫格悬停为唯一导航方式（v5 修正）**：搜索框 `#search` 按钮实测被 SPAN 遮挡无法点击，**已禁用**。一律走四宫格 `DIV.dropmenu` 悬停 → 服务变更 → 携号转网申请查询。
3. **查询/导出按钮是 `<a>` 不是 `<button>`**：用 `getElementById('history_queryBtn')` / `getElementById('history_exportBtn')` 定位。
4. **时间输入必须走 LigerUI API + jQuery val 双重设置**：在 `world:"main"` 中执行，isolated world 无法访问 jQuery/liger。
5. **curl 无法下载导出文件**：IBOP 使用 HttpOnly Cookie，curl 只能拿到 HTML 登录页。必须用浏览器 fetch。
6. **base64 分块传输不可靠**：大文件 base64 通过 `browser_execute_js` 返回值会被截断。改用本地 HTTP 中转服务。
7. **导出弹窗在功能 iframe 内**：需穿透 `iframe[4] → .l-dialog → inner iframe(#except_blind_area_prepare) → contentDocument` 找刷新按钮。
8. **frameId 参数不稳定**：对动态 frame 用 frameId 执行脚本可能返 null。改用顶层文档穿透同源 iframe。
9. **文本锚点优先**：凡可 find 到文本就用文本/elementRef，永不手工估坐标。
10. **跨窗口 Tab 心态**：4A 门户 Tab 与 IBOP-OA Tab 长期并存；操作前后都要 `browser_list_pages` 复核 active tab。
11. **所有弹窗一律点确认**：SSL 警告、重复登录提示、系统提示框等，一律点击"确认"或"确定"。
12. **客户网格归属CSV为GBK编码**：读取时必须指定 `encoding='gbk'`。
13. **xdotool type 中文输入法干扰（v4 强调）**：中文输入**必须**被系统输入法拦截导致乱码，**禁止 xdotool type**。**唯一方案**：文本编辑器中转（写文件 → 打开 → Ctrl+A → Ctrl+C → 微信 Ctrl+V）。
14. **xdotool 坐标需动态确认**：微信/文件管理器窗口位置可能变化，执行前用 `xdotool getwindowgeometry` 确认。
15. **携转数据按号码去重取最新**：同一号码多次申请只保留最近一次，按申请时间字符串比较取最大值。
16. **Windows"保存下载文件"弹窗点取消（v10 新增）**：导出下载流程中可能弹出系统级文件保存对话框，**一律点击"取消"**（非"保存"），文件已通过 fetch+HTTP 中转服务保存，此弹窗为冗余。
17. **携转结果按申请时间倒序排列（v10 新增）**：生成《携转结果.txt》时，所有记录按第2列"最近一次申请时间"从新到旧降序排列。
18. **Excel 打开 .txt 可能弹出文本导入向导（v12 新增）**：选"分隔符号"→勾选"Tab键"→点"完成"。未弹出则直接继续。
19. **截图推荐 PNG 格式（v12 新增）**：PNG 无损格式保证文字清晰，JPEG 压缩可能导致表格文字模糊。
20. **Excel 截图后及时关闭 Excel（v12 新增）**：用 `taskkill /IM excel.exe /F` 关闭，弹出保存框点"不保存"，避免 Excel 进程残留。

---

## 8. 优化点对照表

| # | 优化点 | v1 做法 | v2 做法 | v3 做法 | v4 做法 | 收益 |
|---|--------|---------|---------|---------|---------|------|
| 1 | IBOP_OA 进入 | 找登录按钮/坐标 | 点击 IBOP_OA 文本节点 | 同 v2 | 同 v2 | 消除按钮缺失困惑 |
| 2 | 导航入口 | 四宫格图标 hover | 搜索框输入「携号转网」 | 同 v2，确认 `#search_val` + `#search` | **四宫格悬停为唯一方式，禁用搜索框（按钮被遮挡）** | 更快更稳 |
| 3 | 时间设置 | 手动/硬编码 | native setter + change 事件 | **LigerUI API + jQuery val 双重设置** | 同 v3 | 后端正确读取 |
| 4 | 导出认识 | 认为是直接下载 | 异步工单弹窗轮询 | 同 v2，补充 `#except_blind_area_prepare` | 同 v3 | 不再干等 |
| 5 | 文件下载 | curl/手动 | 浏览器 fetch + HTTP 中转 | 同 v2，补充 no-cors base64 方案 | 同 v3 | 彻底解决 Cookie |
| 6 | 数据完整性 | 信任页面分页数 | 以导出行数为准 | 同 v2 | 同 v3 | 数据不遗漏 |
| 7 | 网格匹配 | 无 | 无 | **客户网格归属CSV关联 GRID_NAME** | **明确4字段固定：手机号码/最近一次申请时间/申请内容/GRID_NAME** | 新增维度 |
| 8 | 携转结果保存 | 无 | 无 | 保存桌面覆盖 | **强调自动覆盖不询问** | 全自动 |
| 9 | 微信文件发送 | 手动 | 手动 | xdotool Ctrl+C/V 自动化 | **明确置顶第1个聊天窗口即目标** | 全自动 |
| 10 | 微信消息发送 | 手动 | 手动 | 文本编辑器中转 + xdotool | **禁止 xdotool type，必须文本编辑器中转** | 避免输入法干扰 |
| 11 | 去重网格消息 | 无 | 无 | 按最新申请时间取截止小时 | **明确取最新一次申请时间的小时数，格式固定** | 标准化 |
| 12 | 弹窗处理 | 逐个询问 | 逐个询问 | 一律点确认 | 同 v3 | 减少中断 |
| 13 | **Excel 截图发送（v12 新增）** | 无 | 无 | 无 | **用 Excel 打开 txt → 截图 → 微信发送图片** | 群成员可直接查看无需下载 |
| 14 | **Excel 文件生成（v19 新增 ⭐）** | 无 | 无 | 无 | **从 txt 解析数据生成 xlsx，含携转明细+网格统计两个 Sheet** | 方便查阅和筛选，替代 txt 发送 |
| 15 | **微信发送 xlsx（v19 修改 ⭐）** | 发送 txt | 发送 txt | 发送 txt | **改为发送 xlsx 文件** | 接收方可直接用 Excel 打开，体验更好 |
| 16 | **刷新后关闭弹窗（v19 新增 ⭐）** | 无 | 无 | 无 | **第十步：刷新后检测并关闭所有弹窗，点击"确认"按钮** | 确保下次任务页面干净无弹窗 |

---

## 9. 标准执行流程（快速版）

```
=== 阶段一：4A登录 + IBOP-OA查询导出 ===
1. 4A 门户 SIM KEY 登录（输入手机号 → 用户手机端确认）
   ※ 如 IBOP-OA 已登录（标题"中国移动客户关系管理系统"），直接跳到第 3 步
2. 首页 iframe 内 find div.appName_1 textContent='IBOP_OA' → click()
   ※ 弹窗一律点确认 → 新 Tab 打开 IBOP-OA
3. 菜单链接直点击：a#760010671252"携号转网申请查询" → dispatchEvent(click)
   ※ 触发 menuClick()，自动加载功能页面到新 iframe
4. 动态探测功能 iframe（src 含 mnp_index_to_event 且 visible）
5. 功能 iframe 内设置参数（world:"main"）：
   - liger.get('history_TimeChooseStart').set('value', 'YYYY-MM-DD 00:00:00')
   - liger.get('history_TimeChooseEnd').set('value', 'YYYY-MM-DD 23:59:59')
   - jQuery val 同步设置
   - 区县 = ""（所有）
6. 点击 a#history_queryBtn → 等待 3-4s → 确认「共N条」
7. 点击 a#history_exportBtn → 弹出异步工单对话框
8. 每 1.5~2s 点击 a#nextBtn（刷新）→ 直至出现 CocRemoteFileDownload 下载链接
9. systemd-run --user --no-block 启动一次性 HTTP 接收服务（/tmp/recv_once.py）
10. 浏览器 fetch 下载链接 → POST blob 到 127.0.0.1:18899（服务自动退出）
11. 验证文件（file 命令 + xlrd 读取）

=== 阶段二：网格匹配，生成《携转结果.txt》和《携转结果.xlsx》（v7 固化, v19 新增 xlsx ⭐） ===
12. 从查询导出数据中提取手机号码，按号码去重取最近一次申请
13. 读取 /data/home/cmcc/Fuxiaozhi/客户网格归属.csv（GBK编码）按号码关联 GRID_NAME
14. 生成《携转结果.txt》，固定4字段（Tab分隔）：
    手机号码 / 最近一次申请时间 / 申请内容 / GRID_NAME
    ※ 按第2列"最近一次申请时间"倒序排列（从新到旧）
15. 保存到桌面 /data/home/cmcc/Desktop/携转结果.txt（自动覆盖原文件，不询问）
16. 生成《携转结果.xlsx》保存到桌面（v19 新增 ⭐）：
    运行 scripts/generate_xlsx.py，从 txt 解析数据生成 Excel
    Sheet1「携转明细」：序号/手机号码/最近一次申请时间/申请内容/GRID_NAME
    Sheet2「网格统计」：序号/网格名称/号码数量/手机号列表（按数量降序，末行合计）
    保存到 C:\Users\Administrator\Desktop\携转结果.xlsx（自动覆盖原文件）

=== 阶段三：微信发送文件和去重网格消息（v8 固化, v19 修改发送 xlsx ⭐） ===
17. 桌面文件管理器中 Ctrl+C 复制《携转结果.xlsx》（v19：改为 xlsx）
18. **直接激活微信当前窗口**（不搜索/不导航）→ 点击输入框 → Ctrl+V 粘贴文件 → 按回车键发送
19. 生成去重网格消息（v20 升级格式 ⭐）：
    - 取程序执行开始时间的小时数为 XX（v15 变更，24小时制）
    - 按 GRID_NAME 分组，每个网格列出号码数量和全部手机号码（顿号连接）
    - 格式：标题行 + 汇总行 + 空行 + 网格明细行 + 空行 + 合计行
    - 详见 SKILL.md §8.2 完整示例
20. 文本编辑器中转：写消息到 /tmp/grid_message.txt → deepin-editor 打开 → Ctrl+A → Ctrl+C
    ※ 禁止 xdotool type 输入中文
21. **直接激活微信当前窗口**（不搜索/不导航）→ 点击输入框 → Ctrl+V 粘贴文本 → 按回车键发送
22. 关闭文本编辑器，清理临时文件

=== 阶段四：刷新页面并关闭弹窗（v17 + v19 新增 ⭐） ===
23. 激活 IBOP-OA 标签页，调用 browser_navigate action=reload 刷新页面
24. 等待 3~5 秒，扫描页面弹窗（v19 新增 ⭐）
25. 检测到弹窗则点击"确认"按钮关闭，循环检测直至无弹窗（最多 5 次）
26. 确认页面回到 IBOP-OA 主界面，任务完成
```

---

## 10. 环境依赖

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| xdotool | 模拟键盘/鼠标操作（微信发送） | 系统自带或 `apt install xdotool` |
| python3-xlrd | 读取 .xls 文件 | `pip install xlrd` |
| python3-csv | 读取 CSV 文件 | 标准库 |
| Pillow | 图片裁剪（截图分析） | `pip install Pillow` |
| ImageMagick (import) | 窗口截图 | 系统自带或 `apt install imagemagick` |
| dde-file-manager | 文件管理器（Deepin/UOS） | 系统自带 |
| 微信桌面版 | 发送文件和消息 | 已安装 |
| Microsoft Excel | 打开 txt 文件并截图（v12 新增） | 通常已安装 |
| pywin32 | Windows 窗口截图（v12 新增） | `pip install pywin32` |
| PowerShell | 备选全屏截图方案（v12 新增） | Windows 系统自带 |

---

## 11. 关键固定配置汇总

| 配置项 | 值 | 备注 |
|--------|----|----|
| 4A 门户 URL | `https://4a.fjit.cmcc:30002/iam/v1/` | SSL 自签证书，首次需手动信任 |
| IBOP-OA URL | `http://10.53.182.13:9900/ibop/sys/main_frame.jsp` | 4A SSO 跳转，不直接访问 |
| IBOP_OA 入口 | 首页 iframe 内 `div.appName_1` 文本节点 click | 非"登录按钮"，直接点文本 |
| 功能 iframe 索引 | `iframes[4]` | 携号转网申请查询页面 |
| 查询按钮 | `a#history_queryBtn` | `<a>` 标签非 `<button>` |
| 导出按钮 | `a#history_exportBtn` | `<a>` 标签 |
| 导出弹窗 iframe | `#except_blind_area_prepare` | 在功能 iframe 内的 .l-dialog 中 |
| 刷新按钮 | `a#nextBtn`（文本"刷新"） | 轮询导出工单状态 |
| 时间控件 | `liger.get('history_TimeChooseStart/End')` | 必须 main world + jQuery val 双重设置 |
| 归属地市 | 龙岩 (value=597) | 固定 |
| 归属区县 | "" (所有) | value 留空即所有区县 |
| 每页条数 | 30 | select[name="rp"]，可选 10/15/20/30 |
| 翻页按钮 | `.l-bar-btnnext` | 下一页 |
| 客户网格归属CSV | `/data/home/cmcc/Fuxiaozhi/客户网格归属.csv` | GBK 编码，约217万条 |
| CSV 关键字段 | MSISDN, GRID_NAME | 按手机号关联 |
| 携转结果文件 | `/data/home/cmcc/Desktop/携转结果.txt` | UTF-8，Tab分隔，自动覆盖 |
| 携转结果字段 | 手机号码/最近一次申请时间/申请内容/GRID_NAME | 固定4字段 |
| 微信窗口标题 | "微信" | `xdotool search --name "微信"` 定位 |
| 微信目标窗口 | 置顶第1个聊天窗口 | 无需额外选择聊天对象 |
| 微信输入框坐标 | (400, 570) | 相对窗口，需动态确认 |
| 微信发送按钮坐标 | (820, 610) | 相对窗口，需动态确认 |
| 消息临时文件 | `/tmp/grid_message.txt` | 文本编辑器中转用 |
| 本地HTTP接收 | `127.0.0.1:18899` | 导出文件中转下载 |
| 查询日期 | 动态取当天 | get_current_time，绝不硬编码 |
| 导航方式 | 菜单链接直接 click（v6 推荐） | v6起直接 click，hover 仅备份方案 |
| 四宫格容器 | `DIV.dropmenu` | v6起 hover 仅备份方案 |
| 一级菜单第4项 | `ul#menu_layout > li:nth-child(4)` | 文本"服务变更" |
| 二级目标链接 | `a#760010671252` | 文本"携号转网申请查询"（v6 修正 ID） |
| 导出轮询间隔 | 1.5~2 秒 | v5 加速，不再死等 5s |
| 4A 门户 URL | `https://4a.fjit.cmcc:30002/iam/v1/` | |
| IBOP-OA URL | `http://10.53.182.13:9900/ibop/sys/main_frame.jsp` | |
| 登录手机号 | **13950880770** | v3 更新 |
| 登录方式 | SIM KEY | |
| 查询地市 | 龙岩（code=597） | |
| 查询区县 | 所有（value=""） | |
| 时间范围 | 当日 00:00:00 ~ 23:59:59 | 动态取当天 |
| 客户网格CSV | `/data/home/cmcc/Fuxiaozhi/客户网格归属.csv` | GBK编码 |
| 携转结果输出 | `/data/home/cmcc/Desktop/携转结果.txt` | v7 固化：自动覆盖原文件 |
| 携转结果 xlsx 输出 | `C:\Users\Administrator\Desktop\携转结果.xlsx` | v19 新增：含"携转明细"+"网格统计"两个 Sheet，自动覆盖原文件 |
| 携转结果字段 | 手机号码⇥最近一次申请时间⇥申请内容⇥GRID_NAME | v7 固化：Tab分隔，固定4字段 |
| 微信窗口标题 | 微信 | `xdotool search --name "微信"` |
| 微信窗口使用方式 | **直接激活当前窗口**，禁止搜索聊天/导航通讯录/切换聊天对象 | v8 固化 |
| 微信目标聊天 | **置顶第1个聊天窗口** | v7 固化：无需额外选择 |
| 文件复制方式 | 桌面文件管理器 Ctrl+C | v7 固化 |
| 文件粘贴方式 | 微信聊天框 Ctrl+V → **回车键发送** | v8 固化 |
| 去重网格消息格式 | **v20 升级**：标题行+汇总行+网格明细行（含号码列表）+合计行 | v20：详细分网格列表格式，详见 SKILL.md §8.2 |
| Excel 截图路径 | `D:\携转查询\携转结果截图.png` | v12 新增：PNG 无损格式，保证文字清晰 |
| Excel 打开命令 | `start excel "C:\Users\Administrator\Desktop\携转结果.txt"` | v12 新增：需处理可能的文本导入向导 |
| 截止小时来源 | **程序执行开始时间的小时数**（v15 变更，24小时制） | v15 变更，v20 沿用 |
| 中文文本输入方式 | 文本编辑器中转：写文件→deepin-editor打开→Ctrl+A→Ctrl+C→微信Ctrl+V | v7 固化：**禁止 xdotool type** |
| 消息发送方式 | **回车键（Return）**发送，不点击发送按钮 | v8 固化 |
| 文本编辑器 | deepin-editor | v8 固化 |
| 弹窗处理 | 一律点确认 | |

---

*以上为 2026-10-27 至 2026-10-30 八轮实测沉淀；执行时若遇控件 id/路径变动，先以文本 find 复勘，再回本文档修订版本号。*
