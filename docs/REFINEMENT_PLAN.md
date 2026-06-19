# DevGuard 精炼规划执行方案与验收标准

| 字段 | 值 |
|---|---|
| 文档版本 | v1.0 |
| 创建日期 | 2026-06-19 |
| 适用范围 | devguard/ 技能包本体（不含具体业务项目规则） |
| 前置批次 | Batch 1-6（控制面、分层加载、摘要披露已实现） |
| 关联文档 | references/batch-roadmap.md、references/forward-testing.md、skillopt/benchmark.jsonl |

---

## 1. 背景与动机

DevGuard 已完成 Batch 1-6，具备完整的路由、门禁、分层加载与摘要优先披露能力。当前主要问题不是「缺规则」，而是：

1. **入口重复**：SKILL.md、README.md、rule-disclosure-index.md 多处重复「何时读什么」
2. **默认 token 偏高**：agent 容易误读 full template、误输出中间态 summary
3. **路由歧义**：risk tags 过多、FAST/STANDARD 可跳过门禁分散在多处
4. **路径歧义**：shared/ 与 references/ 存在同名或重叠文件
5. **完成态过重**：Completion / Review 完整模板日常使用率低
6. **回归不足**：skillopt/ 已有雏形，尚未成为正式质量门禁

本规划目标：在**不削弱硬门禁**的前提下，系统性降低默认成本、提高路由一致性、降低维护复杂度。

---

## 2. 精炼目标

### 2.1 量化目标

| 指标 | 当前基线（估算） | 目标 |
|---|---|---|
| SKILL.md 行数 | ~180 行 | <= 80 行 |
| references/ 总体积 | ~129 KB / 36 文件 | <= 100 KB（去重后） |
| 普通任务默认外显字符数 | 不定，常 > 12k | <= 12k（95% 场景） |
| 普通任务默认 outward 块数 | 不定，常 4-8 块 | 固定 2 块（ES + TCS） |
| forward test 通过率 | 未正式门禁 | 100%（benchmark + held-out） |
| 重复 canonical 路径 | >= 4 组 | 0 组 |
| wrapper skill 平均行数 | ~20 行 | <= 30 行（保持薄） |

### 2.2 定性目标

- 执行严谨度不变：Task Contract、Impact Analysis、Evidence、TDD 硬门禁保留
- 披露与执行分离更清晰：默认 summary，异常 focused expansion，audit 才 full
- agent 决策成本下降：少选题、多查表、少拼装
- 维护者改一处、全链路一致：single canonical path

### 2.3 非目标（明确不做）

- 不新增 domain core（UI、Bug Fix、Migration 等执行语义不改）
- 不把全部 reference 合并成单文件
- 不默认跳过 CodeGraph / Official Docs Check（仅明确 FAST 降级条件）
- 不把项目专属规则写入 DevGuard 通用层
- 不在本规划内实现新的 MCP 或外部工具集成

---

## 3. 精炼原则

1. **先路由，再加载；先理解，再分析；先冻结，再执行** — 核心原则不动
2. **减重复，不减门禁** — 删 prose 重复，不删 BLOCKED 条件
3. **最小切片交付** — 每 Phase 可独立合并、可独立回归
4. **脚本优先于自由 prose** — 标准 outward 块优先用 generate_rule_loading_manifest.py
5. **改披露先跑 forward test** — 任何披露/路由改动必须过回归集
6. **Canonical 唯一** — 每个概念只有一个 authoritative 文件路径

---

## 4. 工作包总览

共 **7 个 Phase、22 个工作包（WP）**。

| Phase | 主题 | 工作包 | 风险 | 预估工作量 |
|---|---|---|---|---|
| P0 | 基线与回归护栏 | WP-00, WP-20 | 低 | 0.5-1 天 |
| P1 | 入口与目录去重 | WP-01, WP-02, WP-11 | 低 | 1-2 天 |
| P2 | 模板三档化 | WP-09, WP-19 | 中 | 2-3 天 |
| P3 | 路由与门禁矩阵 | WP-03, WP-04, WP-10, WP-13, WP-14, WP-15 | 中 | 2-4 天 |
| P4 | 调用面与生态边界 | WP-12, WP-16, WP-22 | 低 | 1 天 |
| P5 | 降级与分层查文档 | WP-17, WP-18 | 中 | 1-2 天 |
| P6 | 词汇表与收尾 | WP-21, WP-00 终验 | 低 | 0.5-1 天 |

