# DevGuard P7 精炼规划：入口收敛与运行层级压缩

| 字段 | 值 |
|---|---|
| 文档版本 | v1.0 |
| 创建日期 | 2026-06-19 |
| 适用范围 | devguard/ 技能包本体（不含具体业务项目规则） |
| 前置批次 | P0–P6（v0.2.0-refined）、v0.2.1（Socratic inquiry） |
| 关联文档 | [REFINEMENT_PLAN.md](REFINEMENT_PLAN.md)、[REFINEMENT_BASELINE.md](REFINEMENT_BASELINE.md)、[forward-testing.md](../references/forward-testing.md) |
| 目标发布 | v0.3.0-refined |

---

## 1. 背景与动机

P0–P6 已解决规则重复披露、默认输出过重、路由歧义、shared/references 去重等问题；v0.2.1 新增 **Socratic inquiry** 后，agent 在路由与 Contract 冻结之间又多了一跳决策。

当前主要矛盾从「缺规则」转为「**入口与层级过多导致默认成本高**」：

| 类别 | 现状（v0.2.1） | 问题 |
|---|---|---|
| 外部入口 | SKILL + README 工作流 + openai.yaml + example-prompts + 多安装副本 | agent 不知先读谁；副本漂移 |
| 内部入口 | 15 个 wrapper SKILL + rule-disclosure-index + chain 映射 | 每增模块多一跳；查表分散 |
| 运行层级 | README 描述 **6 层**；SKILL **8 步** Default Workflow | 心智负担高；与真实门禁链不对齐 |
| 默认阅读面 | report-templates ~665 行（含 T3 正文） | 易误读 full template、误输出中间态 |
| 脚本门禁 | manifest 可选；无 Prepare 后 validate | 三相压缩后更易「跳备跑」 |
| 回归 | benchmark 12 条；无 socratic / lite-skip-inquiry | 新门禁无网 |

**P7 核心诉求**（用户指定）：

1. **入口变少** — 对外只保留一个权威工作流入口
2. **运行层级变少** — 对外只呈现 **3 相**（Orient → Prepare → Act），内部门禁链保留但不外显为 8 步

**P7 不变项**：G1–G8 硬门禁、Gate Matrix、Named Routes、T1/T2 默认两块输出、domain core 正文、P0 回归网。

---

## 2. P7 精炼目标

### 2.1 量化目标

| 指标 | 基线（v0.2.1） | P7 目标 |
|---|---|---|
| 外部权威工作流入口 | 4 | **1**（仅 SKILL.md） |
| 对外可见运行步数 | 8 | **3**（Orient / Prepare / Act） |
| README 架构层数 | 6 | **3**（与三相映射） |
| SKILL.md 行数 | 96 | **≤ 65** |
| report-templates.md | ~665 | **≤ 280**（T3 外置） |
| wrapper SKILL 数量 | 15 | **0–3** |
| 运行时查表文件 | 3+ | **1**（devguard-lookup.md，≤200 行） |
| 安装 canonical 副本 | 多副本手工同步 | **1** + sync 脚本 |
| skillopt 场景数 | 12 | **≥ 16** |

### 2.2 三相运行模型

```text
Orient（定向） → Prepare（备跑） → Act（执行与验收）
```

| Phase | 合并内容 | 默认对外输出 | 内部子门禁（保留） |
|---|---|---|---|
| Orient | 路由、Socratic?、load plan、ES/TCS/Slice/Inquiry | ES + TCS 或 Inquiry Note | Task Profile、Named Route |
| Prepare | PU → Docs? → IA → Contract | 默认无独立块（收敛进 TCS） | Gate Matrix 全部 |
| Act | TDD、domain、review、reroute | Completion / Review Summary | Evidence、TDD Red |

**事实变化** → 回 Orient（更新 ES：Mode / Rules / Status / Next）。

| 旧六层 | P7 相 |
|---|---|
| 入口 + 路由 + 规则加载（计划） | Orient |
| 分析门禁层 | Prepare |
| 执行 + 审查控制 | Act |

