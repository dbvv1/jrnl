# A-AGENT-CHOICE-READER-20261103 · u1 读者记录

页面：`docs/01-agents/README.md@main`（接收端附入任务文件的全文）
任务：照页面选入口，实际处理 jrnl #1990（`--import` 与 `--format` 同用给明确不兼容提示，保留正常导入与独立导出）。
记录约定：命令中的 `<repo>`、`<deps-python>`、`<tmp-config>`、`<tmp-input>` 均为合成占位，不写本机绝对路径与内网地址。

## 1. 入口选择与理由

- 页面《30 秒结论》第一句：“**已有入口能完成任务就保留；只有缺少必要能力或验收反馈时才换。** 把一个正在发生的小修复交给它，从复现做到检查通过，再决定是否需要别的 Agent。”
- 页面《第一步：在已有入口里交付一项真实修改》：“**已经处于能读仓库、改文件和运行检查的会话，就直接继续；不必另启动一个 CLI。** Claude Code 接第三方后端、云端任务或 IDE 中的现成 Agent 同样先走这条。”
- 本次选择：**保留当前会话继续做**。会话已能读仓库、改文件、跑测试，符合页面第一条；没有出现“必要能力或验收反馈缺失”的证据，因此没有另起 Codex/Cursor，也没有为了照抄型号改账户或配置。页面同段也写明“记录当前可见的客户端、模型与 effort，未显示的项记未知”。

按页面要求分项报告：

| 项 | 实际值 |
|---|---|
| 可见客户端 | Claude Code 形态的 Agent 会话（workflow 子代理，headless） |
| 实际后端模型 | `deepseek-v4.1-flash[1m]`（会话环境中显示） |
| 可观察配置 | 未见 `--model` / `--effort` / 模型覆盖参数；effort 未显示，记未知 |
| 未试能力 | 未启动 Codex CLI、Cursor、云端入口；页面说无须同时跑三款，未提供的入口不假装试过 |

页面选型表里“本机仓库里的日常功能、补测试、小改动”一行的入口是 Codex CLI，已有 Claude Code 工作流则用 Claude Code。本会话属于后者的“已有工作流”，因此按页面保留。

## 2. 任务、现状核对与复现

任务要求：`jrnl --import --format <T>` 同时出现时，给出明确的“两者不能同用”提示；正常的 `--import`（stdin 或 `--file`）与单独的 `--format` 导出保持可用。

- 先读项目规则：根目录 `CLAUDE.md` 要求测试走现有 pytest 基础设施、禁止用临时脚本碰真实配置/journal；本记录中的 CLI 验证都显式传 `--config-file <tmp-config>`，journal 也指向临时目录。
- 确认工作树差量：起手时已有 2 个修改文件——`jrnl/args.py`、`tests/unit/test_parse_args.py`。页面没有给“工作树里已有别人/上一轮的候选实现”时的处置办法，我按任务卡的“已有实现可接回验证，不另造同题投稿”处理：先把它当候选核对，再重放验证，没有另写一份同题实现。
- 与既有候选比对：读取既有候选补丁 `pr2120.patch`（属任务允许的“既有候选”，不是旧读者结果）。当前工作树 diff 与该补丁逐行一致，唯一差异是 `jrnl/args.py:456` 帮助示例中的家目录占位从 `user1` 形式改为通用的 `user` 形式；该改动只改帮助文本，不改参数逻辑。
- 线上状态核对失败：本机没有 `gh`；GitHub API 返回 rate limit；`WebFetch` 对 github.com 被网络策略拦下。因此无法确认 #1990/#2120 的实时状态，只以工作树中的候选补丁作为待验证实现。这是环境限制，不能据此推断上游状态。

原行为（基线，`git show HEAD:jrnl/args.py` 换回后实测）：

| 命令 | 退出码 | 关键输出 |
|---|---|---|
| `--import --format jrnl` | 2 | `invalid choice: 'jrnl' (choose from boxed, calendar, dates, fancy, heatmap, json, ...)` |
| `--import --format json` | 1 | 先正常加载 journal，随后 `No importer found for file type 'json'.` |
| `--import --format whatformats` | 2 | `invalid choice: 'whatformats'`，并列出全部导出格式 |