### 工作包索引

| ID | 名称 | Phase |
|---|---|---|
| WP-00 | 基线度量与回归集扩展 | P0 / P6 |
| WP-01 | 瘦身 SKILL.md | P1 |
| WP-02 | 精简 README.md | P1 |
| WP-03 | 简化 risk tags taxonomy | P3 |
| WP-04 | Gate Matrix（阶段可跳过表） | P3 |
| WP-09 | 模板三档化（report-templates） | P2 |
| WP-10 | 阻断清单分层（P0/P1/P2） | P3 |
| WP-11 | shared/ 与 references/ 去重 | P1 |
| WP-12 | 缩短 default_prompt 与 example prompts | P4 |
| WP-13 | 预置命名技能链 | P3 |
| WP-14 | Dynamic Reroute 触发器表 | P3 |
| WP-15 | Unified reference 三段结构 | P3 |
| WP-16 | 外部技能共存规则 | P4 |
| WP-17 | CodeGraph 无 index 降级路径 | P5 |
| WP-18 | Official Docs Check 分层（L1/L2/L3） | P5 |
| WP-19 | Completion Summary 轻量化 | P2 |
| WP-20 | skillopt 正式化 | P0 |
| WP-21 | 核心术语词汇表 | P6 |
| WP-22 | description / discoverability | P4 |


---

## 5. 分 Phase 执行方案

### Phase 0：基线与回归护栏（WP-00, WP-20）

**目的**：建立可度量基线，确保后续精炼有回归网。

#### WP-00 基线度量

**执行步骤**：

1. 记录 SKILL.md、README.md、report-templates.md 行数与体积
2. 记录 references/ 文件数、总体积、wrapper 行数
3. 审计 shared/ 与 references/ 重复文件，写入 docs/REFINEMENT_BASELINE.md
4. 记录 benchmark 条目数与通过率

**交付物**：docs/REFINEMENT_BASELINE.md、重复路径对照表

#### WP-20 skillopt 正式化

**执行步骤**：

1. 扩展 skillopt/benchmark.jsonl 至 12-15 条（见附录 A）
2. README 增加「运行 skillopt 回归」章节
3. 可选：check_devguard_bundle.py 增加 benchmark 存在性检查
4. 文档化回归命令约定

**Phase 0 验收标准**：

- [ ] 基线文档存在且指标可复测
- [ ] benchmark >= 12 条，覆盖 12 类场景
- [ ] fresh agent benchmark 通过率 = 100%
- [ ] README 有明确回归步骤

---

### Phase 1：入口与目录去重（WP-01, WP-02, WP-11）

#### WP-01 瘦身 SKILL.md

1. 保留：Core Responsibilities、Default Workflow、Internal Skill Modules、Operating Rules（<= 15 条）、Helper Scripts
2. 删除「What To Read And When」长清单
3. 替换为 index 链接：rule-disclosure-index.md、report-templates.md
4. 目标：<= 80 行

#### WP-02 精简 README.md

1. 保留：Core Principle、mermaid、Quick Start、Internal Modules 表
2. Output Policy 改为 5 行摘要 + 链接

#### WP-11 shared/references 去重

1. 确定 canonical 一律为 references/
2. shared/ 改 stub redirect 或删除；全局更新引用
3. 运行 check_devguard_bundle.py

**Phase 1 验收标准**：

- [ ] SKILL.md <= 80 行
- [ ] 零 canonical 路径冲突
- [ ] check_devguard_bundle.py 通过
- [ ] benchmark 通过率 = 100%

---

### Phase 2：模板三档化（WP-09, WP-19）

#### WP-09 模板三档化

| Tier | 名称 | 对外块组合 | 触发条件 |
|---|---|---|---|
| T1 | summary | ES + TCS | 默认 |
| T2 | focused-expansion | ES + Risk/Exception + TCS | 高风险/异常 |
| T3 | detailed | 完整 Routing/Manifest/IA/TC | audit/verbose |

1. 标记 internal-only：Routing Summary、Rule-Loading Summary、Project Understanding Summary、Impact Analysis Summary
2. Task Contract Summary 压缩为 4 字段：Goal / Scope / Tests / Acceptance
3. 更新 generate_rule_loading_manifest.py 与 forward-testing.md

