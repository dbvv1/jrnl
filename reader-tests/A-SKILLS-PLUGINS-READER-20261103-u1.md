# A-SKILLS-PLUGINS-READER-20261103 · 读者记录（u1）

## 0. 读者结论

读者问题：修一个依赖库相关的 CLI 错误时，需要装 Skill／插件，还是已有资料与工具就够？

结论：**不需要装 Skill／插件。** 本任务是一个清楚的小 bug，仓库源码、现有单测、公开 issue 与已有候选 PR 已经足够；按页面「已有工具够用就不装」和「先定位实际依赖，再选文档或源码」执行即可。全程未安装、未启用、未调用任何 Skill／插件／MCP。

但真实 CLI 复现与测试执行被环境卡住：仓库未提供可用的 jrnl 运行时／测试依赖，本任务又禁止安装依赖。因此代码改动与回归测试已落到工作树，真实 CLI／pytest 验证未完成，保留待验。

## 1. 开发任务做到哪一步

任务目标：jrnl #2011，`timeformat` 的 `%d` 等字符串覆盖值不再因 YAML 解析崩溃，同时保留布尔、数值、结构化值及嵌套键行为。

已做：

1. 核原 issue #2011 当前状态：open，Unplanned 里程碑；复现命令
   `jrnl -month 06 --config-override timeformat "%d" --short`；ruamel YAML 抛
   `ScannerError: found character that cannot start any token`（line 1, column 13）。
   维护者给出的临时绕过是给值加引号：`--config-override timeformat "'%d'"`。
2. 核上游候选 PR #2110 当前状态：open，1 个 commit，无 review／assignee／milestone。
   其 diff 在 `make_yaml_valid_dict()` 中捕获 `YAMLError`，失败时回退为
   `{input[0]: input[1]}`（原样字符串），并新增 `%d`、`%Y-%m-%d %H:%M` 回归测试。
3. 用候选 PR 的 `.diff` 原样应用到工作树（`git apply --check` 通过后 apply），未另造投稿。
4. 在候选测试基础上补了两个覆盖验收点的用例：
   - `["colors.body", "%d"]`：带点号的嵌套键在 YAML 失败回退后仍保持原键，交给
     `override.py` 的 `_convert_dots_to_list` 展开；
   - `["colors", "{body: red, title: blue}"]`：结构化（YAML flow mapping）值仍按原行为解析为 dict。
5. 对改动文件做 `python -m py_compile` 语法检查，通过。
6. 用 PyYAML 做了**辅助性** YAML 规范核对（明确不能替代 jrnl 真实 CLI）：
   `timeformat: %d`、`timeformat: %Y-%m-%d %H:%M`、`colors.body: %d` 均抛
   `ScannerError`；`linewrap: 23`、`encrypt: false`、结构化 mapping 正常解析。
   这与 issue 报告的 ruamel 行为方向一致，但 ruamel 本体未安装，不能作为验收证据。

产物（工作树相对路径）：

- `jrnl/config.py`：`make_yaml_valid_dict()` 捕获 `YAMLError` 并回退为字面字符串。
- `tests/unit/test_parse_args.py`：候选回归测试 + 嵌套键回退、结构化值保留用例。
- 本文件 `reader-tests/A-SKILLS-PLUGINS-READER-20261103-u1.md`。

未做／待验：

- 真实 CLI 复现（原行为失败、候选通过）；
- `pytest tests/unit/test_parse_args.py`、`poetry run poe test`、ruff／black；
- 临时 journal 与无关配置按原契约保留的端到端确认；
- 未提交、未推送、未切换分支。

## 2. 页面怎样支持能力选择

页面提供的决策方式与本次判断：