候选行为（当前工作树）：

| 命令 | 退出码 | 关键输出 |
|---|---|---|
| `--import --format jrnl` | 2 | `jrnl: error: argument --format: not allowed with argument --import` |
| `--import --format json` | 2 | 同上 |
| `--import --format whatformats` | 2 | 同上 |
| `--import --format=json` | 2 | 同上 |
| `--format json --import` | 2 | 同上 |

正常路径回归：

| 命令 | 退出码 | 结果 |
|---|---|---|
| `--import --file <tmp-input>` | 0 | `1 imported to default journal` |
| 从 stdin 执行 `--import` | 0 | `1 imported to default journal` |
| `--format json` | 0 | 输出合法 JSON；导入 1 条时为 1 条 entry |
| `--format text` | 0 | 追加 stdin 导入后显示 2 条 entry |
| `--help` | 0 | `--import` 帮助只剩 `--file`，不再列 `--format` |

实际命令统一为：

```text
<deps-python> -c "import sys; sys.argv[0]='jrnl'; from jrnl.main import run; sys.exit(run())" --config-file <tmp-config> <测试参数>
```

## 3. 环境与检查结果

- 系统 Python 3.13 缺 `ruamel.yaml`、`cryptography`、`keyring`、`parsedatetime`、`tzlocal` 和 `pytest`；`poetry` 未安装。项目规则与任务卡都要求不安装/更新本机依赖，因此没有用 pip/poetry 安装。
- 发现上一轮尝试留下的 uv 依赖环境 `<deps-python>`（含 pytest 9.1.1 和全部运行依赖），直接复用，未新增安装、未改全局配置。这属于“沿用已有依赖”。
- 回归有效性：把 `jrnl/args.py` 换回 `HEAD` 版本、清掉该文件旧 `__pycache__` 后跑新增用例：4 个参数化用例全部失败（`whatformats` 失败在断言没有 “not allowed with argument --import”；`json`、`--format=json`、反序三种为 `DID NOT RAISE SystemExit`），`test_format_without_import_is_unaffected` 通过；候选版本 55 passed。说明新增回归确实覆盖了原行为失败、候选通过。
- `pytest tests/unit -q -n0`：199 passed, 27 skipped。
- `pytest tests/bdd/test_features.py -q -n0 -k "import or format"`：31 passed, 1 skipped；全量 BDD：497 passed, 17 skipped。
- `ruff check .`：All checks passed。`black --check .`：76 files would be left unchanged。
- 未运行：`poe lint` 的 `poetry check` 步骤（poetry 不在本机）；`poe test` 的 tox 路径。没有隐藏这些未跑项。

## 4. 卡点（页面哪一句、缺什么、做错过什么）

1. **页面“先读项目规则，确认工作树差量与写者”**：照做了，但页面没有说明“工作树里已有一份未提交的候选实现”时该继续改、还是只验证。起手只有 2 个 modified 文件，没有作者信息。我按任务卡的“已有实现可接回验证，不另造同题投稿”选择只验证，没有在页面上找到这一判断依据。这是页面缺口，不是代码卡点。
2. **页面“已经处于能读仓库、改文件和运行检查的会话，就直接继续”**：会话能读写，但本机没有项目依赖管理器和运行依赖；页面不覆盖“依赖缺失但禁止安装”时的做法。通过复用上一轮遗留的 uv 依赖环境解决，没有安装任何东西。属环境缺口。
3. **任务卡“先核当前状态”**：`gh` 不存在、GitHub API 限流、`WebFetch` 域名被拦，无法在线核对 #1990/#2120。只能读既有候选补丁并在本地验证；上游实时状态仍是未知项。属环境限制。
4. **我做错的一步**：第一次用基线跑新增回归时没有清理 `jrnl/__pycache__/args.cpython-313.pyc`，结果 4 个用例都报 `DID NOT RAISE`，与直接调用 `parse_args` 的实测（`whatformats` 会抛 SystemExit）矛盾。清掉该 pyc 后重跑，才得到正确的分项原因（`whatformats` 是提示文案不符，其余三种是不抛异常）。记录此点，避免把工具缓存造成的假结果当成代码行为。
5. **残余边界（未修）**：页面/任务要求的是 `--format`；实际 argparse 允许长选项前缀缩写，`--import --form json` 会绕过这段原始参数检查，落到旧路径；隐藏别名 `--export` 也不在检查内。为保持与既有候选 #2120 一致，没有扩大改动，仅记录为残余风险。

