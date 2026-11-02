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