| 页面内容 | 本次判断 |
|---|---|
| 「已有工具够用就不装，项目已有 Skill 就复用」 | 仓库有 `CLAUDE.md` 测试／贡献说明与完整单测，但没有项目级 `SKILL.md`；没有需要新装的能力。 |
| 「第一步先查已有能力，避免重复安装」 | 先列出本会话已有 Skill／插件（含 Superpowers、Context7、Figma 等）；本任务均不需要启用。 |
| Context7 行：Agent 总写旧 API 才用 | 本次不是 API 版本写错，而是 YAML 解析失败；issue/PR 已给出行为与修法，不装 Context7。 |
| 库作者窄 Skill 行 | ruamel.yaml 没有对应窄 Skill，且官方 YAML 规范足以解释 `%` 开头标量非法，不需要。 |
| Serena 行：经常替换完整方法才用 | 只改一个函数内的几行，普通文本编辑足够，不需要符号编辑工具。 |
| Superpowers 行：「别只为清楚的小 bug 新装整套」 | 本任务就是清楚的小 bug，不进入完整设计／计划流程。 |
| 「先定位实际依赖，再选文档或源码」 | 采用「源码优先」：从 `override.apply_overrides()` 追到 `config.make_yaml_valid_dict()`，确认唯一调用点，再核对候选 PR 补丁。 |

页面还说明「确定采用后，用 [项目原测试命令或操作] 验收任务结果」；这一步因环境缺依赖无法执行（见卡点）。

## 3. 所选资料／能力是否真正用上

真正用上：

- **仓库 `CLAUDE.md`**：测试命令说明、「不得用临时脚本触碰真实 config/journal」的约束，直接决定了本次只用合成配置／临时目录的方案，未运行任何会写默认配置的脚本。
- **源码** `jrnl/config.py`、`jrnl/override.py`、`jrnl/args.py`：定位唯一 YAML 解析点、点号键展开逻辑与 `--config-override` 参数形态。
- **现有测试** `tests/unit/test_parse_args.py`、`tests/unit/test_override.py`：沿用 `TestDeserialization` 风格补用例，并核对原有布尔／数值覆盖断言。
- **公开 issue #2011**：拿到复现命令、错误类型、版本与临时绕过方式。
- **公开候选 PR #2110 的 `.diff`**：原样应用，未另写实现。
- **`pyproject.toml`**：确认运行时依赖为 ruamel.yaml 等，解释环境缺失。
- **`docs/advanced.md`**：核对 `--config-override` 的点号与空值用法。

未用上：

- 没有安装或调用任何 Skill／插件／MCP；因此「安装成功」「自动加载」均未验证，不能声称产品优劣或模型采用。
- 页面中的 Cargo／opensrc、Node／TanStack 配方与 Python 项目不适用；只采用了其「从消费方追到实际实现」的方法。

## 4. 卡点

### 4.1 环境限制

- 页面句：「**确定采用后，用 [项目原测试命令或操作] 验收任务结果。**」
- 缺什么：当前环境没有 jrnl 的运行时依赖 `ruamel.yaml`、`cryptography`、`keyring`、`parsedatetime`、`pyxdg`、`tzlocal`；也没有 `poetry`、`pytest`、`tox`、`ruff`、`black`、`poe`；仓库内无 `.venv`。可用解释器只有系统 Python 3.13（另有裸 Python 3.12），均导入不到上述包。
- 后果：无法按项目 `CLAUDE.md` 的 `poetry run poe test` 或 `pytest` 运行；无法启动真实 `jrnl` CLI；无法用真实 ruamel 验证「原行为失败、候选通过」。
- 为什么没有绕开：任务明确要求本机不安装或更新软件／依赖／插件，必须记录环境卡点、不换通道绕过。未使用 `pip install`、`uv run --with`、`poetry install` 等任何安装路径。
- 做错过什么：一开始按项目文档假定 `poetry` 可用，直接执行 `poetry --version` 才发现不存在；随后才改用解释器 `importlib.util.find_spec` 逐项确认缺失包。

### 4.2 页面缺口