## 5. 页面之外还翻过什么

- 任务文件 `job.md`（页面全文与任务约束）。
- 目标仓 `CLAUDE.md`（测试/配置保护规则）。
- 源码：`jrnl/args.py`、`jrnl/commands.py`、`jrnl/controller.py`、`jrnl/messages/MsgText.py`、`jrnl/plugins/__init__.py`、`jrnl/plugins/jrnl_importer.py`、`jrnl/config.py`、`jrnl/install.py`。
- 测试：`tests/unit/test_parse_args.py`、`tests/conftest.py`、`tests/lib/fixtures.py`、`tests/data/configs/basic_onefile.yaml`、`tests/data/journals/basic_onefile.journal`。
- 配置与入口：`pyproject.toml`、`jrnl/__main__.py`。
- 既有候选补丁 `pr2120.patch`（用于确认工作树实现与其一致）。
- 上一轮遗留的 uv 依赖环境（只用于找现有依赖，未读其中旧读者的解题文件或结果）。
- 尝试过的线上来源：GitHub issue #1990、PR #2120（`gh`、API、`WebFetch` 均不可用）。

## 6. 产物与状态

- 代码改动：`jrnl/args.py`、`tests/unit/test_parse_args.py`（起手即存在；本次核对、重放、检查，未再改动逻辑）。
- 本记录：`reader-tests/A-AGENT-CHOICE-READER-20261103-u1.md`。
- 未提交、未推送、未切换分支、未改任务文件；验证用的临时 config/journal 只落在临时目录。
- 结论：选定入口为“保留当前已有会话”，页面给出的“先复现、最小改动、补失败回归、跑相关检查、自己重放”路径足以指导本次修复；做成状态以本地 diff、CLI 输出与回归结果为准，上游 #2120 的实时状态仍因网络不可达而未核。

## 核对（非读者复核，2026-11-03）

**结论：任务做成（taskDone=true）。** 以下为在隔离 worktree 内独立重跑的实际结果，不采信自报。

### 独立复算
- 工作树 diff 只有 `jrnl/args.py`、`tests/unit/test_parse_args.py`。与上游候选 PR #2120 head `f4c6e2d` 比对：`args.py` 除一行帮助示例脱敏外逐行一致，`tests/unit/test_parse_args.py` 完全相同；该 PR 补丁对基线 `HEAD` 可 `git apply --check` 通过。
- 基线（`git show HEAD:jrnl/args.py`）+ 新增回归：4 个参数化用例失败；`--import --format whatformats` 是文案断言失败（抛出 SystemExit，但提示仍是 invalid choice），`json`、`--format=json`、反序三种为 `DID NOT RAISE SystemExit`；`test_format_without_import_is_unaffected` 通过。与读者记录的原因一致。
- 候选：`tests/unit/test_parse_args.py` 55 passed。
- 候选 CLI（临时 config/journal，`<deps-python>` 直调 `jrnl.main.run`）：`--import --format {jrnl,json,whatformats}`、`--import --format=json`、`--format json --import` 均 exit 2，stderr 含 `jrnl: error: argument --format: not allowed with argument --import`；`--import --file`、stdin `--import` 均 exit 0；`--format json`、`--format text`、`--format tags`、`--export json` 均 exit 0，json 输出合法。`--format yaml` 在临时布局下 exit 1（提示需导出到目录），属既有行为，与本次改动无关。
- 基线 CLI：`--import --format jrnl`／`whatformats` exit 2 invalid choice，`--import --format json`／`--format=json`／反序 exit 1 `No importer found...`；正常导入与独立导出可用。
- 检查：`tests/unit` 199 passed/27 skipped；BDD 定向 31 passed/1 skipped；全量 BDD 497 passed/17 skipped；`ruff check .` 通过；`black --check .` 76 files unchanged。`poe lint` 的 `poetry check` 与 tox 路径未跑（本机无 poetry），与读者披露一致。

