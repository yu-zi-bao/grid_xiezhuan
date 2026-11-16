# IBOP_OA 控件定位备忘（2026-10-28）

## 控件外观（用户截图确认）
- 所属页面：福建移动统一4A门户 → 应用资源 → 应用资源登录
- 页面 URL：https://4a.fjit.cmcc:30002/iam/v1/#/appResource/appResLogin
- 应用卡片要素：
  - 图标：左上方形方块，内含显示器图形 + 蓝色字母 “e”
  - 应用名称：**IBOP_OA**（黑色粗体）
  - 说明文字：“单点登录地址”（灰色小字）
  - 操作按钮：浅蓝色圆角按钮，文案 “IBOP…”（意为 IBOP 登录）
  - 卡左上角有空心复选框，右上角有蓝方块/黄星图标
  - 卡片左下角显示关联账号：7000734
  - 卡片右下角：绿色圆点 + “当前浏览器”

## 程序化定位方法（已实测可行）
1. 先确认处于门户「应用资源登录」页（顶部一级 Tab“应用资源”→ 菜单“应用资源登录”）。
2. 应用列表渲染在与父页同源的子 iframe 中：
   - iframe src 形如：https://4a.fjit.cmcc:30002/appResource/v1/?…
   - 可通过顶层 `document.querySelectorAll('iframe')` 按 src 含 `/appResource/` 筛选。
3. 在 iframe 文档中定位含文本 **IBOP_OA** 的最小块级元素（应用卡片）。
4. ⚠️ 该卡片**没有专属“登录按钮”**，不要再去找按钮；正确动作为：识别 IBOP_OA 文本节点（DIV.appName_1）并**直接点击该文本节点**即触发单点登录（详见下方“实测最佳点击方式”）。
5. 点击后通常由系统拉起 IBOP-OA 目标页（http://10.53.182.13:9900/…），注意观察是否新开标签页/页面跳转；进入后的主界面导航（四宫格 hover → 服务变更 → 携号转网申请查询）详见 `references/ibop-runbook-optimized.md` §2。

## 关键区分
- 应用资源列表里还有“经分”、“BOP…”、“RDMP…”等同级卡片，切勿混淆；
- 文本匹配务必以 `IBOP_OA`（下划线）为锚点，BOP/RDMP 仅为名称尾部相似。
## 实测最佳点击方式（2026-10-28 验证通过）
- 结论：**不要去找“登录按钮”**，IBOP_OA 卡片上没有专属登录按钮。
- 正确动作：识别 IBOP_OA 文本节点（实测为 DIV.appName_1，位于 card_wrap>card_box>card_content>…>card_info_container_right>appName_1 链路的末端），把鼠标移到该节点中央直接点击即可。
- 效果：触发 4A 单点登录 → 自动新开标签页进入 IBOP-OA（标题“中国移动客户关系管理系统”，URL 形如 http://10.53.182.13:9900/ibop/4aplugin/4A_index_hidden.jsp?…）。
- 技术注记：可用脚本取该节点 getBoundingClientRect() 中心，按 order 派发 PointerEvent(mousemove/pointerdown)/MouseEvent(mousedown/…/click) 序列即可生效；点在文本节点比在外层卡片容器更可靠。
---

## v2 补充（2026-10-28 第二次执行）

### 搜索框导航控件（v5 已弃用 ❌）
- 搜索输入框：`input#search_val`（placeholder 含"关键字"）
- 搜索按钮：`#search`
- ⚠️ **v5 弃用**：实测搜索按钮被 SPAN 元素遮挡（`INPUT_TARGET_OBSCURED`），无法可靠点击
- **一律改用四宫格悬停导航**，详见 `references/ibop-runbook-optimized.md` §2

### 查询表单控件（功能 iframe 内）
| 条件 | ID | 类型 | 备注 |
|------|----|------|------|
| 归属地市 | `history_open_home_county` | select | 龙岩=597 |
| 归属区县 | `history_open_home_county` | select | ""=所有 |
| 申请类型 | `history_index_id` | select | -1=所有 |
| 申请状态 | `history_online_bi_status` | select | -1=所有 |
| 起始时间 | `history_TimeChooseStart` | input | 需 native setter + change |
| 结束时间 | `history_TimeChooseEnd` | input | 需 native setter + change |
| 每页条数 | `select[name="rp"]` | select | 10/15/20/30 |
| 查询按钮 | `history_queryBtn` | **a** | 非 button |
| 导出按钮 | `history_exportBtn` | **a** | 非 button |

### 导出弹窗控件
- 弹窗容器：`.l-dialog`（LigerUI Dialog）
- 弹窗内 iframe：`cocibopexcept.jsp`
- 刷新按钮：`a#nextBtn`（文本"刷新"）
- 下载链接：`a[href*="CocRemoteFileDownload"]`
- 下载 URL 格式：`/ibop/CocRemoteFileDownload.do?fileid=CocExportMnpindex_<yyyyMMddHHmmss>&upload_type=cocdefault&format=xls`

