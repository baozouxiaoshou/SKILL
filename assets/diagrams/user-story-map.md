# 用户故事地图模板（User Story Map）

> 按 Jeff Patton 方法拆解：Spine → Activity → Story → Task

---

## 模板 1：标准故事地图

```mermaid
flowchart TB
    subgraph Spine["脊椎（用户目标）"]
        S1[作为健身小白<br/>我想养成运动习惯]
    end
    
    subgraph Activities["活动（Activity）"]
        A1[选择计划]
        A2[开始训练]
        A3[记录反馈]
    end
    
    subgraph Stories["故事（Story）"]
        ST1[3 步问卷]
        ST2[生成 30 天计划]
        ST3[每日推荐]
        ST4[完成反馈]
        ST5[动态调整]
    end
    
    subgraph Tasks["任务（Task）"]
        T1[选目标]
        T2[选水平]
        T3[选时间]
        T4[计算能力]
        T5[匹配模板]
        T6[生成计划]
    end
    
    S1 --> A1
    S1 --> A2
    S1 --> A3
    
    A1 --> ST1
    A1 --> ST2
    A2 --> ST3
    A2 --> ST4
    A3 --> ST5
    
    ST1 --> T1
    ST1 --> T2
    ST1 --> T3
    ST2 --> T4
    ST2 --> T5
    ST2 --> T6
    
    style S1 fill:#fce4ec
    style Activities fill:#fff3e0
    style Stories fill:#e8f5e9
    style Tasks fill:#e3f2fd
```

---

## 模板 2：时间分层版

```mermaid
flowchart LR
    subgraph M1["Sprint 1: MVP"]
        M1A[引导流程]
        M1B[核心闭环]
    end
    
    subgraph M2["Sprint 2: 增长"]
        M2A[反馈机制]
        M2B[动态调整]
    end
    
    subgraph M3["Sprint 3: 进阶"]
        M3A[30 天里程碑]
        M3B[横向探索]
    end
    
    M1 --> M2
    M2 --> M3
    
    M1A -.优先级 P0.-> A[核心 Story]
    M1B -.优先级 P0.-> A
    M2A -.优先级 P1.-> B[增长 Story]
    M2B -.优先级 P1.-> B
    M3A -.优先级 P2.-> C[长期 Story]
    M3B -.优先级 P2.-> C
    
    style M1 fill:#fff3e0
    style M2 fill:#e8f5e9
    style M3 fill:#e3f2fd
```

---

## 模板 3：B 端流程版本

```mermaid
flowchart TB
    subgraph Spine["脊椎"]
        S1[作为合规专员<br/>我要高效提交双语异常分析]
    end
    
    subgraph Activity1["录入"]
        ST1[选择语言]
        ST2[录入中文]
        ST3[自动翻译]
    end
    
    subgraph Activity2["校对"]
        ST4[查看英文]
        ST5[勘误]
    end
    
    subgraph Activity3["提交"]
        ST6[生成快照]
        ST7[审计追溯]
    end
    
    S1 --> Activity1
    S1 --> Activity2
    S1 --> Activity3
    
    Activity1 --> ST1
    Activity1 --> ST2
    Activity1 --> ST3
    Activity2 --> ST4
    Activity2 --> ST5
    Activity3 --> ST6
    Activity3 --> ST7
    
    style Spine fill:#fce4ec
    style Activity1 fill:#fff3e0
    style Activity2 fill:#e8f5e9
    style Activity3 fill:#e3f2fd
```

---

## 模板 4：切割 Release 版

```mermaid
flowchart LR
    subgraph R1["Release 1"]
        R1S1[核心闭环 P0]
        R1S2[基础 AC]
    end
    
    subgraph R2["Release 2"]
        R2S1[反馈机制 P1]
        R2S2[动态调整 P1]
    end
    
    subgraph R3["Release 3"]
        R3S1[长期能力 P2]
        R3S2[扩展场景 P2]
    end
    
    R1 --> R2 --> R3
    
    R1S1 -.Ship MVP.-> USR1[🎯 30% 用户]
    R2S1 -.Ship Growth.-> USR2[🎯 60% 用户]
    R3S1 -.Ship Long.-> USR3[🎯 90% 用户]
```

---

## 自检问题
- [ ] Spine 是否清晰表达了用户目标？
- [ ] Activity 是否是"活动"而非"功能"？
- [ ] Story 是否独立、可估算？
- [ ] 切割线是否明确（每个 Release 的边界）？
- [ ] 优先级是否与切割一致？

---

## 实战技巧

### 切割规则
- 每个 Release 必须能独立发布
- 每个 Release 包含 1-2 个 P0 Story
- 增量价值：每个 Release 比前一个增加 1-2 个能力

### 横向切割 vs 纵向切割
- 纵向：按时间分 Release（推荐）
- 横向：按用户角色分（如：合规专员 / 监管员各自先做核心）
- 斜向：按场景分（如：紧急场景 vs 常规场景）

### 避免
- ❌ Spine 太宽泛（"用户用得开心"）
- ❌ Activity 是功能名（"我要设置功能"）
- ❌ Story 粒度太大（"我要完整系统"）
