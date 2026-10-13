# 泳道图模板（Swimlane Diagram）

> 表达多角色/多系统的协作流程（B 端场景必备）

---

## 模板 1：B 端审批流（3 角色）

```mermaid
flowchart LR
    subgraph 申请人[申请人]
        A1[提交申请] --> A2[等待审批]
    end
    
    subgraph 主管[部门主管]
        B1[接收通知] --> B2{审核材料}
        B2 -->|通过| B3[签字]
        B2 -->|驳回| B4[写意见]
    end
    
    subgraph 财务[财务]
        C1[接收单据] --> C2{额度检查}
        C2 -->|通过| C3[打款]
        C2 -->|不通过| C4[退回]
    end
    
    A1 --> B1
    B3 --> C1
    B4 --> A2
    C4 --> A2
    C3 --> A5[通知申请人]
    
    style A1 fill:#e3f2fd
    style B1 fill:#fff3e0
    style C1 fill:#fce4ec
```

---

## 模板 2：合规录入流程（4 角色）

```mermaid
flowchart TB
    subgraph 合规专员[合规专员]
        C1A[录入中文] --> C1B[校对英文]
        C1B --> C1C[勘误]
    end
    
    subgraph 翻译引擎[HPS 引擎]
        E1[接收原文] --> E2[生成译文]
        E2 --> E3[应用术语库]
    end
    
    subgraph 主管[主管]
        M1[审核提交] --> M2{合规校验}
        M2 -->|通过| M3[签字]
        M2 -->|驳回| M4[退回]
    end
    
    subgraph 系统[系统]
        S1[版本快照] --> S2[审计日志]
    end
    
    C1A --> E1
    E3 --> C1B
    C1C --> M1
    M3 --> S1
    M4 --> C1C
    
    style C1A fill:#e3f2fd
    style E1 fill:#fff3e0
    style M1 fill:#fce4ec
    style S1 fill:#e8f5e9
```

---

## 模板 3：跨境订单处理

```mermaid
flowchart LR
    subgraph 买家[买家]
        U1[下单]
    end
    
    subgraph 平台[电商平台]
        P1[订单审核] --> P2[风控检查]
    end
    
    subgraph 卖家[卖家]
        S1[确认订单] --> S2[发货]
    end
    
    subgraph 物流[物流]
        L1[接收包裹] --> L2[国际运输]
    end
    
    subgraph 海关[海关]
        C1[清关申报] --> C2{查验?}
        C2 -->|是| C3[人工查验]
        C2 -->|否| C4[放行]
    end
    
    U1 --> P1
    P2 --> S1
    S2 --> L1
    L2 --> C1
    C3 --> L2
    C4 --> L3[送达买家]
    L3 --> U2[买家收货]
    
    style U1 fill:#e3f2fd
    style P1 fill:#fff3e0
    style S1 fill:#fce4ec
    style L1 fill:#e8f5e9
    style C1 fill:#ffcdd2
```

---

## 模板 4：版本管理流程

```mermaid
flowchart LR
    subgraph 用户[录入员]
        U1[录入 v1] --> U2[提交]
        U1 -.勘误.-> U3[修改 v2]
    end
    
    subgraph 翻译[翻译引擎]
        E1[生成译文 v1] --> E2[应用到 v1]
        E3[重新生成 v2] --> E4[应用到 v2]
    end
    
    subgraph 系统[版本管理]
        S1[快照 v1] --> S2[快照 v2]
        S2 --> S3[版本对比]
    end
    
    subgraph 审计[审计员]
        A1[追溯版本] --> A2[导出历史]
    end
    
    U2 --> E1
    E2 --> S1
    U3 --> E3
    E4 --> S2
    S2 --> S3
    S3 --> A1
    
    style U1 fill:#e3f2fd
    style E1 fill:#fff3e0
    style S1 fill:#fce4ec
    style A1 fill:#e8f5e9
```

---

## 自检问题
- [ ] 每个角色是否清晰定义？
- [ ] 角色间交接是否明确？
- [ ] 异常路径是否覆盖（驳回、退回）？
- [ ] 每个角色内部流程是否完整？
- [ ] 是否需要进一步拆分系统 vs 业务角色？

---

## 实战技巧

### 角色设计
- 按组织角色分：申请人、主管、财务、法务、IT
- 按系统角色分：前端、后端、数据库、第三方服务
- 混合模式：业务角色 + 系统角色（适合复杂流程）

### 颜色规范
- 每个角色一个主色调
- 蓝色系：用户/客户
- 黄色系：审核/中台
- 粉色系：决策/管理层
- 绿色系：后台/系统

### 文字精简
- 节点文字 ≤10 字
- 状态/分支用关键词（"通过"、"驳回"、"已读"）

### 流程方向
- 横向（LR）：角色少、流程短
- 纵向（TB）：角色多、流程长