### 文件下载中转方案
- curl 不可用（HttpOnly Cookie 限制）
- 方案：浏览器 `fetch(url, {credentials:'include'})` → `blob()` → POST 到 `127.0.0.1:18899`
- 本地接收服务：`/tmp/recv_file.py`（Python http.server）---

# 更新记录（2026-10-29 第二轮执行）

## 登录手机号变更
- 旧号码：13850686599
- 新号码：**13950880770**
- 登录方式不变：SIM KEY 认证

## 查询功能关键技术发现

### 1. 查询按钮的真实触发机制
- 查询按钮（`#history_queryBtn`）的 click 事件绑定：
  ```javascript
  sellers_table_list.clearAll();
  sellers_table_list.loadData();
  ```
- `loadData()` 触发 grid 的 `onGetDataDIY` 回调 → 调用 `qryCocElecChnl(param)`
- **关键**：直接调用 `qryCocElecChnl({page:1})` 不会加载数据到 grid，因为缺少 grid 提供的 callback
- 正确做法：`sellers_table_list.clearAll(); sellers_table_list.loadData();`

### 2. 时间赋值方法
- LigerUI 日期控件需要同时设置两处：
  ```javascript
  // 方法1：通过 LigerUI API（main world 中执行）
  liger.get('history_TimeChooseStart').set('value', '2026-10-29 00:00:00');
  // 方法2：通过 jQuery val（查询函数实际读取此值）
  $('#history_TimeChooseStart').val('2026-10-29 00:00:00');
  ```
- **必须**在 `world: "main"` 中执行，isolated world 无法访问 jQuery/liger

### 3. 后端 API 调用机制
- 函数：`$BsspUtilPub().invokeBssp(sysfunc_id, 'COC_MnpindexToeventQry', req, callback)`
- sysfunc_id = "20101252"
- 时间参数格式：去除所有分隔符 → "20261029000000"
- home_city = "597"（龙岩）

### 4. 导出流程（异步工单）
1. 点击导出 → 弹出"携号转网申请导出"对话框
2. 对话框内 iframe (`#except_blind_area_prepare`) 加载 `/ibop/common/coc/cocibopexcept.jsp`
3. 初始状态：step_1 绿色（等待处理），fileDiv 显示"当前工单正在等待处理中"
4. 点击"刷新"按钮（`#nextBtn`）轮询
5. 完成状态：step_3 绿色（`cfig_step_green_3`），fileDiv 显示下载链接
6. 下载链接格式：`/ibop/CocRemoteFileDownload.do?fileid=CocExportMnpindex_YYYYMMDDHHMMSS&upload_type=cocdefault&format=xls`

### 5. 查询结果（2026-10-29 10:30 快照）
- 今日（10-29）：73 条
- 昨日（10-28）：478 条
- 导出文件名：CocExportMnpindex_20261029102725.xls---

# v3 更新记录（2026-10-29 第三次执行）

## 登录手机号变更
- 旧号码：13850686599 / 13600987561
- 新号码：**13950880770**
- 登录方式不变：SIM KEY 认证

## 搜索框导航控件确认（v5 已弃用 ❌）
- 搜索输入框：`input#search_val`（placeholder 含"关键字"）
- 搜索按钮：`#search`（点击提交搜索）
- ⚠️ **v5 弃用**：实测搜索按钮被 SPAN 元素遮挡，无法可靠点击
- **一律改用四宫格悬停导航**（`DIV.dropmenu` hover → 服务变更 → `a#760010671252`，v6 起可直接 click）
- 详见 `references/ibop-runbook-optimized.md` §2

## 时间赋值控件（v3 关键发现）
- **必须**在 `world:"main"` 中执行，isolated world 无法访问 jQuery/liger
- **必须**同时设置 LigerUI 控件值和 jQuery val：
  ```javascript
  // LigerUI API
  liger.get('history_TimeChooseStart').set('value', '2026-10-29 00:00:00');
  // jQuery val（查询函数实际读取此值）
  $('#history_TimeChooseStart').val('2026-10-29 00:00:00');
  ```

## 查询按钮触发机制
- 查询按钮（`#history_queryBtn`）的 click 事件绑定：`sellers_table_list.clearAll(); sellers_table_list.loadData();`
- `loadData()` 触发 grid 的 `onGetDataDIY` 回调 → 调用 `qryCocElecChnl(param)`
- **直接调用 `qryCocElecChnl({page:1})` 不会加载数据到 grid**，因为缺少 grid 提供的 callback