1. 页面句：「**✅ 查实际行为，从调用方追到已解析包、项目补丁和具体模块；查版本用法，再看官方文档或 Context7。**」及其后的 `cargo metadata`、`pnpm/node` 示例。
   - 缺什么：只有 Rust/Cargo 与 Node/TanStack 的依赖定位配方，没有 Python／pip／poetry 的等价入口（例如如何从消费包定位已安装的 ruamel.yaml 版本与模块路径）。
   - 本次替代：读 `pyproject.toml`、用解释器 import 探测、读 issue／PR 与 YAML 规范；这只能算手工定位，不是页面配方。
   - 做错过什么：先做了一次跨用户目录的全盘 `find` 找 ruamel，2 分钟超时；之后才收敛为直接检查解释器可导入性。
2. 页首页尾只讲 Skill／插件选择与加载，没有覆盖「接回已有上游候选 PR 并验证」的流程。
   - 缺什么：如何判定候选状态、如何只取候选 diff 应用而不另造投稿、如何留下「原失败／候选通过」的回归证据。
   - 本次替代：自行用公开 `.diff` + `git apply --check/apply`，测试按仓库现有 `TestDeserialization` 风格补。
3. 输入层面：任务文件以 `docs/decisions/skills-and-plugins.md@main` 引用页面，附入了全文，但未附**解析提交 SHA**。
   - 缺什么：无法把 `@main` 固定到具体版本；只能记录内容指纹（见第 7 节）。
   - 影响：页面内容若在两次读取间变化，无法证明本次读的是哪一版。

### 4.3 读者误解

- 误以为项目文档列出的 `poetry`／测试环境在接收端已就绪；实际没有。这是环境限制，不是页面表述错误。
- 曾考虑是否需要 Context7 来查 ruamel 的版本行为；按页面「已有资料够用就不装」和 issue/PR 已给出行为，判断不需要，未安装。
- 没有把 PyYAML 的辅助核对当成 jrnl 的真实复现；报告中已明确标注它不能替代真实 CLI。

## 5. 页面之外还翻了什么（页外帮助）

- GitHub 原 issue #2011 页面：复现命令、`ScannerError`、版本、维护者 quoting 绕过、Unplanned 里程碑。
- GitHub 候选 PR #2110 页面与其 `.diff`：当前 open、1 commit、无 review；实际补丁与测试内容。
- 仓库 `pyproject.toml`：运行时与开发依赖清单。
- 仓库 `CLAUDE.md`、`CONTRIBUTING.md`：测试／贡献流程，以及「不得触碰真实用户 config/journal」的约束。
- 仓库 `docs/advanced.md`：`--config-override` 的点号与示例。
- 仓库源码 `jrnl/config.py`、`jrnl/override.py`、`jrnl/args.py`；测试 `tests/unit/test_parse_args.py`、`tests/unit/test_override.py`。
- 本机解释器与包探测：确认缺 `ruamel.yaml` 等依赖（不属于 a1dbv 文档）。
- 尝试读取 ruamel.yaml 上游 `error.py` 源码页确认 `YAMLError` 导出，返回 404，未取得；未据此替代任何运行验证。

未读取 a1dbv 的其他教程、地图、TASKS 或旧实测结果。

## 6. 验证记录与准确输出

已运行：

```text
$ git apply --check <候选 PR #2110 的 .diff>
CHECK_OK

$ git apply <候选 PR #2110 的 .diff>
 jrnl/config.py                |  9 ++++++++-
 tests/unit/test_parse_args.py | 12 ++++++++++++
 2 files changed, 20 insertions(+), 1 deletion(-)

$ python -m py_compile jrnl/config.py tests/unit/test_parse_args.py
PY_COMPILE_OK
```

补充测试后工作树 diff 统计：

```text
 jrnl/config.py                |  9 ++++++++-
 tests/unit/test_parse_args.py | 17 +++++++++++++++++
 2 files changed, 25 insertions(+), 1 deletion(-)
```

辅助性 PyYAML 核对（**不是** jrnl 真实 CLI，也不替代 ruamel）：

