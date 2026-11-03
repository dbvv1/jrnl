# A-INSTRUCTION-FILES-READER-20261103-u1 记录

## 1. 做到哪一步与产物

已经按附入页面走完三步中的第一步和第三步，并完成一次真实的文档修改：

- `docs/usage.md`：在 `### Using Tags ###` 第一次介绍标签的示例后，加入 PowerShell 的引用／转义说明（+22 行）。
- `CLAUDE.md`：补充 `## Editing Documentation`（+9 行），给出文档入口、预览命令、CI 的 `docs-check` 及缺依赖时的完成标准。
- 本记录：`reader-tests/A-INSTRUCTION-FILES-READER-20261103-u1.md`。

没有新建 `AGENTS.md`，没有改生产代码、依赖、`tasks.py`、`mkdocs.yml`，没有提交、推送、切分支。工作树最终只有上述两个文件被修改（另有本记录）。

未完成／待验：

- 完整 jrnl 路径（实际写入、标签读取）未运行：本机没有 poetry、jrnl 包和运行依赖，且任务不允许安装。
- MkDocs 构建和 `poe docs-check`（Pa11y 可访问性）未运行：缺 poetry、mkdocs、npm 依赖和 docs server。
- 仅完成 PowerShell 参数探针、Markdown 链接静态检查、`git diff --check` 和最终 diff 审阅；不把未运行的文档构建写成通过。

## 2. 输入与页面指纹

- 任务文件：`job.md`（任务输入本身；未改）。
- `job.md` 全文指纹：`sha256:f9ccfd86cb26a8f5d468f6c2e03b8489c2e39ec4a743185909a43bd833ff11be`（22,796 bytes）。
- 附入页面正文（从标题 `# CLAUDE.md／AGENTS.md 怎么写` 到文件末）指纹：`sha256:7b8c59ff80cb8361d7ab958a8c9436ab690090d4fac7e9735dc6b2686b0a72e5`（9,932 字符 / 19,328 UTF-8 bytes）。
- 解析提交：`job.md` 只写了 `page: docs/decisions/instruction-files.md@main`，**未附解析提交 SHA，也未附接收端计算的内容指纹**。正文已附，所以不是“没附正文”的阻塞；我按附文自行计算了上面的指纹，但无法把它对应到某个上游 commit。这是输入元数据缺口（见卡点 1）。

## 3. 页面采用步骤

### 第一步：判断维护哪份指令

页面说“只用 Claude、已有 `CLAUDE.md` 已经好用的项目，继续维护原文件”，并说“没有的项目删掉，不为凑齐栏目新建流程”。目标仓根目录只有 `CLAUDE.md`，没有 `AGENTS.md`；本次也只有 Claude Code 一种工具。因此：

- 不新建 `AGENTS.md`，不复制整份规则。
- 对照页面骨架检查现有 `CLAUDE.md`：安装、测试、单测、BDD、lint、format、`docs-run`、架构、安全契约都已存在。
- 发现的具体缺口：`docs/**` 的改动有 CI 检查 `poetry run poe docs-check`（见 `.github/workflows/docs.yaml`），但 `CLAUDE.md` 的 Common Commands 只列了 `poetry run poe docs-run`，没有文档编辑入口，也没有这个检查。做本次纯文档任务时，现有规则无法说明“文档改动该跑什么检查”，属于页面说的“新任务暴露遗漏”。
- 只补了这一处：新增 `## Editing Documentation` 小节，保留全部原有规则。改动理由和实际作用见第 5 节。
- 页面里的 Cloudflare／Anthropic／NVIDIA 例子只用于说明“借什么、不照抄”，没有把它们的命令或规则复制进本项目；页面“静态检查先拿本仓样本试”提到的 `agents-md-lint` 也没有安装或运行——它不是 jrnl 的依赖，安装新软件越界，本次以项目自带的 docs 检查和链接静态检查替代。

### 第二步：加载入口与当前上下文（按当前接口能做到的程度）

- 起始目录：目标仓是单包仓库，jrnl 包就在仓库根，直接在仓库根开始；本次不访问附加仓库，不需要 `--add-dir`，也没有共享 `AGENTS.md`。
- 加载证据：本会话启动时的系统上下文直接包含项目 `CLAUDE.md` 全文（标注为 project instructions），这发生在任何工具调用之前；随后我出于核对又手动 `Read` 了一次。
- 工具侧核对：本会话是子代理，没有 `/memory`、`/context` 或对应的斜杠命令入口，无法取得“Memory files”列表页，因此**没有独立的工具侧加载列表证据**。不能把启动注入、手动读取和实际遵守混为一谈。
- 无工具复述：在启动上下文里可以直接看到以下约定：优先 `main` + PR；`poetry run poe test` 是完整检查；`Never Touch Real User Config/Journals`；black/ruff。由于我在复述前已经手动 `Read` 过文件，这次不能算严格的“无工具复述”；只能记为“规则在当前上下文可见”，启动展开证据依赖系统注入，不冒充 `/context` 证据。

### 第三步：参与眼前的真实修改

使用的真实任务是 jrnl issue #1977，不是为测规则编的题。修改前保留的验收条件：

1. 在 usage 文档第一次介绍标签的位置，给 PowerShell 用户可照用的引用／转义说明。
2. 用 PowerShell 实际运行文档给出的形式，确认传给程序的参数与预期字符一致。
3. 如 jrnl 可运行，再用临时 journal 验实际写入与标签读取；仅探针通过时明确标出完整路径待验。
4. 核 Markdown 链接、项目适用的文档检查和最终 diff；缺依赖保留环境缺口。
5. 不接触真实 journal／配置。

实施过程：

- 读 `docs/usage.md`，确认第一次介绍标签的位置是 `### Using Tags ###`（原第 64 行），第一个标签示例在 `jrnl Had a wonderful day at the @beach with @Tom and @Anna.`。
- 读 `docs/contributing.md`、`mkdocs.yml`、`docs.yaml`、`pyproject.toml`、`tasks.py`，确认文档源是 `docs/*.md`，站点用 MkDocs，CI 在启动 docs server 后运行 `poetry run poe docs-check`。
- 在标签示例后新增一个 `!!! note`，并在注释外放 PowerShell 代码块；原有“其他 shell 用 `\` 转义”的说明保持不动。
- 用两个 PowerShell 版本做参数探针，见第 4 节。
- 把文档入口和检查补进 `CLAUDE.md`，再用它指导检查尝试，见第 5 节。

## 4. 实际修改与验证

### 4.1 `docs/usage.md`

新增内容（diff 摘要）：

- `!!! note`：说明 PowerShell 中未加引号的 `@` 开头参数是 splatting 表达式，`jrnl @beach` 可能在 jrnl 看到前就丢掉标签，表现为打开编辑器或新建条目而不是筛选；PowerShell 的转义字符是反引号，`\@beach` 不行（反斜杠会原样传过去）；同样的引用保护 `#`、`&` 等保留字符。
- 三个等价形式：``jrnl `@beach``、`jrnl '@beach'`、`jrnl "@beach"`。
- 整句引用示例：`jrnl "Had a wonderful day at the @beach with @Tom and @Anna."`。

没有改原有 Composing Entries 里的通用 note，也没有动其他 shell 的说明；没有新增链接，因此没有新增失效锚点。

### 4.2 PowerShell 参数探针

用一个只打印 `sys.argv[1:]` 的探针代替 jrnl 可执行文件，验证 PowerShell 实际传给外部程序的参数（jrnl 在 Windows 上也是控制台脚本，参数到达方式相同；但这不是 jrnl 本身的参数解析）。

环境：PowerShell 7.6.9；Windows PowerShell 5.1.26100.9711；Python 3.13.5。

```text
探针命令形式                                   PS 7.6.9              Windows PowerShell 5.1
python probe.py @beach                         []                    []
python probe.py `@beach                        ["@beach"]            ["@beach"]
python probe.py '@beach'                       ["@beach"]            ["@beach"]
python probe.py "@beach"                       ["@beach"]            ["@beach"]
python probe.py \@beach                        ["\\@beach"]          ["\\@beach"]
python probe.py #beach                         []                    []
python probe.py '#beach'                       ["#beach"]            ["#beach"]
python probe.py "Had a wonderful day at the    ["Had a wonderful     ["Had a wonderful
@beach with @Tom and @Anna."                   day at the @beach      day at the @beach
                                               with @Tom and          with @Tom and
                                               @Anna."]               @Anna."]
```