## 导出弹窗控件补充
- 弹窗内 iframe id：`#except_blind_area_prepare`
- 完成状态 CSS class：`cfig_step_green_3`（step_3 绿色 = 处理完成）
- 下载链接格式：`/ibop/CocRemoteFileDownload.do?fileid=CocExportMnpindex_YYYYMMDDHHMMSS&upload_type=cocdefault&format=xls`

## 后端 API 调用机制
- 函数：`$BsspUtilPub().invokeBssp(sysfunc_id, 'COC_MnpindexToeventQry', req, callback)`
- sysfunc_id = "20101252"
- 时间参数格式：去除所有分隔符 → "20261029000000"
- home_city = "597"（龙岩）

## 导出文件字段（7列）
| 列 | 字段 | 说明 |
|----|------|------|
| A | 事件ID | |
| B | 归属地市 | 龙岩 |
| C | 归属区县 | 新罗/永定/上杭/武平/长汀/连城/漳平 |
| D | 手机号码 | |
| E | 申请时间 | YYYY-MM-DD HH:MM:SS.0 |
| F | 申请类型 | 申请过授权码成功/查询过携转资失败等 |
| G | 申请状态 | |

## 微信发送控件定位（v3 新增，v28 重构 Windows 窗口查找 ⭐⭐⭐⭐⭐）
- **v28 核心改进**：新版微信 4.0+ 将进程名从 `WeChat.exe` 改为 `Weixin.exe`，窗口类名也发生变化，导致 `FindWindow` 方式全部失效
- **v28 统一方案**：使用 `tasklist` 获取 `Weixin.exe` / `WeChat.exe` 进程 PID → `EnumWindows` + `GetWindowThreadProcessId` 匹配窗口
- **共享模块**：`scripts/wechat_window_helper.py`（v28 新增），所有脚本统一调用 `find_wechat_window()` 和 `activate_window()`
- **窗口激活改进**：使用 `AttachThreadInput` + `SetForegroundWindow` 组合方式，解决 Win10 前台窗口锁定问题
- 旧版 Linux/deepin 方式（已弃用）：`xdotool search --name "微信"` → 窗口ID
- ⚠️ 坐标为实测值，每次执行前需动态确认窗口位置和大小

## 客户网格归属 CSV（v3 新增）
- 路径：`/data/home/cmcc/Fuxiaozhi/客户网格归属.csv`
- 编码：GBK（**必须** encoding='gbk'）
- 大小：约 91MB，217万条记录
- 字段：MSISDN, HOME_COUNTY, GRID_ID, GRID_NAME
- 用途：按手机号码关联匹配 GRID_NAME

## 携转结果文件规格（v3 新增，v7 固化 ⭐⭐⭐⭐⭐）
- 文件名：`携转结果.txt`
- 编码：UTF-8，Tab分隔
- **固定4字段（v7 固化）**：手机号码 / 最近一次申请时间 / 申请内容 / GRID_NAME
- **保存路径（v7 固化）**：`/data/home/cmcc/Desktop/携转结果.txt`（**自动覆盖原文件，不询问**）
- **数据源（v7 固化）**：从查询导出数据中提取手机号码，不再笼统说"读取.xls"
- **网格匹配（v7 固化）**：读取 `/data/home/cmcc/Fuxiaozhi/客户网格归属.csv` 按号码关联 GRID_NAME

## 去重网格消息格式（v3 新增，v7 固化，v8 优化，v20 格式升级 ⭐⭐⭐⭐⭐）
- **格式（v20 升级）**：详细分网格列表格式——标题行 + 汇总行 + 每个网格的号码数量和号码列表 + 合计行，详见 SKILL.md §8.2
- **XX（v15 变更）** = **程序执行开始时间的小时数**（24小时制，如 17 时），填入标题行 `（截至XX时）`
- **grid_name（v20 升级）** = 按 GRID_NAME 分组，每个网格列出号码数量和全部手机号码，号码间用顿号（、）连接
- **中文发送方式（v7 固化）**：**必须文本编辑器中转**（写文件→deepin-editor打开→Ctrl+A→Ctrl+C→微信Ctrl+V），**禁止 xdotool type**
- **发送方式（v8 固化）**：**回车键（Return）发送**，不点击发送按钮

## 微信发送文件规格（v7 固化，v8 优化 ⭐⭐⭐⭐⭐）
- **复制方式（v7 固化）**：桌面文件管理器中 **Ctrl+C** 复制《携转结果.txt》
- **目标窗口（v7 固化）**：桌面微信**置顶第1个聊天窗口**就是目标，无需额外选择
- **窗口使用方式（v8 固化）**：**直接激活微信当前窗口**，禁止搜索聊天/导航通讯录/切换聊天对象
- **粘贴发送（v8 固化）**：微信聊天框 **Ctrl+V** 粘贴文件 → **回车键发送**