### 对卡点的判定
1. 工作树已有候选、无写者信息 → **页面缺口（page）**：页面只要求“确认差量与写者”，未给“已有未提交候选/写者不明”时继续改还是只验证的处置规则。
2. 缺依赖且禁止安装 → **页面前提未写（page）**：页面“会话能运行检查”的前提在本机不成立，也未说明如何发现已有隔离环境；页面《第一步》已写“缺依赖且不能安装时保留未跑项”，读者复用上一轮 venv 的处理合理，属环境限制。
3. 无法在线核对上游 → **读者尝试不足（model）**：实测 `git ls-remote`／`git fetch` 正常，可取到 PR #2120 head `f4c6e2d`；只有 open/merged 状态仍需 API/网页，这一项确未核。
4. 旧 pyc 导致假失败 → **读者自身操作失误（model）**：已自我识别并在清理后重跑，方法无误。
5. 残余边界 → **读者枚举不全（model）**：除 `--form`、`--export` 外，`--impor`／`--impo`／`--imp` 等 `--import` 缩写同样绕过原始字符串检查。

### 读者未意识到的
- `--import` 的 argparse 长选项缩写（`--imp`／`--impo`／`--impor`）不被新增检查覆盖；`--form`（`--format` 缩写）与隐藏别名 `--export` 也同样。实测这些组合仍输出旧的 `No importer found ...`，不是新的不兼容提示。属范围外残余，但卡点记录不完整。
- “无法在线核对上游”的结论过强：`git ls-remote`／`git fetch` 可用，已确认 #2120 head 与工作树一致；仅 open/merged 状态未核。
- 读者称页面不覆盖“依赖缺失且禁止安装”的做法，但页面《第一步》已写明“缺依赖且不能安装时保留未跑项，不能归因为模型弱”，属漏读。
- 新增检查在 argparse 处理 `--help`／`--version` 之前执行：基线 `jrnl --version --import --format json` 打印版本 exit 0、`--help ...` 打印帮助 exit 0，候选两者都变成 usage 错误 exit 2。读者只测了单独 `--help`，未覆盖该优先级副作用；属次要行为回归（与上游候选同源）。

### 页面能否指导选路
页面“已有入口能完成就保留”“先读项目规则、核工作树差量”“自己核 diff、重放原触发路径”足以指导本次选路与验证；本次选“保留当前会话”符合页面结论。缺口集中在“已有未提交候选/写者不明”的处置规则，以及缺依赖时如何找已有隔离环境，建议各补一句；上游实时状态与别名／缩写边界不影响本次选路结论。

## 修订（第二轮，2026-11-03）

> 本轮是原 result_branch 上从 `655d8a9` 的定点返工，不是新读者实测。首轮记录、原提交与失败原样保留，仅在文末追加。

### 1. 做到哪一步、产物在哪

继续按页面《30 秒结论》和《第一步》选择**保留当前会话**，没有另起 Codex/Cursor/云端入口。页面要求的“先读项目规则、确认工作树差量与写者”照做：本轮起手工作树干净，HEAD 就是 `655d8a9`，只有单一写者。

返工内容（`jrnl/args.py`）：

