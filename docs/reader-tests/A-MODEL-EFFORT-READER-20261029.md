# A-MODEL-EFFORT-READER-20261029 · 结果文档

## 原目标

修复 jrnl #1908：现代版本的 JSON 风格 YAML 配置不再误触发 1.x 升级提示；同时正确识别真正旧版；没有 `version` 的配置保留原有回退行为。按维护者验收评论，判定规则为：

- `version` 存在且低于 2.0 → 旧版，进入升级流程；
- `version` 存在且不低于 2.0 → 不是旧版；
- 没有 `version` → 沿用原有 `is_config_json()` 检查。

## 实现

- `jrnl/upgrade.py`
  - 新增 `_parse_config_version()`：把 `version` 解析为数值元组，支持 `v4.1` 前缀、YAML 数值 `4.6`、预发布后缀；不可解析返回 `None`。
  - `is_old_version()`：先读取配置的 `version`，可解析时返回 `tuple < (2,)`；否则回退到 `is_config_json()`。
  - 未改 `jrnl/config.py`、`jrnl/install.py` 或依赖声明。
- `tests/unit/test_upgrade.py`：20 个用例，覆盖现代 version、真正旧版、2.0 边界、无 version、非 JSON 配置、数值 version、不可解析 version。
- `tests/bdd/features/upgrade.feature`：2 个 CLI 场景。
- `tests/data/configs/modern_version_json_style.json`、`tests/data/configs/old_version_json_style.json`：场景夹具。

## 实际采用／拒绝的页面建议

采用：

- 「已有会话能完成任务就沿用」「按可用客户端二选一，不改全局配置」：全程使用当前会话，不新开模型客户端、不改全局模型配置。
- 「型号不可用或数据不能走该服务，就沿用合规可用入口」：本会话可见后端模型为 `deepseek-v4.1-flash[1m]`，不在页面的 Sol/Sonnet/Opus/Haiku 表内，按该回退规则继续。
- 「按原标准接收 diff；修 bug 重放原触发路径，新增回归须能暴露原问题」：先重放 CLI 路径，再回退生产代码验证回归失败。

拒绝／未采用：

- 页面示例的 `claude --model claude-sonnet-5-5 --effort medium` 与 `codex --model gpt-6.1-sol ...`：本机是否可用无法核实，且任务明确要求不为实验启动额外模型或改全局配置，故未执行。
- 页面的分档、成本与团队实践部分（Cloudflare、CodeRabbit、VulcanBench 等）与本次单项修复无直接关系，未据此调整入口；也没有可核的单任务账单或完整计时可供比较。
- 页面引用的 02/08 等其他章节未展开阅读。

## 验收证据

环境：Windows，Python 3.13.5，jrnl 4.6（editable 安装），pytest 9.1.1，pytest-bdd 8.1.0，pytest-xdist 3.8.0，ruff 0.16.2，black 26.5.1，tox 4.58.0。项目未提供 poetry/poe，使用工作目录内 `.venv`（已 gitignore）复现锁定版本。

| 检查 | 命令 | 结果 |
|---|---|---|
| 回归在原代码失败 | 临时回退 `jrnl/upgrade.py` 后跑 `tests/unit/test_upgrade.py` + 新 BDD 现代配置场景 | 11 failed, 10 passed |
| 回归在修复后通过 | 恢复后同上 | 21 passed |
| 全量 unit | `pytest tests/unit -n0 -q` | 214 passed, 27 skipped，退出码 0 |
| 全量 BDD | `pytest tests/bdd/test_features.py -n auto -q` | 499 passed, 17 skipped，退出码 0 |
| 原测试入口 | `tox -q -e py --` | 713 passed, 44 skipped，退出码 0 |
| lint | `ruff check .` | All checks passed，退出码 0 |
| 格式 | `black --check .` | 77 files unchanged，退出码 0 |

未运行／受限范围：

- `poe test` 与 `poe lint` 无法按原样运行（本机无 poetry/poe）；已分别用等价命令 `tox -q -e py --`、`ruff check .`、`black --check .` 覆盖。`poetry check` 未运行。
- 文档站检查 `poe docs-check` 未运行（需要本地文档服务与 npx，与本改动无关）。
- `pytest-clarity` 因 Windows wheel 构建失败未安装；它不是 pytest 的 `required_plugins`，不影响测试结果。
- `tox` 首次运行因依赖无上界拉到不兼容的 pytest-bdd 9.0.0 而失败；在 tox 环境内钉到 `poetry.lock` 版本后通过，未改依赖声明。

手工 CLI 重放（隔离 HOME，显式 `--config-file`，临时目录，已清理）：

- 现代 JSON 风格配置（`"version": "v4.1"`）：退出码 0，只提示配置更新并输出日记条目，无 "The following journals will be upgraded"。
- `"version": "1.9.5"` 的 JSON 风格配置：出现 "The following journals will be upgraded"，输入 `n` 后安全中止，未改动任何真实配置。

## 纠正轮次

1. 初版实现即按维护者规则落地；临时回退生产代码验证新回归有效（11 个失败）后恢复，未需要返工修改逻辑。
2. 测试环境第一次解析到 pytest 9.2 + pytest-bdd 9 导致 BDD 全挂，按 `poetry.lock` 钉版本后恢复；tox 环境重复出现同一问题，同样处理。这两次是环境纠正，不是代码返工。