```text
'timeformat: %d'                  -> ERROR ScannerError
'timeformat: %Y-%m-%d %H:%M'      -> ERROR ScannerError
'colors.body: %d'                 -> ERROR ScannerError
'linewrap: 23'                    -> {'linewrap': 23}
'encrypt: false'                  -> {'encrypt': False}
'colors: {body: red, title: blue}'-> {'colors': {'body': 'red', 'title': 'blue'}}
```

未运行及原因：

- `pytest`／`poetry run poe test`／`tox`：pytest、poetry、tox 均未安装，且 ruamel.yaml 等运行时依赖缺失；安装被任务禁止。
- 真实 `jrnl` CLI 复现：无法导入 jrnl（`ModuleNotFoundError: No module named 'ruamel'`），且不得用依赖桩或读源码冒充真实 CLI。
- `ruff`／`black`：未安装；仅做了 `py_compile` 语法检查。

## 7. 页面输入记录

- 页面引用：`docs/decisions/skills-and-plugins.md@main`。
- 附入正文：任务文件中页面全文完整（标题「该装哪些 Skill 与插件」至末尾参考段），未见正文缺失。
- 内容指纹：页面正文（任务文件第 37–268 行，含标题到末段）共 15191 字符 / 24162 字节（UTF-8），SHA-256 `e3cb8f3a7d81e54a49614d7713ab084ce2a2cfeab31d200301d1ffac2139c353`。
- 解析提交：未随附；记为输入卡点（见 4.2 第 3 项）。

## 8. 恢复条件与后续验收

需要有 jrnl 运行时依赖与 pytest 的环境（本机不自行安装）。恢复后按序执行：

1. `pytest tests/unit/test_parse_args.py -k deserialize` 或 `poetry run poe test`；
2. 用临时目录中的合成 config 与 journal：
   `jrnl --config-file <临时配置> -month 06 --config-override timeformat "%d" --short`，
   核对输出形如 `02 Title 1`；
3. 同法核对非字符串覆盖：布尔（如 `encrypt false`）、数值（如 `linewrap 20`）、结构化 mapping，以及 `colors.body` 等嵌套键；
4. 在应用候选补丁前的基线上运行新增用例，确认原实现失败、候选实现通过；
5. 核对运行后临时 journal 与无关配置键未被改写；
6. 跑 ruff／black 与项目完整测试。

当前状态：实现与回归用例已就位，真实执行待上述环境恢复；未提交、未推送，交 dot-A 接收。

## 核对

核对人于工作树内独立复核，不以读者自报为准。

### 1. 按任务验收：未做成

任务「怎样算做成」要求：真实 CLI 用同输入复现字符串覆盖、另核非字符串覆盖、留下原行为失败/候选通过的回归、跑项目相关测试与检查，并确认临时 journal 与无关配置按原契约保留。以上均未执行：

- 本机系统 Python（3.13.5）导入不到 `ruamel`、`cryptography`、`keyring`、`parsedatetime`、`pyxdg`、`tzlocal`；无 `poetry`、`pytest`、`pytest-bdd`、`tox`、`ruff`、`black`、`poe`，仓库无 `.venv`。与读者所记一致。
- 因此没有真实 `jrnl` CLI 输入/输出、没有 pytest/ruff/black 结果，也没有端到端「临时 journal 与无关配置保留」的证据。`py_compile` 与 PyYAML 核对只能算辅助检查，不能替代任务规定的真实 CLI。
- 环境缺依赖与「本机不安装或更新软件/依赖/插件」的约束冲突；读者没有越界安装、换通道，这一点处理正确，但按任务验收仍不能算做成。

### 2. 独立核到的证据