- 先把参数在裸 `--` 处截断，`--` 之后的正文／检索词不再当选项；因此 `-- --import --format json` 与 `--format json -- --import` 恢复为合法输入。
- 按 argparse 的实际语义解析长选项，而不是字符串等值比较；覆盖 `--imp`／`--impo`／`--impor`（`--import` 的唯一前缀）、`--form`（`--format` 的唯一前缀）、隐藏别名 `--export`，以及 `--i`／`--exp` 等其它唯一前缀。
- 检测到 `--help`／`-h`／`--version`／`-v`／`--diagnostic` 等 preconfig 命令时跳过本互斥检查，交给原有 parser/controller 顺序处理，保留它们的原有优先级。
- 报错文案按识别到的选项名生成：`argument --format: not allowed with argument --import`；使用别名时是 `argument --export: not allowed with argument --import`。
- 未改 `jrnl/messages/MsgText.py`（本轮不需要）、依赖、扫描器、白名单、全局配置或权限。

回归（`tests/unit/test_parse_args.py`）：

- 错误组合扩到 11 个：原 5 个（含 `--import --format jrnl`）＋ `--imp`／`--impo`／`--impor`、`--import --form`、`--import --export`、`--import --exp`。
- 新增 version 优先级 2 例、help 优先级 2 例、`--` 边界 2 例；保留 `--format json` 单独导出用例。

产物（仓库相对路径）：

- `jrnl/args.py`
- `tests/unit/test_parse_args.py`
- 本记录 `reader-tests/A-AGENT-CHOICE-READER-20261103-u1.md`

未提交、未推送、未切换分支、未改任务文件、未改 a1dbv 页面或其他卡。

### 2. 实际验证（修前失败、修后通过）

把 `jrnl/args.py` 换回 `655d8a9`（即本轮修改前）并清掉 `__pycache__`，跑同一套 `tests/unit/test_parse_args.py`：

- 修前：12 failed / 56 passed（12 个新用例全部失败；原有用例仍通过）。
- 修后：68 passed。

CLI 实测（临时 config／journal，`<deps-python>` 直调 `jrnl.main.run`）：

| 命令 | 退出码 | 关键结果 |
|---|---|---|
| `--import --format jrnl` | 2 | `argument --format: not allowed with argument --import` |
| `--import --format json` | 2 | 同上 |
| `--import --format whatformats`（未知格式） | 2 | 同上 |
| `--import --format=json` | 2 | 同上 |
| `--format json --import` | 2 | 同上 |
| `--imp --format json` | 2 | 同上 |
| `--impo --format json` | 2 | 同上 |
| `--impor --format json` | 2 | 同上 |
| `--import --form json` | 2 | 同上 |
| `--import --export json` | 2 | `argument --export: not allowed with argument --import` |
| `--import --exp json` | 2 | 同上 |
| `--import --file <tmp-input>` | 0 | 正常导入 |
| 从 stdin 执行 `--import` | 0 | `1 imported to default journal` |
| `--format json` | 0 | 合法 JSON |
| `--format text` | 0 | 正常输出正文 |
| `--help` | 0 | 帮助 |
| `--version --import --format json` | 0 | 打印版本（优先级保留） |
| `--import --format json --version` | 0 | 打印版本（优先级保留） |
| `--help --import --format json` | 0 | 打印帮助（优先级保留） |
| `--diagnostic --import --format json` | 0 | 打印诊断（优先级保留） |
| `-- --import --format json` | 0 | 作为正文追加，journal 中出现 `--import --format json` 条目 |
| `--format json -- --import` | 0 | 作为检索词 `--import`，正常完成导出 |

原套件结果：

- `pytest tests/unit -q -n0`：212 passed, 27 skipped（首轮 199/27；净增 13 个用例）。
- `pytest tests/bdd/test_features.py -q -n0`：497 passed, 17 skipped；定向 `-k "import or format"`：31 passed, 1 skipped。
- `ruff check .`：All checks passed。
- `black --check .`：76 files would be left unchanged。
- 未运行：`poe lint` 的 `poetry check` 步骤与 tox 路径，本机无 `poetry`／`tox`，且按约束未安装。未跑项未被隐藏。

### 3. 卡点（页面哪一句、缺什么、做错过什么）