#### WP-19 Completion Summary 轻量化

1. 新增默认 Completion Summary（Changed / Verified / Acceptance / Unverified）
2. 完整 Completion/Review Report 标记 T3 only

**Phase 2 验收标准**：

- [ ] T1/T2/T3 三档说明存在
- [ ] 普通任务 outward = ES + TCS
- [ ] manifest 脚本输出对齐 T1
- [ ] forward test 场景 1-4 全部通过

---

### Phase 3：路由与门禁矩阵（WP-03, WP-04, WP-10, WP-13, WP-14, WP-15）

#### WP-03 简化 risk tags

Primary（12）：api_contract, auth_permission, data_consistency, migration, release, security, performance, official_docs_required, codegraph_required, compatibility, ai_output, ux_flow

其余降为 Secondary，不参与 mode 决策。

#### WP-04 Gate Matrix

| Gate | S0 | S1/FAST | S2/STANDARD | S3+/STRICT |
|---|---|---|---|---|
| Project Understanding | 否 | 轻量/条件 | 是 | 深 |
| Official Docs Check | 否 | 条件 | 条件 | 是 |
| Impact Analysis | 否 | 轻量 | 是 | 深 |
| Task Contract | 否 | 简版 | 是 | 严格 |
| TDD Red | 否 | repro 可替代 | 是 | 是 |

#### WP-10 阻断清单分层

- **P0（8 条硬阻断）**：无 output、跳过 gate、无 Contract 编码、编造结果、无 evidence、TDD 无 failing、invented artifacts、两次失败无新 evidence
- **P1**：domain 懒加载（UI 路径、migration rollback、AI cost cap 等）
- **P2**：警告（budget overrun、mock 质量、性能 deferred）

P0 -> BLOCKED + Exception Note；P2 -> ALLOW_WITH_WARNINGS + Risk Note

#### WP-13 预置命名技能链（8 条）

route:feature-normal / ui-implementation / bugfix-standard / bugfix-desktop-ui / refactor-migration / performance-change / ai-llm-feature / review-only

#### WP-14 Dynamic Reroute 触发器表

| 触发器 | 动作 |
|---|---|
| phase -> review/release | 补 load review/release |
| 新 contract 面暴露 | rerun IA + amend contract |
| 同一问题第 2 次失败 | failure-retrospective -> reroute |
| 用户改 outcome | rebuild Task Profile + contract |
| blocker 出现 | Exception Note + BLOCKED |

Reroute outward 仅更新 ES：Mode / Rules / Status / Next

#### WP-15 Unified reference 三段结构

Metadata / Summary / Full Rule。优先：impact-analysis-core、bug-fix-core、daily-development-core、code-review-core

**Phase 3 验收标准**：

- [x] Primary risk tags = 12
- [x] Gate Matrix 存在
- [x] Blocking 分 P0/P1/P2
- [x] Named Routes >= 8
- [x] 4 个 core 完成三段结构
- [x] FAST 不 over-gate；STRICT 仍正确阻断


---

### Phase 4：调用面与生态边界（WP-12, WP-16, WP-22）

#### WP-12 缩短 prompts

1. agents/openai.yaml default_prompt <= 120 字
2. example-prompts.md 每场景 1 行
3. 新增短触发词：/devguard fast | strict | review

#### WP-16 外部技能共存规则（SKILL.md，<= 5 条）

1. DevGuard 管：路由、门禁、Contract、规则加载
2. Domain skill 管：具体执行手法
3. 冲突时：DevGuard 门禁优先
4. 不重复 domain skill 的 TDD/debug 细节
5. 用户显式指定 domain skill 时，DevGuard 仅做路由与 Contract

#### WP-22 description 优化

SKILL frontmatter description <= 120 字，含 When to use / When NOT to use

**Phase 4 验收标准**：

- [x] default_prompt <= 120 字
- [x] example-prompts 每场景 1 行 + 短触发词
- [x] Coexistence Rules <= 5 条
- [x] description <= 120 字且含 When to use / When NOT to use
- [ ] benchmark 100%（fresh-agent run pending）

---

### Phase 5：降级与分层查文档（WP-17, WP-18）