1. 改动范围：仅 `jrnl/config.py`、`tests/unit/test_parse_args.py` 与本记录；未改依赖声明/锁文件、页面或其他功能。`git diff --check` 无空白错误。
2. 候选补丁：取公开 PR #2110 的 `.diff` 比对，`jrnl/config.py` 的导入、try/except 与回退三处与工作树逐字一致；测试文件为候选 12 行加 `colors.body` 参数 1 行、结构化值用例 4 行，共 17 行，与 `git diff --stat` 一致。PR #2110 与 issue #2011 当前均为 open，issue 里程碑为 Unplanned，与读者记录相符。
3. 核心行为（用 ruamel.yaml 0.19.1 的公开发布 wheel 解包到临时目录后经 `sys.path` 直接加载，未安装、未改项目依赖；同时核了最低支持版 0.17.22）：
   - `YAML(typ="safe").load("timeformat: %d")`、`"timeformat: %Y-%m-%d %H:%M"`、`"colors.body: %d"` 均抛 `ScannerError`，且 `ScannerError` 是 `YAMLError` 子类；`ruamel.yaml.error.YAMLError` 在 0.19.1 与 0.17.22 均存在。
   - 以补丁等价实现复核：三种 `%` 输入由抛 `ScannerError` 变为返回字面字符串；`linewrap 23`、`encrypt false`、`highlight true`、结构化 mapping、`colors.title`、`editor` 等原有结果不变。函数层面补丁方向正确。
   - 但完整 `import jrnl.config` 仍因缺 `xdg` 失败，真实 CLI 未跑通，上述结果不能替代 CLI 验收。
4. 页面输入：读者给的 15191 字符/24162 字节、SHA-256 `e3cb…` 与 a1dbv 参考副本 `docs/decisions/skills-and-plugins.md` 当前内容逐字节一致（含末尾换行），正文完整、无缺失；缺的只是解析提交 SHA。

### 3. 逐条卡点判断

| 读者卡点 | 判断 | 理由 |
|---|---|---|
| 缺可运行 jrnl 环境，无法按页面用项目原测试命令验收 | page | 页面/任务要求用项目原测试命令验收，却没写明运行前置（依赖已备或允许安装），而任务同时禁止安装；读者正确记录环境卡点、未绕过。 |
| 页面只给 Cargo/Node 依赖定位配方，缺 Python/pip/poetry 等价入口 | page | 对 Python 项目确有缺口；读者先做全盘 `find` 是多余动作（model 侧低效），但改用解释器探测后定位方式合理。 |
| 页面引用 `@main` 未附解析提交 SHA | page | 输入未把页面固定到具体版本；内容指纹本身正确（见上）。 |
| 页面不含「接回已有候选 PR 并验证」流程 | model | 页面职责是能力选择，不含开发/PR 流程；任务第 14、17 行已交代先核状态、可接回候选，读者自行用公开 `.diff` + `git apply` 完成，属预期内，不应记为页面缺口。 |

### 4. 读者未意识到的错误/缺口

1. 嵌套键用例只测中间结果：`["colors.body", "%d"]` 断言的是 `make_yaml_valid_dict` 返回 `{"colors.body": "%d"}`，没有经 `apply_overrides` / `_convert_dots_to_list` 走到实际 config 树；即使点号展开逻辑坏了该用例也会通过，无法证明「嵌套键行为保留」。（复核源码后实际路径可展开，但测试覆盖不足。）
2. 吞掉全部 `YAMLError` 的口径变化未评估：如 `--config-override colors "{body: red"` 这类坏结构化值，旧行为在解析处抛 `ScannerError`，新行为静默把 `colors` 覆盖成字符串，稍后按 mapping 使用时才以无关的 `AttributeError` 等方式暴露；读者只讨论了 `%d`，未记录这一面。
3. §8 恢复条件不完整：`pyproject.toml` 有 `required_plugins = ["pytest-bdd"]` 与 `addopts = ["-n=auto"]`（需 `pytest-xdist`），只装 pytest 仍会在启动期失败；读者的缺失工具清单漏了 `pytest-bdd`/`pytest-xdist`，所写 `pytest ... -k deserialize` 不能直接执行。
4. 补丁注释「`%` starts a YAML directive」不准确：`%d` 不在行首，不是 directive，而是标量起始处的保留指示符；不影响行为，但作为长期留在代码里的注释是错的说法。