1. **页面“先读项目规则，确认工作树差量与写者”**：页面仍只要求“确认”，没有给“已有未提交候选且写者不明时继续改还是只验证”的处置规则。首轮遇到该情况；本轮起手工作树干净，不触发，但缺口仍在。
2. **页面“已经处于能读仓库、改文件和运行检查的会话，就直接继续”**：页面默认检查能跑，未写“缺依赖且禁止安装时如何找到已有的隔离环境”。本轮复用上一轮遗留的 `<deps-python>` 只作解释器，未安装、未读其中旧读者文件或结论。
3. **页面未覆盖“选项值本身长得像选项”**：`--config-override` 一次吃两个值，argparse 会把 `--import --config-override editor --format` 里的 `--format` 当作值。基线 exit 0，本轮预扫描会误报 exit 2。该边界不在返工清单内，记为未修残余；现有清单内的缩写、别名、help/version 与 `--` 边界均已处理。
4. **环境卡点（不是页面方法问题）**：本机 Windows 控制台默认 GBK，第一次跑 `--format text`／`--version` 因输出含非 GBK 字符得到 `UnicodeEncodeError`、exit 1。这是环境编码，不是代码行为；设 `PYTHONUTF8=1`、`PYTHONIOENCODING=utf-8` 后复跑 exit 0，与基线一致。做错的一步是把首次 exit 1 当成了 CLI 行为，复跑后修正。
5. **原 page 解析提交／全文指纹**：本轮输入里只有 `job.md` 附入的页面全文，没有当时保留的解析回执或指纹。按任务要求“原件没有就明确无法恢复”，不拿当前页面回填，也不重跑 fresh reader。页面文本、输入回执、实际采用三者分开：页面=job.md 附文；输入回执=缺失；实际采用=本轮返工与验证。
6. **#2120 状态**：沿用负责人 2026-11-02 22:17 UTC 的公开观察（仍 open／未合，head `f4c6e2db`、base `90de4948`），本轮未联网复核，也不以 PR 状态代替本地 CLI 验收。

### 4. 页面之外还翻过什么

- 任务文件 `job.md`（页面全文与返工约束）。
- 目标仓 `CLAUDE.md`（测试 fixture、真实配置保护规则）。
- 源码：`jrnl/args.py`、`jrnl/controller.py`、`jrnl/commands.py`、`jrnl/main.py`。
- 测试与数据：`tests/unit/test_parse_args.py`、`tests/data/configs/basic_onefile.yaml`、`tests/data/journals/basic_onefile.journal`。
- 配置：`pyproject.toml`（ruff／black／tox 配置）。
- 既有依赖环境：上一轮遗留的 `<deps-python>`（只用 `--version`、import 检查和 pytest；未读旧读者结果或作者解题记录）。
- 未访问 a1dbv 页面、地图、TASKS、其他卡或旧结果；未使用任何账号、凭据或网络接口。

## 核对（第二轮，非读者复核，2026-11-03）

**结论：限定通过。** 本轮返工清单（缩写／别名、help/version 优先级、`--` 边界、修前失败／修后通过、未跑项披露）在隔离 worktree 内独立复算全部成立；但互斥检测仍有未修的“原 CLI 反例”，不能算完整验收。

### 独立复算
- diff 仍只有 `jrnl/args.py`、`tests/unit/test_parse_args.py` 和本记录；本记录为 90 行纯追加，首轮内容未回填、未改动。
- 修前（`jrnl/args.py` 换回 `655d8a9`）：同一新测试 12 failed / 56 passed；对上游原版 `90de4948` 跑同一份新测试为 11 failed / 57 passed（help/version 与 `--` 用例在原版本就通过）。候选：68 passed。
- 候选 CLI（临时 `<tmp-config>`／`<tmp-journal>`，`<deps-python>` 直调 `jrnl.main.run`）：11 个错误组合全部 exit 2，stderr 含 `argument --format: not allowed with argument --import` 或 `argument --export: not allowed with argument --import`；`--import --file`、stdin `--import`、`--format json`、`--format text` 均 exit 0；`--help`／`--version`／`--diagnostic` 与 `--import --format json` 同现仍 exit 0；`-- --import --format json` 作为正文 exit 0，`--format json -- --import` 作为检索 exit 0。
- 与 `655d8a9` 对照：两个 `--` 合法输入在 `655d8a9` 均 exit 2，本轮恢复；`--imp`／`--form`／`--export` 在 `655d8a9` 走到 exit 1 旧路径，本轮 exit 2 且文案正确。
- 套件：`tests/unit` 212 passed / 27 skipped；BDD 全量 497 passed / 17 skipped；定向 `-k "import or format"` 31 passed / 1 skipped；`ruff check .` 通过；`black --check .` 76 files unchanged。`poetry`／`tox` 不在本机，`poe lint` 的 `poetry check` 与 tox 路径未跑，与记录一致。
- `#2120` 按任务要求沿用负责人 2026-11-02 22:17 UTC 的公开观察，未联网复核；页面解析提交／全文指纹原件缺失，记录已明确“无法恢复”，未用当前页面回填。