结论：

- 裸 `@beach` 在两种 PowerShell 里都变成零个参数，和 issue #1976 的“打开编辑器”一致；结合源码 `jrnl/controller.py` 的 `_is_append_mode`/`append_mode`，无参数会进入 append mode 并打开编辑器。
- 反引号、单引号、双引号三种文档写法都让探针收到精确的 `@beach`；整句双引号收到完整原句。
- `\@beach` 收到的是字面 `\@beach`（JSON 显示为 `["\\@beach"]`），不是标签。
- 裸 `#beach` 是 PowerShell 注释，零参数；加引号后收到 `#beach`。
- 额外验证了 `&`：未加引号的 `I paid the bill & went home.` 在 PS 7 触发后台 job/解析错误；整句加单引号或双引号后收到完整字符串。文档 note 用“引用保护 `#`、`&`”覆盖这一点，没有为 `&` 单独加示例。

### 4.3 实际运行的检查与结果

| 检查 | 结果 |
|---|---|
| `git diff --check` | 退出 0，无空白错误 |
| 自定义 Markdown 相对链接检查（`docs/usage.md`） | 6 个相对链接，0 个缺文件／缺锚点 |
| 代码围栏计数 | 文件内围栏成对（42 个 fence 标记） |
| `poetry run poe test` | 退出 127：`poetry: command not found` |
| `poetry run poe docs-run` | 退出 127：同上 |
| `poetry run poe docs-check` | 退出 127：同上 |
| MkDocs／Markdown 渲染器 | `mkdocs`、`markdown` 均未安装；未运行文档构建 |
| jrnl／poetry 包 | `pip show` 未找到；无 `.venv`；`ruamel.yaml` 缺失 |
| Node/npm | Node v22.23.2、npm 10.9.8 存在，但无 `node_modules`；按约束未运行 `npm install` |
| 完整 jrnl 写入／标签读取 | 未运行，标为待验 |

因此，**文档构建和可访问性检查未通过也未失败，是未运行**；参数探针通过，但不能替代完整 jrnl 路径。

## 5. `CLAUDE.md` 改动的必要性与实际作用

改动前的事实：

- `CLAUDE.md` 的 Common Commands 有 `poetry run poe docs-run`，但没有 `docs-check`。
- `.github/workflows/docs.yaml` 在 `docs/**` 变更时启动 docs server 并运行 `poetry run poe docs-check`（Pa11y 可访问性）。
- `docs/contributing.md` 有文档编辑流程，但 `CLAUDE.md` 没有“改文档 → 读哪里 → 跑什么检查”的导航。
- 对本次纯文档任务，`poetry run poe test` 只覆盖 Python lint/test，不覆盖 docs；如果只看原 `CLAUDE.md`，会误以为没有适用的文档检查。

因此按页面“已有稳定配置：只修具体缺口；新任务暴露遗漏时，同次更新”，新增了 9 行 `## Editing Documentation`：

- 入口：`docs/*.md`、`mkdocs.yml`、`docs/contributing.md`（做什么 → 去哪里 → 为什么）。
- 预览：`poetry run poe docs-run`。
- 检查：CI 的 `poetry run poe docs-check`，并写明它需要 `npm install` 和已运行的 docs server。
- 完成标准：前提不具备时报告“未验证”，不要写成通过。

实际作用的具体证据：

- 这条新规则让我去核对了 `docs.yaml`、`tasks.py`、`package.json` 的命令与依赖，而不是只跑 `poe test`。
- 按它尝试 `poetry run poe docs-check`，实际得到退出 127；我据此在记录里写明文档检查未运行，没有把静态链接检查冒充成 docs-check 通过。
- 它没有改变原有规则：`Never Touch Real User Config/Journals`、main/PR 偏好、测试和代码风格全部保留。
- 原有 `Never Touch Real User Config/Journals` 也实际影响了做法：我没有用 `python -c` 或临时脚本去碰 `jrnl.config`，也没有运行 jrnl；PowerShell 侧只用打印 argv 的探针，不读写任何 journal/config。

规则冲突记录：`CLAUDE.md` 顶部写“ALWAYS prefer contributing to the `main` branch with a PR”，本次任务明确禁止提交、推送、切分支。两者冲突时按任务范围执行，没有做任何 git 写操作。

## 6. 卡点：页面哪一句、缺什么、做错过什么