### 2.3 非目标

不删 Socratic；不合并 Prepare 子门禁；不删 domain core；不削弱 G1–G8；不把 T3 塞回默认 template；不默认跳过 validate。

---

## 3. P7 原则

1. 一步入口（SKILL 唯一权威）
2. 三相可见、门禁不可见
3. 查表一次（devguard-lookup.md）
4. T1/T2 与 T3 物理拆分
5. 脚本出块 + validate 放行 Prepare
6. 减 wrapper 不减 reference
7. 单源发布 + sync 脚本
8. 改披露先跑 forward test

---

## 4. 工作包总览（WP-30 – WP-39）

| 子阶段 | WP | 名称 |
|---|---|---|
| P7-A | WP-30 | 单入口收敛 |
| P7-A | WP-31 | T3 外置 |
| P7-A | WP-38 | SKILL ≤65 行 |
| P7-B | WP-32 | control-plane-core 三相 |
| P7-B | WP-33 | module-registry；wrapper ≤3 |
| P7-B | WP-34 | devguard-lookup 单表 |
| P7-C | WP-35 | manifest + validate_outward_packet |
| P7-C | WP-36 | skillopt 扩展（socratic/lite） |
| P7-D | WP-37 | sync_devguard_install.py |
| P7-D | WP-39 | 基线 + v0.3.0 签核 |

依赖：P7-A → P7-B → P7-C → P7-D。

---

## 5. 分阶段执行方案

### P7-A：入口与模板瘦身

#### WP-30 单入口收敛

1. SKILL.md 保留：三相 Default Workflow、模块/registry 链接、压缩 Operating Rules、Helper Scripts
2. README.md：6 层/8 步改为三相图 + 链接 SKILL；保留安装与 skillopt
3. openai.yaml default_prompt 一行指向 SKILL 三相
4. example-prompts.md 每场景 1 行；删除重复 workflow
5. rule-disclosure-index 顶部声明「工作流权威：SKILL.md」

**完成定义**：新 agent 只读 SKILL 即可 Orient；README 无冲突逐步流程。

#### WP-31 T3 外置

1. 新建 report-templates-detailed.md 承载 T3 全文
2. report-templates.md ≤280 行：Tier 表 + T1/T2 + must-not + Inquiry
3. 更新 forward-testing、manifest 脚本注释

#### WP-38 SKILL ≤65 行

1. Default Workflow 改为 Orient / Prepare / Act 各 1 句
2. 模块表 → 链接 devguard-module-registry.md
3. Coexistence 压缩或移入 lookup

---

### P7-B：三相控制面与模块面

#### WP-32 control-plane-core.md

定义三相：目的、准入、准出、默认输出、禁止跳跃；Prepare 子门禁顺序与 Gate Matrix 对齐；reroute 回 Orient 规则。task-routing Named Routes 标注 [Orient]/[Prepare]/[Act]。

#### WP-33 devguard-module-registry.md