### 未修反例（独立复现，均相对上游 `90de4948` 的原行为）
1. `--import --config-override editor --format`：上游原版 exit 0（`argparse` 把 `--format` 当作 `--config-override` 的第二个值，正常导入），候选 exit 2。`--config-override editor --format=json` 同类；`--config-override editor --import --format json`（`--import` 作为值、`--format` 为独立导出）上游 exit 0，候选也 exit 2。
2. `--import --list --format json`：上游原版 exit 0（`--list` 后置命令生效并输出 json），候选 exit 2。根因同属“裸参数预扫描”不认识值消费与后置命令覆盖。
3. 读者记录把第 1 类的基线写成 exit 0；按本轮修改前的 `655d8a9` 实测为 exit 2，只有上游原版 `90de4948` 是 exit 0。

### 卡点判定
1. 「工作树已有候选且写者不明」→ **model**：附入页面已明确写“已有未提交候选但写者不明时，保留原树、不切基线、覆盖文件或清缓存；先核归属与允许范围，再在独立副本验证候选，别另造同题实现”。读者称页面未给规则属漏读，不是页面缺口。
2. 「缺依赖且禁止安装如何发现已有隔离环境」→ **page（小缺口）**：页面已写“缺依赖且不能安装时保留未跑项”，但未写如何发现已有隔离环境；读者复用遗留 `<deps-python>`、未安装依赖，处理可接受。
3. 「选项值本身像选项」→ **model**：残余反例真实存在，属“按实际 CLI 语义修互斥检测”未完全修完；读者已测到 `--config-override` 一类，但基线归属错误，且未覆盖 `--format=json`、`--import` 作为值、`--list` 后置覆盖等同类。
4. Windows GBK 编码 → **model（环境诱发，已自行修正）**：首次 exit 1 是控制台编码而非 CLI 行为；设 `PYTHONUTF8=1`／`PYTHONIOENCODING=utf-8` 后 exit 0，读者已识别并纠正，不计为本轮失败项。
5. 页面解析提交／指纹缺失 → **page（输入回执缺口，非读者）**：按任务要求明确“无法恢复”，未回填、未重跑，处理符合要求。
6. `#2120` 状态 → **page（任务已给定观察）**：按要求沿用负责人公开观察、不联网复核，无缺陷。

### 页面能否指导选路
页面“已有入口能完成就保留”“先读项目规则、核工作树差量”“自己核 diff、重放原触发路径”足以指导选路与验证；本轮“保留当前会话”符合页面。附入页面已写出“已有未提交候选且写者不明”的处置规则，读者仍按旧印象称缺口。真正未覆盖的是“缺依赖且禁装时如何发现已有隔离环境”，建议补一句。缩写／别名／`--` 边界已修；`--config-override` 值消费与 `--list` 后置覆盖仍是未修反例，不影响本轮选路结论，但不支持“完整验收”。

### 残留与未运行
- 未提交、未推送、未切换分支、未改任务文件、未改页面与其他卡；临时配置／journal 只在临时目录。
- 未运行：`poe lint` 的 `poetry check`、tox 路径（本机无 `poetry`／`tox`，按约束未安装）。