| # | 页面／任务原句或位置 | 卡点与缺什么 | 我做了什么／做错了什么 |
|---|---|---|---|
| 1 | `job.md`“按什么做”：`记录解析提交与内容指纹` | `job.md` 只给 `page: docs/decisions/instruction-files.md@main`，没有解析提交 SHA，也没有接收端内容指纹；无法把附文对应到具体上游 commit。 | 正文已附，不阻塞阅读；我按附文自行算了 SHA-256 并记在第 2 节，同时明确“解析提交未知”。没有伪造 commit。 |
| 2 | 第二步：`v2.1.280+ 用 /memory 查看 AGENTS.md 路径`、`用 /context 查看 Memory files` | 本会话是子代理，没有 `/memory`、`/context` 入口，也没有工具侧的 Memory files 列表；页面给的核对方法在当前接口不可用。 | 改用“启动系统上下文注入的 `CLAUDE.md` 全文 + 手动 Read”作为可见性证据，并在记录里标明这不是工具侧列表证据；没有用复述冒充加载证据。 |
| 3 | 第三步：`直接用下一项本来就要做的修复或功能`；issue #1977 正文 | issue 正文说 PowerShell 用户“escape ampersands”，但链接的 #1405、#1963、#1976 实际报告的是 `@` 被 PowerShell 处理（#1963 的 `jrnl @tag` 进入 append mode，#1976 的 `jrnl @b` 打开编辑器），正文没有给出精确命令、错误文本或推荐写法。 | 我最初按字面把“ampersands”理解成 `&`，读链接 issue 后确认主因是 `@`；随后同时实测 `@`、`#`、`&`，文档以 `@` 为主，并用“引用保护 `#`、`&`”覆盖。这里既有 issue 表述不精确，也有我一开始的读者误解。 |
| 4 | 页面第一步骨架：`提交前检查：[项目规定的检查命令]` | 目标仓有 docs CI，但原 `CLAUDE.md` 没写 `docs-check`；纯文档任务没有可引用的文档检查入口。 | 按真实缺口补了 `## Editing Documentation`（第 5 节），没有新建 `AGENTS.md` 或重写整份文件。 |
| 5 | 页面：`命令从当前项目复制并试跑`；`完成需看到 [可观察结果]，并报告相关检查的实际结果` | 环境没有 poetry、mkdocs、jrnl 及其依赖，`poe test`／`docs-run`／`docs-check` 全部退出 127；不能安装或更新依赖。 | 保留为环境缺口：没有运行文档构建和 Pa11y；只做了 `git diff --check`、相对链接检查、围栏计数和 PowerShell 探针。没有把未运行写成通过。 |
| 6 | 任务“怎样算做成”：`如已能运行 jrnl，再以临时 journal 验实际写入及标签读取` | jrnl 没安装（无 poetry、无 jrnl 包、`ruamel.yaml` 缺失），无法走完整 jrnl 路径。 | 只做了 argv 探针，并在第 4.2 节明确“不是 jrnl 本身的解析”；完整写入／标签读取标为待验。没有用探针冒充实跑。 |
| 7 | 页面第一步：`把已知环境条件写进实际命令，不只放在旁注` | `docs-check` 必须先有 docs server 和 `npm install`；项目 `tasks.py` 没有“启动 server 再检查”的组合命令，而本次写范围不允许改 `tasks.py`。 | 在 `CLAUDE.md` 里把前提写在同一条规则内（`docs-check` 需要 `npm install` 和已运行的 server），但没有做成单条可直接复制的完整命令。这是页面的“写进命令”要求与本项目结构／写范围之间的部分缺口。 |
| 8 | 目标仓渲染配置：`mkdocs.yml` 只启用 `admonition`，没有 `superfences` | 没把握在 `!!! note` 内嵌 fenced code 能按预期渲染，且本机无法构建 MkDocs 验证。 | 第一稿把代码块放在 note 内缩进的位置有犹豫；最终把代码块放在 note 外、用普通句子引入，note 自身只保留行内代码。没有把未验证的渲染写法硬塞进注释。 |
| 9 | 执行过程（非页面） | 首次用 `curl` 调 GitHub REST API 遇到速率限制；首次把 issue HTML 放在 `/tmp`，Git Bash 与 Python 的路径映射不一致导致 `FileNotFoundError`。 | 改用 GitHub 网页 HTML + WebFetch 读取 issue；把临时文件放到工作树内的临时目录后重跑。两处都保留了首次失败记录。 |
| 10 | `CLAUDE.md` 顶部：`ALWAYS prefer contributing to the main branch with a PR`；任务输入：`不提交、不推送、不切换分支` | 项目规则与本次任务限制冲突。 | 按任务限制执行：只在工作树改文件，没有 commit/push/checkout；在记录里标明冲突，没有擅自开 PR。 |

## 7. 页面之外翻了什么

按页面允许的范围（原 issue、目标仓现有指令／贡献规范、相关文档／源码／检查配置及页面直接引用的资料）：

- 原 issue：GitHub #1977 正文；链接的 #1405、#1963、#1976 三个实际 PowerShell 报告。读取方式：WebFetch + 直接抓取公开 HTML（REST API 被速率限制）。
- 目标仓指令与贡献规范：`CLAUDE.md`、`CONTRIBUTING.md`、`docs/contributing.md`。
- 目标仓文档与配置：`docs/usage.md`、`docs/reference-config-file.md`（`#tagsymbols` 锚点）、`mkdocs.yml`、`pyproject.toml`、`tasks.py`、`package.json`。
- CI 配置：`.github/workflows/docs.yaml`、`.github/workflows/testing_prs.yaml`。
- 源码（只读，判断行为）：`jrnl/controller.py`（`_is_append_mode`、`append_mode`、`_has_only_tags`）、`jrnl/args.py`（composing 帮助文案）、`jrnl/config.py`（`tagsymbols` 默认 `#@`）、`jrnl/os_compat.py`。
- PowerShell 实测：PowerShell 7.6.9、Windows PowerShell 5.1.26100.9711；探针和输出见第 4.2 节。
- 没有读页面所属项目的其他教程、旧读者答案或页面所在地图；`job.md` 里的附文是唯一方法指南。

## 8. 恢复条件

- 若恢复 poetry 环境：先按项目说明安装依赖（本次未安装），再运行 `poetry run poe docs-run`，另开终端运行 `poetry run poe docs-check`；另跑 `poetry run poe test`。
- 若要让完整 jrnl 路径通过：用临时配置和临时 journal 运行文档中的三种 PowerShell 形式，确认 `@beach` 被识别为标签筛选，并验证整句写入后标签可读；不要使用真实用户 jrnl 配置目录或真实 journal。
- 若需要核对页面版本：需接收端提供 `docs/decisions/instruction-files.md@main` 的解析提交 SHA 或接收端指纹；本记录只提供附文的自算指纹。
- 本次无需再改代码或页面；剩余都是环境与输入元数据待验。

## 核对

核对人独立复核（只读检查＋另起 PowerShell 参数探针，未改读者产物）。

### 一、事实核对

- 指纹：`job.md` 22,796 bytes、`sha256:f9ccfd86…ff11be`；附文 9,932 字符 / 19,328 UTF-8 bytes、`sha256:7b8c59ff…b0a72e5`，均与记录一致。`job.md` 确实没有解析提交 SHA。
- 改动范围：工作树只有 `docs/usage.md`（+22）和 `CLAUDE.md`（+9）被修改，另有本记录；没有新建 `AGENTS.md`，没有改 `tasks.py`、`mkdocs.yml`、生产代码或依赖，没有 commit/push/checkout。
- 链接与格式：`docs/usage.md` 的 6 个相对链接均指向存在的文件与锚点；42 个围栏标记成对；`git diff --check` 退出 0。
- PowerShell 复核（PowerShell 7.6.9、Windows PowerShell 5.1）：裸 `@beach`、裸 `#beach` 均为零参数；反引号、单引号、双引号、整句双引号均得到预期字符；`\@beach` 得到字面 `\@beach`；裸 `&` 在 PS7 触发后台 job、在 5.1 触发解析错误。与记录一致。
- 源码复核：`jrnl/controller.py` 的 `_is_append_mode`／`_has_only_tags` 与 `Journal.filter(tags=args.text, ...)` 支持文档叙述：仅标签参数进入搜索过滤，零参数进入 append／编辑器。
- 上游 issue：#1405（`jrnl --debug test tag @todo`）、#1963（`jrnl @` 进入 append）、#1976（`jrnl @b` 打开编辑器）均是 PowerShell 吞掉 `@`；#1977 正文的“escape ampersands”与实际报告不一致。读者以 `@` 为主线、附带覆盖 `#`／`&` 的判断正确。
- 环境：无 poetry、mkdocs、markdown，`ruamel.yaml` 缺失、无 `.venv`；文档构建、Pa11y 与完整 jrnl 未运行属实，读者标为待验，没有谎报通过。

### 二、卡点逐条判定