#### WP-17 CodeGraph 无 index 降级

1. codegraph_status 不可用 -> codegraph_unavailable
2. S1：limited read（入口文件 + 有限 grep）
3. S2+：init 或 ALLOW_WITHOUT_CODEGRAPH
4. outward 一行：Structural tool: CodeGraph unavailable, fallback: limited read

#### WP-18 Official Docs 分层

- L1：Context7 summary，够用于 IA
- L2：原文核验（S3+ / deprecated / permission / installer）
- L3：人工确认（STRICT + release）
- Task Contract 仅保留一条 official constraint

**Phase 5 验收标准**：

- [x] No-Index Fallback 文档化（codegraph_unavailable / limited read / ALLOW_WITHOUT_CODEGRAPH）
- [x] Official Docs L1/L2/L3 分层 + TCS 单行 official constraint
- [x] Execution Summary `Structural tool` 字段
- [ ] stale/platform benchmark 100%（fresh-agent run pending）

---

### Phase 6：词汇表与终验（WP-21, WP-00）

#### WP-21 词汇表

创建 references/glossary.md（>= 15 术语）。建议：Task Profile, Task Contract, Impact Analysis, Execution Summary, Risk Note, Exception Note, FAST/STANDARD/STRICT, metadata/summary/full, ALLOW/ALLOW_WITH_WARNINGS/BLOCKED, Named Route, Gate Matrix, Completion Summary, Coexistence Rules, No-Index Fallback, Official Docs L1/L2/L3

#### WP-00 终验

1. 复测 2.1 量化指标
2. benchmark + held-out 全跑
3. check_devguard_bundle.py
4. forward-testing Regression Example Set 人工 spot-check
5. 更新 REFINEMENT_BASELINE.md 为 before/after
6. CHANGELOG 精炼条目

**Phase 6 验收标准**：

- [x] glossary.md >= 15 术语
- [x] REFINEMENT_BASELINE.md before/after 更新
- [x] CHANGELOG v0.2.0 条目
- [x] bundle + skillopt schema 全通过
- [ ] fresh-agent benchmark 100%（CI/manual pending）

---

## 6. 依赖关系

`
P0 -> P1, P2（可并行）-> P3 -> P4, P5（可并行）-> P6
`

每 Phase 合并前必须跑 benchmark。

---

## 7. 总体验收标准

### 7.1 硬门禁 G1-G8（必须全部满足，否则不予发布）

| # | 验收项 | 验证方法 |
|---|---|---|
| G1 | 无 rule-loading output 不得开始执行 | forward test |
| G2 | 需 project understanding 的任务不得跳过进入 IA/编码 | benchmark refactor |
| G3 | platform-sensitive 任务须 official docs check 后再 IA | platform 场景 |
| G4 | 无 Task Contract 不得编码/修复/重构 | implementation 场景 |
| G5 | 无 failing test/repro 不得宣称 TDD 完成 | bugfix 场景 |
| G6 | 同一问题两次失败须进入 failure-retrospective | reroute 场景 |
| G7 | UI 任务须 real user operation path 验证 | UI 场景 |
| G8 | CodeGraph stale 时不得 silent trust | stale-index 场景 |

### 7.2 披露标准 D1-D7

| # | 验收项 | 验证方法 |
|---|---|---|
| D1 | 普通任务 outward = ES + TCS（仅） | 场景 1 + max_chars |
| D2 | 高风险无异常 = ES + Risk Note + TCS | 场景 2 |
| D3 | 异常 = ES + Exception Note（+ TCS 若可形成） | 场景 3 |
| D4 | 默认不得输出 internal-only 块 | must-not 列表 |
| D5 | 普通任务 outward <= 12k chars | benchmark |
| D6 | Record block 格式正确 | spot-check |
| D7 | T3 detailed 仅 audit/verbose 显式触发 | 普通场景 |

### 7.3 结构标准 S1-S7

| # | 验收项 | 验证方法 |
|---|---|---|
| S1 | SKILL.md <= 80 行 | wc -l |
| S2 | 零 canonical 路径冲突 | 审计 |
| S3 | check_devguard_bundle.py 通过 | 脚本 |
| S4 | benchmark >= 12 条，通过率 100% | skillopt |
| S5 | Gate Matrix 存在 | 文件检查 |
| S6 | glossary.md >= 15 术语 | 文件检查 |
| S7 | CHANGELOG 有精炼条目 | 文件检查 |

