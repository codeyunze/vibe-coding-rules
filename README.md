# vibe-coding-rules

本仓库是 yz-mall 的 Cursor 项目规则、技能和 Harness。它不是业务代码仓库。

克隆之后，必须把本仓库放在工作区根目录下，并且目录名是 `.cursor`。Cursor 只从「当前打开的工作区根」读取 `.cursor/rules`、`.cursor/skills`。把本仓库自己当成工作区打开，规则和技能不会生效。

## 目标目录

```text
<workspace>/                         # 用 Cursor 打开这一层
├── .cursor/                         # 本仓库（含 .git）
│   ├── rules/
│   ├── skills/
│   └── harness/
├── yz-mall/                         # https://github.com/yunze-gh/yz-mall.git
├── yz-mall-web-admin-pc/            # https://github.com/codeyunze/yz-mall-web-admin-pc.git
└── mall-demo/                       # 可选，https://github.com/codeyunze/mall-demo.git
```

`<workspace>` 的文件夹名可以自定（例如 `mall`）。`.cursor` 这个名字不能改，也不能多套一层目录。

## 配置步骤

按顺序做。每一步先检查，已经满足就跳过，不要重复克隆或覆盖。

1. 确定本仓库根目录：该目录内同时有 `.git`、`rules/`、`skills/`、`harness/`。下面把这个目录叫「本仓库根」。
2. 确定工作区根：
   - 若本仓库根的上一级里已经有 `yz-mall`（能看到 `yz-mall/pom.xml`），工作区根就是这一级。
   - 若没有，在本仓库根的上一级新建工作区目录，或使用用户指定的目录。不要把工作区根设成 `yz-mall` 或 `yz-mall-web-admin-pc` 里面。
3. 把本仓库根变成 `<workspace>/.cursor`：
   - 已经是这个路径：不要移动。
   - 不是：把整个目录（连同 `.git`）移到 `<workspace>/.cursor`。
   - 目标路径已存在、且不是这次克隆：停下来问用户，禁止覆盖。
4. 补齐同级业务仓库。目录已存在就不要再克隆。
   - `git clone https://github.com/yunze-gh/yz-mall.git`
   - `git clone https://github.com/codeyunze/yz-mall-web-admin-pc.git`
   - `mall-demo` 只在用户明确要演示工程时再克隆：`git clone https://github.com/codeyunze/mall-demo.git`
5. 不要把 `rules/`、`skills/` 复制到用户主目录，也不要写进 Cursor 的 User Rules。项目规则和技能放在 `.cursor` 里就会随工作区加载。`skills/install-*` 是可选的第三方技能安装器，只有用户明确要求安装时才执行。
6. 不要提交、不要 `git push`，除非用户这次明确要求。
7. 告诉用户：用 Cursor 打开 `<workspace>` 这一层（不是只打开 `yz-mall`），然后新开一个 Agent 对话。当前对话如果是在错误的根目录里开始的，规则要到新对话里才会加载。

## 自检

以下路径都相对于 `<workspace>`，必须存在：

- `.cursor/rules/imported/vibe-coding-rules/rules/yz-mall-overview.mdc`
- `.cursor/skills/yz-mall-feature-pipeline/SKILL.md`
- `.cursor/skills/design-mysql-table/SKILL.md`
- `.cursor/harness/README.md`
- `.cursor/harness/PIPELINE.md`
- `yz-mall/pom.xml`
- `yz-mall-web-admin-pc/package.json`

再确认：

- `git -C <workspace>/.cursor remote get-url origin` 为 `https://github.com/codeyunze/vibe-coding-rules.git`
- 本仓库工作区干净，或只有用户自己的未提交改动

新对话里应已带上项目总览、改码纪律等 `alwaysApply` 规则。用户说「建表」时使用 `design-mysql-table`；说「走功能管道 / 开 feature harness」时先读 `.cursor/skills/yz-mall-feature-pipeline/SKILL.md`，再按 `.cursor/harness/PIPELINE.md` 把需求卡、任务清单、验收清单写到 `.cursor/harness/runs/`。

## 以后更新

在 `<workspace>/.cursor` 里执行 `git pull`。不要把规则或 Harness 再复制进 `yz-mall` 或前端仓库。