模块 ID、相位、canonical core 路径。默认 0 wrapper，直读 references/*-core.md；兼容保留 ≤3 薄 wrapper（task-router、codegraph、TDD）。其余 skills/XX 先 stub 一版本。

#### WP-34 devguard-lookup.md（≤200 行）

合并：输出 Tier、Named Routes 速查、Reroute 触发器、模块路径、短触发词。disclosure-index / chain-mapping 改 stub 指向 lookup。

---

### P7-C：脚本门禁与回归

#### WP-35 manifest + validate

FAST+ Prepare 准出须 manifest summary；新增 validate_outward_packet（或并入 bundle check）：Orient 块齐全、T1 must-not、Prepare 未完成 → BLOCKED。control-plane Act 准入 = validate pass。

#### WP-36 skillopt 扩展（≥16 条）

新增：socratic-inquiry、lite-skip-inquiry、three-phase-normal、prepare-blocked-skip。

---

### P7-D：发布与同步

#### WP-37 sync_devguard_install.py

canonical `.codex/skills/devguard` → `.cursor`、`.agents` 薄副本；支持 --dry-run。

#### WP-39 签核

更新 REFINEMENT_BASELINE P7 列、CHANGELOG v0.3.0-refined、tag 发布。

---

## 6. 验收标准

### 6.1 硬门禁 G1–G8（与 P6 相同）

G1 无 Contract 不编码；G2 bug 无 failing 不宣称修复；G3 无 evidence 不完成；G4 不编造路径；G5 TDD Red 不跳；G6 UI 须操作路径；G7 两次失败须 retrospective；G8 BLOCKED 须 Exception Note。

### 6.2 P7 入口与层级 E1–E8

| ID | 标准 |
|---|---|
| E1 | 仅 SKILL 含完整三相 workflow |
| E2 | control-plane-core 与 SKILL 三相一致 |
| E3 | devguard-lookup ≤200 行，唯一主查表 |
| E4 | wrapper ≤3 |
| E5 | report-templates ≤280，T3 在 detailed |
| E6 | benchmark 含 socratic + lite-skip |
| E7 | sync 脚本存在 |
| E8 | SKILL ≤65 行 |

### 6.3 披露 D1–D7、量化 M1–M4

与 P6 相同（T1 ES+TCS、LITE Slice、Inquiry 无 premature TCS、reroute 仅 ES 四字段；benchmark ≥16 schema 100%、bundle pass、outward ≤12k）。

---

## 7. 回归测试

每子阶段合并前：

```bash
python scripts/check_devguard_bundle.py
python scripts/generate_rule_loading_manifest.py --format summary
```

forward 必查：Normal、High-Risk、Anomaly、Platform、Socratic、LITE micro。

失败处理：跳 Prepare → 修 validate，**禁止**删门禁；入口歧义 → 修 README stub。

---

## 8. 风险与回滚

| 风险 | 缓解 |
|---|---|
| wrapper 断链 | registry + stub 一版本 |
| 三相被误解为可跳 Prepare | validate + P0 文案 |
| lookup 超长 | 只速查，细节链 core |
| sync 漏文件 | dry-run + bundle check |

回滚：子阶段独立 PR；严重问题回 v0.2.1；tag v0.3.0-refined。

---

## 9. 排期（约 8 天）

P7-A 1–2d → P7-B 2–3d → P7-C 1–2d → P7-D 0.5–1d。

---

## 10. 交付清单

| 交付物 | 路径 |
|---|---|
| 三相控制面 | references/control-plane-core.md |
| 模块注册表 | references/devguard-module-registry.md |
| 单表 lookup | references/devguard-lookup.md |
| T3 外置 | references/report-templates-detailed.md |
| validate | scripts/validate_outward_packet.py |
| sync | scripts/sync_devguard_install.py |

---

## 11. 附录 A：benchmark 新增（WP-36）

| task_id | 关键 checks |
|---|---|
| socratic-inquiry | ES, Inquiry Note, not_contains TCS |
| lite-skip-inquiry | ES, Slice, not_contains Inquiry |
| three-phase-normal | ES, TCS, not_contains PU summary |
| prepare-blocked-skip | BLOCKED / Exception Note |

## 12. 附录 B：旧八步 → 三相

Route/Socratic/loads/gates/emit → Orient；PU→Docs→IA→Contract → Prepare；handoff/reroute → Act。

## 13. 附录 C：假精炼（P7 补充 11–17）

11 合并 Prepare 为一步；12 删 Coexistence；13 删 core 正文；14 lookup 替代 Contract；15 跳过 validate；16 README 六层与三相并存；17 为瘦身删 Helper Scripts。

## 14. 附录 D：口诀

```text
一个技能进门 · 三步走完 · 两块平时输出 · 事实变了回 Orient
```

## 15. 附录 E：与 P6 关系

P6 已做：T1/T2/T3 三档、Gate Matrix、glossary、shared 去重。P7 增量：单入口、三相、T3 外置、registry、lookup、sync、≥16 benchmark。**不重复** P6 已完成项。

---

*文档结束。实施时每子阶段须 bundle check + skillopt。*