### 7.4 量化达标 M1-M4

| # | 指标 | 目标 |
|---|---|---|
| M1 | 普通任务 outward 块数 | 2（95% 场景） |
| M2 | outward 字符 | <= 12k |
| M3 | references/ 体积 | <= 100 KB |
| M4 | wrapper 总行数 | <= 450 |

---

## 8. 回归测试方案

### 8.1 skillopt 自动化

每 Phase 合并前：对 benchmark.jsonl 全量 fresh agent，验证 section_present / contains / max_chars / not_contains。

### 8.2 人工 forward test

Regression Example Set 4 场景 + Recommended 9 类中 >= 6 类。

### 8.3 脚本检查

`ash
python scripts/check_devguard_bundle.py
python scripts/generate_rule_loading_manifest.py --format summary
`

### 8.4 回归失败处理

| 失败类型 | 动作 |
|---|---|
| 披露块多余 | 修 template/routing，不删门禁 |
| 门禁被削弱 | **禁止合并** |
| FAST over-gate | 修 Gate Matrix |
| 路径引用断裂 | 修 redirect/index |

---

## 9. 风险登记

| 风险 | 概率 | 影响 | 缓解 |
|---|---|---|---|
| 删重复误删门禁 | 中 | 高 | P0 benchmark + G1-G8 对照 |
| 模板三档 agent 仍输出 full | 中 | 中 | must-not + 脚本 T1 |
| FAST 降级过度 | 中 | 高 | S3 场景回归 |
| shared/ 删除破坏引用 | 低 | 中 | stub 保留 1 版本 |
| skillopt 覆盖不足 | 中 | 中 | 扩至 12+ 条 |

---

## 10. 回滚策略

1. Phase 级回滚：每 Phase 独立 PR
2. shared/ 删除前先 stub 一个版本周期
3. REFINEMENT_BASELINE.md 保留 before 指标
4. 发布 tag v0.2.0-refined；严重问题回 v0.1.0

---

## 11. 排期建议

| 阶段 | 内容 | 工期 | 累计 |
|---|---|---|---|
| P0 | 基线 + skillopt | 0.5-1 天 | 1 天 |
| P1 | 入口去重 | 1-2 天 | 3 天 |
| P2 | 模板三档化 | 2-3 天 | 6 天 |
| P3 | 路由门禁 | 2-4 天 | 10 天 |
| P4 | 调用面 | 1 天 | 11 天 |
| P5 | 降级查文档 | 1-2 天 | 13 天 |
| P6 | 词汇表终验 | 0.5-1 天 | 14 天 |

P1+P2 并行可压缩至 10-12 天。


---

## 12. 交付清单

| 交付物 | 路径 | Phase |
|---|---|---|
| 精炼规划 | docs/REFINEMENT_PLAN.md | - |
| 基线快照 | docs/REFINEMENT_BASELINE.md | P0 |
| 瘦身 SKILL | SKILL.md | P1 |
| 精简 README | README.md | P1 |
| 去重 shared | shared/ stubs | P1 |
| 三档模板 | references/report-templates.md | P2 |
| Gate Matrix | references/task-routing.md | P3 |
| 阻断分层 | references/shared-guardrails.md | P3 |
| Named Routes | references/task-routing.md | P3 |
| Reroute 表 | references/dynamic-reroute-core.md | P3 |
| 短 prompts | agents/openai.yaml, example-prompts.md | P4 |
| Coexistence Rules | SKILL.md | P4 |
| CodeGraph fallback | references/codegraph-project-understanding.md | P5 |
| Official Docs 分层 | references/official-docs-check.md | P5 |
| 词汇表 | references/glossary.md | P6 |
| 扩展 benchmark | skillopt/benchmark.jsonl | P0 |
| CHANGELOG | CHANGELOG.md | P6 |

---

## 13. 发布签核清单

发布 v0.2.0-refined 前，维护者逐项签核：