| 读者 # | 判定 | 说明 |
|---|---|---|
| 1 缺解析提交／指纹 | 页面／输入包 | 输入元数据缺口，不阻塞；读者自算指纹准确。 |
| 2 无 `/memory`、`/context` | 页面 | 页面按交互式客户端写核对步骤，子代理没有这些入口，也未给替代；读者明确区分“当前上下文可见”与“工具侧加载证据”，处理正确。 |
| 3 #1977 “ampersands” | 页面 | 上游 issue 表述不精确且未附精确命令；读者起初按字面误读，读链接 issue 后纠正，最终正确。 |
| 4 CLAUDE.md 缺 docs-check | 目标仓缺口 | 这是本次要修的真实缺口，不是页面缺陷；按“只修具体缺口”补齐，必要。 |
| 5／6 依赖缺失、完整 jrnl 未跑 | 环境／任务约束 | 非页面缺信息，也非读者能力不足；任务禁止安装，读者保留待验正确。 |
| 7 环境条件未写进命令 | 读者（部分） | 页面明确要求写进实际命令；写范围允许在 CLAUDE.md 放 `npm install`＋后台 docs-run＋docs-check 的可复制片段，读者只写了散文前提。 |
| 8 无 superfences、渲染未验 | 目标仓配置 | 把 fence 放在 note 外是稳妥处理；无 mkdocs 无法验证渲染，属环境缺口。 |
| 9 限流与 `/tmp` 失败 | 读者（已恢复） | 临时路径选择导致一次 FileNotFoundError，已恢复；保留首次失败符合要求。 |
| 10 main/PR 规则与任务冲突 | 非缺陷 | 页面“代码与说明冲突”原则适用；读者按任务限制执行，无错。 |

### 三、读者没意识到的错误与缺口

1. **双引号整句示例会静默吞掉 `$` 和反引号。** 实测 `jrnl "I paid $5 for coffee"` 传给程序的是 `I paid  for coffee`，`"a `b c"` 变成 `a \b c`；单引号则原样。文档在“整句引用”只给双引号示例，正是 issue 要避免的 shell 解析问题；应改用单引号示例，或注明 `$`／反引号需转义。
2. **同页旧说明仍称保留字符可用 `\` 转义。** Composing Entries 的 note 与新增“`\@beach` 在 PowerShell 不生效”没有交叉引用，也没有把旧说明限定为 POSIX shell；PowerShell 用户先读到旧说明仍可能误用。
3. **CLAUDE.md 的 docs-check 前提可能不完整。** 只写 `npm install` 和已运行的 docs server，遗漏 CI 单独执行的 `npx puppeteer browsers install chrome`（`.github/workflows/docs.yaml`）；仅按新增说明可能仍缺 Chrome。这一点未安装验证，属待核风险。

### 四、结论

读者按页面完成了本次真实修改的核心验收：位置、内容、参数探针、链接与格式检查、待验项报告均成立；完整 jrnl 路径和文档构建因缺依赖保留为环境缺口，符合任务要求。按任务自己的验收判定为做成。主要遗留是新引入文档中双引号整句示例的 `$`／反引号副作用（可复现），其次是旧 note 的一致性与 CLAUDE.md 前提完整性。

---

# 第二轮返工记录（2026-11-03）

本轮按任务文件「修改要求」做定点返工；任务文件同时说明这不是首次实测，要求保留上一切记录和原提交，只追加修订结果。下面不覆盖、不改写第 1–8 节和上方「核对」的任何内容。

## 9. 做到哪一步与产物

三项修订都已完成，产物仍在工作树内：

- `docs/usage.md`
  - 整句 PowerShell 示例从双引号改为字面单引号，并补上「单引号内 apostrophe 双写」的示例。
  - 保留首轮已验证的单标签反引号／单引号／双引号三种写法。
  - Composing Entries 的旧反斜杠转义说明限定为 POSIX/Bash-like shell，并交叉引用 `#using-tags` 下的 PowerShell note。
- `CLAUDE.md`
  - `## Editing Documentation` 改为指向实际 CI 入口 `.github/workflows/docs.yaml`，列出 Python/Poetry 文档环境、Node/`pa11y-ci`、匹配的 Puppeteer Chrome 和已运行的 docs server 四个前提。
  - `npm install` 写成仅在 `node_modules` 缺失时安装，不再表述为每次检查必做。
- 本记录：追加本节到 `reader-tests/A-INSTRUCTION-FILES-READER-20261103-u1.md`。

按本会话约束没有提交、推送、切分支；工作树只改了 `docs/usage.md`、`CLAUDE.md` 和本记录。任务文件里的 result branch 推送和 review 状态由接收端处理。

## 10. 三项修订的具体内容与理由

### 10.1 `docs/usage.md` 的 PowerShell 整句写法

首轮整句示例只有 `jrnl "Had a wonderful day at the @beach with @Tom and @Anna."`。复测发现双引号里 `$` 会展开、反引号会被当转义符，整句可能在 jrnl 看到之前就丢字符。本轮改为：

```powershell
jrnl 'Had a wonderful day at the @beach with @Tom and @Anna.'
```

并补一个同时含 apostrophe、`$`、反引号、`@`、`#`、`&` 的合成示例：

```powershell
jrnl 'It''s a $5 day at the `spot` @cafe #1 & @Tom.'
```

说明文字明确：单引号内 apostrophe 要双写；双引号对单个标签仍然可用，不是一律错误，但整句写在双引号里会被 PowerShell 展开 `$` 和处理反引号。单标签的三种旧写法原样保留：

