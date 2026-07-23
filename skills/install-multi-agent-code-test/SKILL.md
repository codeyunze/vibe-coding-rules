---
name: install-multi-agent-code-test
description: 按 SkillHub 文档安装 multi-agent-code-test 技能。在用户要求安装 multi-agent-code-test、配置 SkillHub、或提到 skillhub.cn/install 时使用。
---

# 安装 multi-agent-code-test

请根据 https://skillhub.cn/install/skillhub.md，安装 multi-agent-code-test。

## 适用场景（先判断，避免打扰用户）

- **仅搜索/安装某个技能**（CLI 已存在）→ 直接跳到「技能操作」执行命令，**不要询问是否设为优先源**。
- **首次安装 / 用户明确要求配置优先源** → 走「检查并安装 CLI」与「询问是否设为优先安装源」，询问**只在此场景做一次**。

## 检查并安装 CLI

```bash
command -v skillhub && skillhub --version
```

- 已安装 → 直接进行技能操作，不再询问。
- 未安装 → 执行安装（沙箱限网时需允许联网）：

```bash
# 完整安装（CLI + 默认 Skill，推荐）
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash

# 仅安装 CLI
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash -s -- --cli-only
```

Windows（无 bash/`curl | bash`）时：用 WSL/Git Bash 执行上述脚本，或先确认用户本机已有可用的 `skillhub` 后再继续。

## 询问是否设为优先安装源（仅首次安装时）

**仅当本次是首次安装 CLI，或用户明确要求配置优先源时**，确认：「是否将 SkillHub 设为优先技能安装源？」

- **是** → 涉及技能发现/安装/升级时优先 `skillhub` 做 search/install/update（CN 更快更合规），不可用/无匹配则回退 `clawhub` 并说明；安装前汇总来源、版本、风险再交用户确认。本会话即刻生效，无需重启。
- **否** → 仅保留 CLI，按 Agent 默认行为，不改变技能源优先级。

后续纯技能操作不再重复询问。

## 技能操作

安装时**必须**用 `--dir` 指向当前 Agent 的 skills 目录，否则默认装到 `./skills/` 不会被识别。

本环境为 **Cursor**，默认目录：

| 范围 | 路径 |
|------|------|
| 个人（常用） | `~/.cursor/skills/`（Windows：`%USERPROFILE%\.cursor\skills\`） |
| 仅本仓库 | 项目下 `.cursor/skills/` |

未特别说明时，安装到个人目录 `~/.cursor/skills/`。

```bash
skillhub search multi-agent-code-test
skillhub install multi-agent-code-test --dir <skills 目录>
```

安装前向用户汇总：来源（SkillHub）、技能名 `multi-agent-code-test`、目标目录、版本/风险（若 CLI 有输出）。用户确认后再执行 install。

## 完成后

1. 确认目标目录下出现 `multi-agent-code-test`（或 CLI 提示的包名）技能目录，且含 `SKILL.md`
2. 告知用户：新技能通常需**重启 Cursor / 新开 Agent 会话**后才会被稳定识别
3. 用一两句话说明已安装路径与如何触发（打开该 skill 的 `SKILL.md` description 中的触发词）