- [ ] 7.1 硬门禁 G1-G8 全部通过
- [ ] 7.2 披露标准 D1-D7 全部通过
- [ ] 7.3 结构标准 S1-S7 全部通过
- [ ] 7.4 量化指标 M1-M4 达标
- [ ] benchmark 100% + held-out 100%
- [ ] check_devguard_bundle.py 通过
- [ ] CHANGELOG 已更新
- [ ] 无已知 P0 开放问题

---

## 14. 附录 A：benchmark 扩展规格（WP-20）

| task_id | 场景 | 关键 checks |
|---|---|---|
| feature-normal | 普通 feature | ES, TCS, max_chars 12000 |
| refactor-compact | 多文件 refactor | ES, TCS, CodeGraph, max_chars |
| bugfix-evidence | 证据链弱 | ES, TCS, evidence |
| review-only | 纯 review | ES, finding |
| high-risk-installer | 高风险无异常 | ES, Risk Note, TCS |
| anomaly-missing-rule | 缺规则阻断 | ES, Exception Note |
| platform-wpf | 平台约束 | ES, TCS; 可选 Official Docs |
| ui-change | UI 变更 | user operation path |
| ai-tool-calling | AI 功能 | cost, tool bounds |
| repair-failure-reroute | 两次失败 | retrospective, reroute |
| codegraph-stale | 索引 stale | freshness, no silent trust |
| fast-s1-tiny | FAST 小改 | ES, TCS; 无 over-gate |

### judge.checks 扩展建议

- not_contains: Project Understanding Summary（T1）
- not_contains: Rule-Loading Manifest（T1）
- not_contains: Skill Routing Decision（T1）
- section_absent: Exception Note（场景 1）

---

## 15. 附录 B：工作包详细任务分解（节选）

### WP-01

| 步骤 | 动作 | 完成定义 |
|---|---|---|
| 1.1 | 备份当前 SKILL.md | git diff 可回退 |
| 1.2 | 删除 What To Read 清单 | 行数减少 >= 40% |
| 1.3 | 添加 index 链接 | 2 条链接存在 |
| 1.4 | 跑 benchmark | 100% pass |

### WP-09

| 步骤 | 动作 | 完成定义 |
|---|---|---|
| 2.1 | 写 Output Tier Model | T1/T2/T3 表存在 |
| 2.2 | 标记 internal-only | >= 4 块 |
| 2.3 | 压缩 TCS 字段 | 4 字段 |
| 2.4 | 更新 manifest 脚本 | summary 对齐 |
| 2.5 | 更新 forward-testing | 4 场景 |
| 2.6 | 跑 benchmark | 100% pass |

### WP-11

| 步骤 | 动作 | 完成定义 |
|---|---|---|
| 3.1 | 审计重复文件 | 对照表 |
| 3.2 | 确定 canonical | references/ |
| 3.3 | stub 或删除 shared | 无断链 |
| 3.4 | 更新 index | 路径一致 |
| 3.5 | bundle check | 通过 |

---

## 16. 附录 C：forward-testing 对齐检查表

改披露/路由/Contract 后必查：

1. 场景 1 Normal：仅 ES + TCS
2. 场景 2 High-Risk：ES + Risk Note + TCS
3. 场景 3 Anomaly：ES + Exception Note
4. 场景 4 Platform：ES + TCS；允许 Risk/Official Docs；禁止 full Report
5. 不得 silent trust stale CodeGraph
6. UI 不得仅用 internal check 宣称 verified
7. 不得无 Contract 批准 coding
8. 不得 invent rule paths

---

## 17. 附录 D：禁止的「假精炼」清单

1. 删除 Task Contract / Impact Analysis 门禁
2. 合并全部 reference 为单文件
3. 默认跳过 CodeGraph / Official Docs Check
4. 去掉 wrapper skill 导致路径不可发现
5. 用缩短输出掩盖门禁缺失
6. 删除 forward test 失败项而非修复根因
7. 将 BLOCKED 降级为 WARN 且无 Exception Note
8. 为达标 max_chars 而省略 Task Contract Summary
9. 将 full template 内容塞入 Risk Note 规避 must-not
10. 删除 failing test 而非修复根因

---

## 18. 附录 E：基线快照模板

见 docs/REFINEMENT_BASELINE.md（P0 创建，P6 更新 before/after）。

---

*文档结束。执行时以 Phase 顺序推进，每 Phase 合并前满足该 Phase 验收标准与第 7 节回归要求。*