```powershell
jrnl `@beach
jrnl '@beach'
jrnl "@beach"
```

### 10.2 Composing Entries 旧 note

原句是「Although reserved characters can be escaped using `\`」，没有限定 shell 类型，和新增「`\@beach` 在 PowerShell 不生效」相矛盾。现改为：

- 明确 `\` 转义只适用于 POSIX/Bash-like shell；
- 明确 PowerShell 里 `\` 不转义，应改用引用；
- 交叉引用 `[Using Tags](#using-tags)` 下的 PowerShell note。

锚点 `using-tags` 由 `### Using Tags ###` 生成；本机无 MkDocs，未做真实渲染构建，只做了文件内锚点的静态核对（见 11.2）。

### 10.3 `CLAUDE.md` 的文档检查说明

改为按 CI 实际步骤列前提：

- CI 入口：`.github/workflows/docs.yaml` 的 accessibility job；
- Python/Poetry：已有 `poetry install`／`poetry sync --no-root` 环境，`mkdocs` 来自 dev 依赖，由 `poetry run poe docs-run` 提供预览；
- Node：`package.json` 的 devDependencies 含 `pa11y-ci`，`node_modules` 缺失时才需要 `npm install`；
- Chrome：CI 在 npm 安装后执行 `npx puppeteer browsers install chrome`，需要与该 Puppeteer 依赖匹配的 Chrome；
- docs server：`poetry run poe docs-run` 需已在 8000 端口运行，`tasks.py` 的 `DOCS_URL` 指向该端口。

并写明：不为了跑这个检查去安装或下载；前提缺失时只静态核 CI，报告「未验证」，不冒充通过。

## 11. PowerShell argv 复测（合成数据）

### 11.1 方法与环境

- 探针：只打印 `sys.argv[1:]` 的 Python 脚本，不读写任何 journal／config；用 `python <probe> <args>` 观察 PowerShell 实际传给子进程的 argv。
- 版本：Windows PowerShell 5.1.26100.9711；PowerShell 7.6.9；Python 3.13.5。
- 脚本文件只含 ASCII 合成文本，避免编码和 PowerShell 5.1 的 `.ps1` 读取差异。

### 11.2 结果

| 形式（probe 代表 jrnl） | PS 5.1 argv | PS 7.6.9 argv |
|---|---|---|
| `probe @beach` | `[]` | `[]` |
| ``probe `@beach`` | `["@beach"]` | `["@beach"]` |
| `probe '@beach'` | `["@beach"]` | `["@beach"]` |
| `probe "@beach"` | `["@beach"]` | `["@beach"]` |
| `probe \@beach` | `["\\@beach"]`（字面反斜杠＋@） | 同左 |
| `probe #beach` | `[]`（注释） | `[]` |
| `probe '#beach'` | `["#beach"]` | `["#beach"]` |
| `probe Had a wonderful day at the @beach with @Tom and @Anna.` | 三个 `@tag` 全部消失，只剩 `["Had","a","wonderful","day","at","the","with","and","."]` | 同左 |
| `probe 'Had a wonderful day at the @beach with @Tom and @Anna.'` | 完整原句 | 完整原句 |
| `probe 'It''s a $5 day at the `spot` @cafe #1 & @Tom.'` | `["It's a $5 day at the `spot` @cafe #1 & @Tom."]` | 同左 |
| `probe "I paid $5 for coffee at the @cafe."` | `["I paid  for coffee at the @cafe."]`（`$5` 变空） | 同左 |
| `probe "A `literal` backtick and @tag."` | `["A literal backtick and @tag."]`（反引号被吃掉） | 同左 |
| `probe "It's a great day at the @beach."` | 完整原句（双引号内 apostrophe 没问题） | 同左 |
| `probe I paid the bill & went home.` | 解析错误 `AmpersandNotAllowed`，整段脚本未执行 | 触发后台 job，`went` 被当作命令并报错 |
| `probe 'I paid the bill & went home.'` | 完整原句 | 完整原句 |

两条文档里的整句示例和三条单标签示例都按原样在 5.1／7.6.9 各跑了一次，argv 与预期字符一致。`$`、反引号、apostrophe 双写、`@`、`#`、`&` 的组合只在单引号下完整保留；双引号会改内容。这个结论对两个 PowerShell 版本一致。

### 11.3 检查与未运行项

| 检查 | 结果 |
|---|---|
| `git diff --check` | 退出 0 |
| `docs/usage.md` 相对链接／锚点 | 7 个相对链接，0 个缺文件／缺锚点；`using-tags` 锚点存在 |
| 代码围栏 | 44 个 fence 标记，成对 |
| `poetry` | 未找到 |
| `mkdocs` | 未找到（Python 环境也无 `mkdocs`、`ruamel.yaml`） |
| `jrnl` | 命令未安装；本地 `import jrnl.main` 因缺 `ruamel.yaml` 失败 |
| Node/npm | Node v22.23.2、npm 10.9.8 存在；`node_modules` 不存在 |
| MkDocs 构建 | 未运行 |
| `poe docs-check`／Pa11y | 未运行（缺 poetry、Node 依赖、Puppeteer Chrome、docs server） |
| 完整 jrnl 写入／标签读取 | 未运行（jrnl 不可启动），保留待验 |

没有安装、下载或运行 `npx`；没有接触真实 journal／配置。

## 12. 本轮卡点：页面哪一句、缺什么、做错过什么

| # | 页面／任务原句或位置 | 卡点与缺什么 | 我做了什么／做错了什么 |
|---|---|---|---|
| 1 | 第一步：`先看项目的 CI、包配置和已有指令，填入实际能用的入口` | 页面是通用方法，没有说 PowerShell 说明应放在 usage 的哪一段、写多长；需要自己从 issue 和文档结构判断。 | 按 issue「first mention of tags」放到 `### Using Tags ###` 第一个标签示例后；这是页面之外的推断，不是页面给出的定位。 |
| 2 | 第一步：`命令从当前项目复制并试跑` | `poetry`、`mkdocs`、`jrnl` 均不可用，无法试跑文档构建和完整 CLI；任务禁止安装。 | 只实际跑了 PowerShell argv 探针、链接／锚点静态检查、围栏检查和 `git diff --check`；其余标为未运行。 |
| 3 | 第一步：`完成需看到 [可观察结果]，并报告相关检查的实际结果` | 本轮的可观察结果只有 argv 和静态检查；MkDocs 渲染、Pa11y 可访问性没有环境。 | 没有把静态链接检查冒充 docs-check，也没有把 argv 探针冒充 jrnl 实跑。 |
| 4 | 第二步：`v2.1.280+ 用 /memory 查看...`、`用 /context 查看 Memory files` | 当前是子代理，没有 `/memory`、`/context` 入口。 | 页面自己也写了「API、SDK 或子代理若不提供这些入口，就不要硬套斜杠命令」，因此改用启动上下文里的项目指令＋手动读取作为「当前可见」证据，并保持「工具侧加载列表未取得」。 |
| 5 | 任务「按什么做」：`记录解析提交与内容指纹` | 任务文件只给 `docs/decisions/instruction-files.md@main`，没有解析提交 SHA。当前任务文件 28,341 bytes；我按标题 `# CLAUDE.md／AGENTS.md 怎么写` 到文件末重算附文为 10,269 字符 / 20,025 UTF-8 bytes、`sha256:c4e5a91d…`。这与首轮记录的 19,328 bytes／`7b8c59ff…`、以及任务文件第 41 行提到的 `21b5f4ab` 都不一致；附文里新增了指向首轮记录 `bfd477e` 的链接，页面内容应已在首轮后更新。 | 如实记下三个指纹不一致和「无法映射到具体上游 commit」，没有回填或改写首轮记录，也没有伪造 SHA。 |
| 6 | 「静态检查先拿本仓样本试」：`agents-md-lint` 两条命令 | 它不是 jrnl 的依赖，安装属于任务禁止的新软件。 | 跳过，改用项目自带的链接／锚点、围栏和 `git diff --check` 检查。 |
| 7 | `CLAUDE.md` 顶部：`ALWAYS prefer contributing to the main branch with a PR` | 与本会话「不提交、不推送、不切分支」的限制冲突。 | 按任务限制执行，只在工作树改文件；记录冲突，没有开 PR。 |
| 8 | 我自己的检查脚本（非页面） | 第一版锚点检查把 `_` 当成需要剔除的字符，误报既有链接 `#default_hour-and-default_minute` 缺锚点。 | 修正 slug 规则后重跑，确认该链接和新增的 `#using-tags` 都存在；没有因此改文档。 |

## 13. 页面之外还翻了什么

- 原 issue：GitHub `jrnl-org/jrnl#1977` 公开页面，确认标题「Add documentation for PowerShell users」、正文的 `escape ampersands`、`first mention of tags`，以及链接的 #1405／#1963／#1976；正文没有精确命令或错误文本。
- 目标仓现有指令与贡献规范：`CLAUDE.md`、`docs/contributing.md`。
- 目标仓文档与检查配置：`docs/usage.md`、`mkdocs.yml`、`.github/workflows/docs.yaml`、`pyproject.toml`（`docs-check`／`docs-run` 的 poe 定义、`mkdocs` dev 依赖）、`tasks.py`（`DOCS_URL`、sitemap、Pa11y 配置生成）、`package.json`、`package-lock.json`（Puppeteer 依赖）。
- 源码只读核对：`jrnl/main.py`、`jrnl/controller.py`，确认 `--version` 在加载 config 前执行；随后 `import jrnl.main` 因 `ruamel.yaml` 缺失失败，所以没有继续跑 jrnl。
- 本机 PowerShell 实测：5.1.26100.9711、7.6.9。
- 已存在于仓库中的首轮记录 `reader-tests/A-INSTRUCTION-FILES-READER-20261103-u1.md`（任务要求保留和追加的对象）。
- 没有读 a1dbv 的其他教程、旧读者答案或页面所属地图；没有访问模型网关、凭据或内网服务。

## 14. 恢复条件

- 文档构建：具备 Poetry 环境（`poetry install`／`poetry sync --no-root`）、Node 依赖、匹配的 Puppeteer Chrome 和已运行的 `poetry run poe docs-run` 后，再跑 `poetry run poe docs-check`；本次未安装，不能写成通过。
- 完整 jrnl：安装项目依赖后可启动 jrnl，再用临时配置和临时 journal 验证三种单标签形式和两条整句示例的写入／标签读取；不要接触真实用户配置。
- 页面版本：需要接收端提供 `docs/decisions/instruction-files.md@main` 的解析提交 SHA 或原始附文；本记录只能给出当前任务文件里附文的自算指纹。

## 核对（第二轮返工，2026-11-03）

核对人独立只读复核，另起 PowerShell argv 探针；未改读者产物，本节只追加结论。核对时只读查看了 a1dbv 参考副本的页面历史，未改页面。

### 一、事实核对

- 工作树与范围：`git status --porcelain` 只有 `CLAUDE.md`、`docs/usage.md`、`reader-tests/A-INSTRUCTION-FILES-READER-20261103-u1.md`；HEAD 仍是 `bfd477e`，没有新提交、推送或切分支；`node_modules` 不存在。改动统计：`CLAUDE.md` +15/−4，`docs/usage.md` +21/−8，读者本轮新增记录 +143/−0（本核对节为追加，未改前文）。
- 三项修订均落地：
  1. `docs/usage.md` 整句改为字面单引号 `jrnl 'Had a wonderful day at the @beach with @Tom and @Anna.'`；补 apostrophe 双写示例 ``jrnl 'It''s a $5 day at the `spot` @cafe #1 & @Tom.'``；保留反引号／单引号／双引号三种单标签形式；明确双引号对单标签仍可用、整句会丢 `$` 和反引号。
  2. Composing Entries 的旧 note 已限定 `\` 转义只适用于 POSIX/Bash-like shell，并交叉引用 `[Using Tags](#using-tags)`。
  3. `CLAUDE.md` 的 `## Editing Documentation` 指向 `.github/workflows/docs.yaml`，列出 Poetry 文档环境、`pa11y-ci`／`package.json`、Puppeteer Chrome、8000 端口 docs server 四项前提；`npm install` 仅在 `node_modules` 缺失时；写明缺前提只静态核 CI、报告未验证。
- PowerShell 独立复测（Windows PowerShell 5.1.26100.9711、PowerShell 7.6.9、Python 3.13.5；探针只打印 `sys.argv[1:]`）：读者第 11.2 节表格逐行复现一致。包括：裸 `@beach`／`#beach` 为 `[]`；`` `@beach ``、`'@beach'`、`"@beach"` 为 `["@beach"]`；`\@beach` 为 `["\\@beach"]`；裸整句三个 `@tag` 消失；单引号整句完整；单引号合成句完整；`"I paid $5 ..."` 变成 `I paid  for...`；双引号反引号被吃掉；裸 `&` 在 5.1 解析错误、在 7 触发后台 job，加引号完整。两条文档整句示例和三条单标签示例均按原样通过。
- 静态检查：`git diff --check` 退出 0；`docs/usage.md` 44 个行首 fence 标记成对；7 个相对链接／锚点均可解析（`using-tags`、`default_hour-and-default_minute`、`tagsymbols`、`editor`、`journals` 对应标题存在）。这些检查不能替代 MkDocs 渲染或 Pa11y。
- 环境：本机 `poetry`、`mkdocs`、`jrnl`、`ruamel.yaml` 均不可用，`node_modules` 不存在；MkDocs 构建、`poe docs-check`／Pa11y、完整 jrnl 写入／标签读取未运行，读者标为待验属实，未把未运行写成通过。
- 指纹：当前 `job.md` 28,341 bytes、`sha256:4ae714fd…`；附文（标题到文末）10,269 字符／20,025 UTF-8 bytes、`sha256:c4e5a91d…`，与 a1dbv 参考副本当前页面（提交 `684e5bcf`）完全一致，读者本轮自算正确。

### 二、新发现：`21b5f4ab` 是提交号，不是与首轮指纹冲突的第三个指纹

- a1dbv 参考副本历史：提交 `21b5f4ab` 的 `docs/decisions/instruction-files.md` 为 19,328 bytes／9,932 字符、`sha256:7b8c59ff…`，正是首轮附文和读者首轮记录的值；该版本不含 `bfd477e` 链接。
- 当前页面提交 `684e5bcf` 为 20,025 bytes／10,269 字符、`sha256:c4e5a91d…`，含 `bfd477e` 链接。
- 因此 `21b5f4ab`（提交）与 `7b8c59ff`（该提交的页面内容 SHA-256）互不矛盾，任务文件第 41 行“与负责人独立计算的 21b5f4ab 页指纹相符”指的就是同一页面版本。读者把它当成内容指纹去比较，得出“三个指纹不一致、无法映射到具体上游 commit”的结论不成立；这是读者没意识到的错误（missed）。任务文件把提交号写成“页指纹”确有歧义，属输入回执措辞问题（page），但提交与内容指纹本身可解析。

### 三、卡点逐条判定

| 任务消息顺序（读者表编号） | 判定 | 说明 |
|---|---|---|
| 1 记录解析提交与内容指纹（读者 #5） | page（输入措辞）／model（误读） | `job.md` 没有单独的“解析提交”字段，且把 `21b5f4ab` 写成“页指纹”，属输入回执缺口；但读者未认出 8 位缩写是提交号，误判三个值冲突，见 missed。 |
| 2 `/memory`、`/context` 入口（读者 #4） | page | 页面按交互式客户端写核对入口；虽已提示子代理不要硬套斜杠命令，但未给子代理可用的工具侧替代证据。读者按页面回退、保留启动加载待验，处理正确。 |
| 3 命令试跑与可观察结果：缺 poetry/mkdocs/Node/Puppeteer/docs server（读者 #2/#3） | 环境／禁装边界（非页面、非模型） | 任务禁止安装；页面要求报告实际结果，读者如实标为未运行。不能计为页面缺陷。 |
| 4 jrnl 不可运行、完整写入／标签读取未验（读者 #2、11.3） | 环境／任务条件（非页面、非模型） | 任务本身写“如已能运行 jrnl”；读者用 argv 探针并明确区分，标为待验正确。 |
| 5 PowerShell 说明放在 usage 哪一段（读者 #1） | 正常任务判断（非缺陷） | 页面是通用方法，未规定项目文案定位；读者按 issue“first mention of tags”放在首个标签示例后，判断合理。 |
| 6 CLAUDE.md 的 main+PR 与任务限制冲突（读者 #7） | 任务约束／指令优先级（非缺陷） | 页面“代码与说明冲突”原则适用；读者按任务限制只在工作树改文件，未开 PR，正确。 |
| 7 `agents-md-lint` 未运行（读者 #6） | 非缺陷 | 页面只说“可先试”，它不是 jrnl 依赖，安装越界；读者用项目自带检查替代，正确。 |
| 8 自己的锚点脚本首版误报（读者 #8） | model（已自纠） | 读者把下划线当剔除字符，修正 slug 规则后重跑；未影响文档，已记录。 |

### 四、结论

- 三项返工均已完成并经独立复测：单引号整句、apostrophe 双写、POSIX/PowerShell 交叉引用、`CLAUDE.md` 的 CI 入口与四项前提都成立；`git diff --check`、fence 配对、链接／锚点静态检查通过。
- 完整 MkDocs／Pa11y 与 jrnl 写入／标签读取未运行，属环境与禁装缺口；读者已明确标为待验，不能写成通过。
- 按任务自己的验收，读者真的做成了（taskDone=true）；首轮三项 open issue 已修，本轮返工通过，但不代表完整文档构建或完整 CLI 已验证。
- missed：读者把提交 `21b5f4ab` 当成内容指纹，误称三个指纹不一致、无法映射到上游提交；实际 `21b5f4ab` 的页面内容哈希正是首轮 `7b8c59ff`，当前页面是 `684e5bcf`／`c4e5a91d`。除此之外未发现新的产物错误。

---

# 第三轮定点修订记录（2026-11-03）

本轮按任务文件「修改要求」只做一处定点返工，不是新读者首次实测。不覆盖、不改写第 1–14 节和两轮「核对」；`docs/usage.md` 以及首轮、二轮已核通过的内容原样保留，未重跑 Windows／PowerShell 探针，未重读首次流程，也未再计算或改写指纹结论。工作树停在 `7572c11`，首轮 `bfd477e`、二轮 `7572c11` 的提交与 u1 全部原记录均保留。

## 15. 做到哪一步与产物

- 修改 `CLAUDE.md` 的 `## Editing Documentation` 最后两段：把「禁装」从永久规则改成按当前任务授权的条件分支，并去掉「仅 `node_modules` 缺失才可安装」的永久条件。这是本轮唯一的产品改动。
- 追加本节到 `reader-tests/A-INSTRUCTION-FILES-READER-20261103-u1.md`。
- 未改 `docs/usage.md`、未改其他文档页、未新建 `AGENTS.md`、未改生产代码／依赖／`tasks.py`／`mkdocs.yml`；未提交、未推送、未切分支、未安装或下载任何东西。

## 16. 修改前后

修改前（二轮提交的状态）：

- `(install with npm install only when node_modules is absent)`：把「目录存在」当成依赖完整、浏览器就绪的充分条件。
- `Do not install or download anything just to run this check.`：把本轮任务的 no-install 约束固化成项目永久规则，和同一段前文的正常 setup 前提冲突。

修改后：

- 仍保留 `.github/workflows/docs.yaml` 这一 CI 入口和四项准确前提：Python／Poetry 文档环境（`poetry install` 或 `poetry sync --no-root`，提供 `mkdocs`）、`package.json` 中的 Node 依赖且含 `pa11y-ci`、与该依赖匹配的 Puppeteer Chrome（CI 用 `npx puppeteer browsers install chrome`）、运行中的 `poetry run poe docs-run`。
- 新增：检查前这些依赖、匹配浏览器和 docs server 必须已具备，但不要求每次重装；删除了「仅在 `node_modules` 不存在时才 `npm install`」的表达，避免目录存在但依赖不全时误判。
- 新增条件分支：安装或下载是否允许以当前任务的授权为准；当前任务禁止时不执行 setup，缺前提就静态核对 CI 并把检查记为未验证；任务允许时按 CI job 的方式准备环境。

## 17. 实际检查与未运行项

| 检查 | 结果 |
|---|---|
| `git diff --check` | 退出 0 |
| `git status --porcelain` | 仅 `CLAUDE.md`、`reader-tests/A-INSTRUCTION-FILES-READER-20261103-u1.md` |
| `git diff --stat` | `CLAUDE.md` +7／−5；本记录为追加 |
| `docs/usage.md` 是否改动 | 未改动，仍为二轮已核版本 |
| MkDocs 构建 | 未运行（无 mkdocs 环境，本轮禁装） |
| `poetry run poe docs-check`／Pa11y | 未运行（缺 poetry、Node 依赖、Puppeteer Chrome、docs server） |
| 完整 jrnl 写入／标签读取 | 未运行（jrnl 不可启动，依赖缺失） |
| PowerShell argv 探针 | 按任务要求未重跑 |

文档构建、可访问性检查和完整 CLI 仍按未运行处理，不写成通过；云端已验范围也没有拿来冒充本机 Windows 宿主或完整门禁。

## 18. 本轮卡点：页面哪一句、缺什么、做错过什么

| # | 页面／任务原句或位置 | 卡点与缺什么 | 我做了什么／做错了什么 |
|---|---|---|---|
| 1 | 任务「修改要求」：`CLAUDE.md 的“Do not install or download anything just to run this check” ... 改成条件分支` | 只给了改动方向和两个分支语义，没有给可直接替换的完整措辞；页面也没有「如何在项目指令里表达安装授权」的模板。 | 按修改要求自行组织措辞，保留原四项前提，只替换授权与重装相关的句子。这是任务之外的写作判断。 |
| 2 | 任务「修改要求」：`不要把“仅 node_modules 不存在才可安装”固化为永久条件` | 页面通用方法没有讨论依赖目录存在但内容不完整的情况，只能按任务要求补。 | 拟定措辞时先沿用「缺 Node 依赖才 `npm install`」的句式，发现这仍把安装动作留成项目规则，改为「检查前依赖须已具备、不要求每次重装、是否安装看当前任务授权」。这一调整只发生在措辞设计阶段，没有写入错误版本。 |
| 3 | 页面第一步：`命令从当前项目复制并试跑`、`完成需看到 [可观察结果]` | 本机仍无 poetry、mkdocs、Node 依赖、Puppeteer Chrome、docs server 和可启动的 jrnl；本轮又明确禁装。 | 只做了 diff、状态和范围核对；没有试跑文档构建或 Pa11y，如实标为未运行。 |
| 4 | 页面第二步：`v2.1.280+ 用 /memory ...`、`用 /context 查看 Memory files` | 当前仍是子代理，没有这些工具侧入口（与首轮、二轮相同，未新增缺口）。 | 沿用既有记录，不再重复取证，也不把复述当加载证据。 |
| 5 | `CLAUDE.md` 顶部：`ALWAYS prefer contributing to the main branch with a PR` | 与本轮「不提交、不推送、不切分支」限制冲突。 | 按任务限制只在工作树改文件，未做任何 git 写操作。 |
| 6 | 任务「按什么做」：`记录解析提交与内容指纹` | 本轮修改要求明确不重读首次流程、不因指纹误读再造输入；任务文件仍只有 `@main`，没有独立解析提交字段。 | 保留前两轮记录原文与负责人已给的更正结论，不重算、不回填，也不把提交号当内容指纹。 |

## 19. 页面之外还翻了什么

- 目标仓 CI 与检查配置：`.github/workflows/docs.yaml`（accessibility job 的实际步骤：`poetry sync --no-root`、`npm install`、`npx puppeteer browsers install chrome`、后台 `poe docs-run`、`poe docs-check`）。
- 包与任务配置：`package.json`（devDependencies `pa11y-ci` 4.0.0）、`pyproject.toml`（`mkdocs >=1.4`、`docs-check` 的 sequence、`docs-run` 为 `mkdocs serve`）、`tasks.py`（`DOCS_URL` 为 8000 端口、sitemap 与 Pa11y 配置生成）。
- 工作树状态：`git log`、`git status`、`git diff`，用于确认基于 `7572c11`、单写者、范围仅两个文件。
- 未读 a1dbv 的其他教程、旧读者答案或页面所属地图；未访问模型网关、凭据或内网服务。

## 20. 恢复条件

- 文档检查：在允许安装且具备 Poetry 文档环境、`package.json` 的 Node 依赖、匹配的 Puppeteer Chrome 与运行中的 `poetry run poe docs-run` 后，运行 `poetry run poe docs-check`；本轮未安装，不能记为通过。
- 完整 jrnl：安装项目依赖后，用临时配置与临时 journal 验证文档中的单标签和整句写法；不要接触真实用户配置。
- 页面版本：仍需接收端提供 `docs/decisions/instruction-files.md@main` 的独立解析提交回执；本轮按要求未重算指纹。

## 核对（第三轮定点修订，2026-11-03）

核对人独立只读复核；本节只追加，未改读者第 1–20 节与前两轮核对。核对只运行 git 只读命令并读取项目内的 CI／配置，未改读者产物。

### 一、事实核对

- 基线：HEAD `7572c118` 与任务 `base_ref` 相同，`7572c118..HEAD` 无提交；分支 `receiver/A-INSTRUCTION-FILES-READER-20261103` 与其上游 `origin/relay/a-instruction-files-reader-20261103` 都指向 `7572c118`，没有新提交、推送或切分支。
- 改动范围：`git status --porcelain --untracked-files=all` 只有 `CLAUDE.md` 与 `reader-tests/A-INSTRUCTION-FILES-READER-20261103-u1.md`；`git diff -- docs/usage.md` 为空，工作树仍是 `7572c11` 已提交的二轮版本（单引号整句、`It''s` 双写、三种单标签写法、POSIX 限定与 `#using-tags` 互链均未变）。没有新建 `AGENTS.md`，未改 `tasks.py`、`mkdocs.yml`、生产代码或依赖；无 `node_modules`、`.venv`、`sitemap.xml`、`config.json`。
- `CLAUDE.md`：`git diff --numstat` 为 +10／−7，单一 hunk。删除的是 `(install with npm install only when node_modules is absent)` 与 `Do not install or download anything just to run this check...` 两句；新增的是「依赖、匹配浏览器和 docs server 检查前须已具备、不要求每次重装」，以及按当前任务授权分支：禁止安装／下载时不执行 setup、缺前提只静态核 CI 并记未验证，允许时按 CI job 方式准备环境。`.github/workflows/docs.yaml`、Python/Poetry、Node／`pa11y-ci`、Puppeteer Chrome、运行中的 docs server 四项前提都保留。
- 项目配置复核：`docs.yaml` 的 accessibility job 依次执行 `poetry sync --no-root`、`npm install`、`npx puppeteer browsers install chrome`、后台 `poetry run poe docs-run`、`poetry run poe docs-check`；`package.json` 的 devDependencies 含 `pa11y-ci` 4.0.0；`pyproject.toml` 的 dev 依赖含 `mkdocs >=1.4`，`docs-check` 最终调用 `npx pa11y-ci`；`tasks.py` 的 `DOCS_URL` 指向 8000 端口。`CLAUDE.md` 的 CI 入口与四项前提和项目一致。
- 记录：读者本轮追加为 +64／−0，`git diff -U0` 当时显示新内容从原第 402 行起纯追加 64 行、无删除；本核对节再加 37 行，合并后 `git diff --numstat` 为 +101／−0。第 1–14 节和两轮核对原文未变。
- 检查：`git diff --check` 退出 0。
- 环境：`poetry`、`mkdocs`、`jrnl` 不在 PATH，`ruamel.yaml` 缺失，无 `.venv`；Node v22.23.2／npm 10.9.8 存在但无 `node_modules`。MkDocs 构建、`poe docs-check`／Pa11y、完整 jrnl 写入／标签读取未运行，读者标为待验属实，没有把未运行写成通过。工作树内没有安装或下载留下的产物，也未发现运行 `npx` 的痕迹。

### 二、读者第三轮卡点逐条判定

| 读者 # | 判定 | 说明 |
|---|---|---|
| 1 缺可直接替换的措辞／页面无安装授权模板 | page（轻） | 输入只给方向与两分支语义，未给完整措辞；页面也没有模板。读者自行组织的措辞与要求一致，未造成产物错误。 |
| 2 `node_modules` 条件的措辞 | model（草稿自纠） | 读者先沿用「缺 Node 依赖才 `npm install`」的句式，随后自行改为「依赖须已具备、不要求每次重装、是否安装看任务授权」，未写入错误版本。 |
| 3 缺 poetry／mkdocs／Node 依赖／Puppeteer Chrome／docs server | 环境与禁装边界 | 不是页面缺信息，也不是读者能力问题；任务允许保留环境缺口，读者如实标为未运行。 |
| 4 子代理无 `/memory`、`/context` | page | 页面按交互式客户端写核对入口，虽已提示子代理不要硬套斜杠命令，但未给可用的工具侧替代证据；读者沿用前两轮回退方式，处理正确。 |
| 5 `CLAUDE.md` 的 main+PR 偏好与不提交／不推送／不切分支冲突 | 任务约束／指令优先级 | 不是页面或读者缺陷；读者按任务限制只在工作树改文件，正确。 |
| 6 任务无独立解析提交字段 | page（输入回执） | `job.md` 仍只有 `page: ...@main`，没有独立解析提交 SHA；本轮按要求不重算、不回填，保留负责人更正结论，未造新错。 |

### 三、读者没意识到的错误

1. 第 17 节把 `git diff --stat` 的结果记成 `CLAUDE.md` +7／−5；实际 `git diff --numstat` 为 +10／−7（`git diff --stat` 显示 17 处变更，10 insertions／7 deletions），即前提段落改写新增 3 行、授权分支新增 7 行，共删除 4 + 3 行。这是自报检查结果与最终工作树不一致，不影响文档产物，但应在记录中更正。

除这一处外，未发现本轮新增的产物错误；上一轮把页面提交 `21b5f4ab` 当成内容指纹的 missed 已由负责人更正，读者本轮按要求保留原文、未再重算，不重复计入。

### 四、结论

- 本轮两项修改要求均已落地且经独立核对：永久禁装句改为按当前任务授权的条件分支；「仅 `node_modules` 缺失才安装」的固化条件删除；四项准确前提与 CI 入口保留；`docs/usage.md` 未动，范围与 no-install 限制遵守。
- MkDocs 构建、Pa11y 与完整 jrnl 写入／标签读取仍因环境缺依赖未运行，不能写成通过；这属环境与禁装边界，不是本轮修订失败。
- 按本轮任务自己的验收，读者做成了这次定点修订（taskDone=true，仅指修订本身；不代表完整文档／CLI 验收）。