## 模型、effort、等待与费用边界

- 实现：`deepseek-v4.1-flash[1m]`（会话可见标识）；effort 未知。
- 审查／复核：本读者未单独启动审查模型或返工轮次；按任务要求应由非读者另行复核。
- 等待：未记录完整墙钟时间；各测试命令耗时见上（unit 约 1.5s，BDD 约 22s，tox 全量约 33s）。
- 费用：无单任务账单，未知；未使用付费服务、凭据或账号用量接口。

## 返工补充（2026-11-01，原文保留并追加）

本节只记录返工轮相对上文的变化与仍未完成的验证；上文历史内容与数字不改写，也不继承为本次结果。

### 修正

- `version` 键存在但不可解析（如源码构建的 `version: source`、空串、`null`）不再等同于「没有 version」，不再落入 `is_config_json()` 的 1.x 回退；实现改为按「键是否存在」判断，只有完全缺少 `version` 键才回退。上一轮把该偏差固化成期望的 `test_unparseable_version_falls_back_to_json_check` 已改为断言不回退，并补 `source`/`""`/`null`/`"dev"` 参数化、YAML 风格 `version: source`、复用已加载配置、`load_or_install_jrnl` 不二次加载等用例。
- 重复加载：`is_old_version()` 增加可选 `config` 参数；`jrnl/install.py` 只改一行，把 `load_or_install_jrnl()` 已加载的 `config` 传入，避免同一配置解析两次（重复键配置会因此重复告警）。`jrnl/install.py` 超出原允许写域，属任务文件第 3 条允许的最小扩展，改动仅 `is_old_version(config_path)` → `is_old_version(config_path, config)`。

### 本次实际执行

- `python -m py_compile` 三个改动文件：通过。
- 从生产源码 AST 抽出 `_parse_config_version()`/`is_old_version()`（仅把 `load_config`/`is_config_json` 换成 JSON 桩）做 26 项语义检查：通过。
- 同一组 4 个不可解析用例对返工前代码复跑：`source`、空串、`null` 三项返回旧版（错误），证明新回归能暴露原问题；`"dev"` 原本可解析，作守卫。

### 未执行及原因

按任务文件第 6 条，本轮未在用户电脑安装或更新任何软件/依赖，只使用现有隔离环境；现有环境缺 `ruamel.yaml`、`ruamel.yaml.clib`、`cryptography`、`keyring`、`parsedatetime`、`pyxdg`、`tzlocal`、`pytest`、`pytest-bdd`、`pytest-xdist`、`tox`、`ruff`、`black`、`poetry`/`poe`，故以下全部未运行：

- `python -m pytest tests/unit/test_upgrade.py`、全量 unit/BDD、`tox -q -e py --`、`ruff check .`、`black --check .`；
- `source`、现代、旧版、无 `version` 四类临时配置的 CLI 重放与 journal 内容不变核验；
- 「重复 `load_config` 是否真的打印两次告警」的端到端实测（只由单测锁定「传入配置时不重载」）。

恢复条件：提供含上述依赖的既有隔离环境（按 `poetry.lock` 钉 pytest 9.1.1 / pytest-bdd 8.1.0）或在允许安装的轮次执行；入口为 `python -m pytest`、`tox -q -e py --`、`jrnl --config-file <临时配置>`。

### 页面卡点与页外帮助（补齐上一轮遗漏）

- 页面「型号与档位须在当前账号、客户端和提供方可用…」：本会话可见后端 `deepseek-v4.1-flash[1m]` 不在页面型号表内，页面未给非列表提供方的 effort 核对办法；按同页「沿用合规可用入口」处理，effort 记未知。
- 页面只讲模型选择，不含本仓测试入口；从项目 `CLAUDE.md`、`pyproject.toml`、`poe` 任务名取入口。
- 「运行原检查」与「不得安装依赖」在环境缺项时冲突；选择不安装并报告精确缺项，不以缩小范围宣称全套通过。
- 记录路径两处要求不一致（本次派发正文写 `reader-tests/`，任务文件第 4 条写 `docs/reader-tests/` 且旧 u1 只读）：两处都写，u1 以「原文保留＋末尾追加」处理。
- 维护者验收评论只写「有 version 就比较、没有才走 JSON 检查」，未提不可解析值；按任务文件第 1 条对 `source` 的明确要求处理。

### 与 u1 记录的差异

`reader-tests/A-MODEL-EFFORT-READER-20261029-u1.md` 为上一轮读者记录，本轮在其末尾追加返工记录、未改写上文。差异：上文把不可解析 version 当作「没有」并回退为旧版；上文称两份记录「内容一致」不准确；上文列出的 pytest/BDD/tox/lint 数字是历史结果，本轮未能复跑，不作为本次验收证据。

### 返工轮的模型、effort、等待与费用

- 实现／返工：`deepseek-v4.1-flash[1m]`（会话可见标识）；effort 未知；单任务账单未知；完整计时未记录；未使用付费服务、凭据或账号用量。
- 非作者复核仍待外部完成；本次返工不自称新盲读。
