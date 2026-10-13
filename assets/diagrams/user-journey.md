# 用户旅程图模板（User Journey Map）

> 展示用户从认知到传播的完整体验路径。

---

## 模板 1：基础版（5 阶段）

```mermaid
flowchart LR
    A[认知<br/>Awareness] --> B{考虑<br/>Consideration}
    B -->|感兴趣| C[使用<br/>Use]
    B -->|不感兴趣| X[流失]
    C --> D{满意?}
    D -->|是| E[留存<br/>Retention]
    D -->|否| Y[流失]
    E --> F[传播<br/>Advocacy]
    
    style A fill:#e3f2fd
    style C fill:#fff3e0
    style E fill:#e8f5e9
    style F fill:#fce4ec
    style X fill:#ffebee
    style Y fill:#ffebee
```

---

## 模板 2：详细版（含触点）

```mermaid
flowchart LR
    subgraph 认知阶段
        A1[看到广告] --> A2[搜索了解]
    end
    
    subgraph 考虑阶段
        B1[查看评价] --> B2{对比选择}
    end
    
    subgraph 使用阶段
        C1[首次使用] --> C2[学习探索]
        C2 --> C3[熟练使用]
    end
    
    subgraph 留存阶段
        D1[形成习惯] --> D2[高频使用]
        D2 --> D3{遇到问题}
        D3 -->|自助解决| D1
        D3 -->|找客服| D5[客服介入]
        D5 --> D1
    end
    
    subgraph 传播阶段
        E1[推荐给朋友] --> E2[社交分享]
        E2 --> E3[主动评价]
    end
    
    A2 --> B1
    B2 -->|选择| C1
    C3 --> D1
    D2 --> E1
    
    style A1 fill:#e3f2fd
    style B2 fill:#fff3e0
    style C1 fill:#fff3e0
    style D1 fill:#e8f5e9
    style E1 fill:#fce4ec
```

---

## 模板 3：情绪曲线版

```mermaid
flowchart LR
    A[😟 困惑<br/>认知] --> B[😐 中性<br/>考虑]
    B --> C[😊 期待<br/>首次体验]
    C --> D[🤩 惊喜<br/>Aha 时刻]
    D --> E[😐 习惯<br/>留存]
    E --> F[😊 满足<br/>持续]
    F --> G[🤩 推荐<br/>传播]
    
    G -.流失.-> H[😟 离开]
    H -.唤回.-> C
    
    style A fill:#ffebee
    style D fill:#fff3e0
    style G fill:#fce4ec
```

---

## 模板 4：跨设备旅程

```mermaid
flowchart LR
    subgraph 手机端
        M1[刷信息流] --> M2[看到内容]
        M2 --> M3[点击详情]
    end
    
    subgraph 电脑端
        P1[搜索相同内容] --> P2[深度阅读]
    end
    
    subgraph 平板端
        T1[睡前浏览]
    end
    
    M3 --> P1
    P2 --> T1
    
    style M1 fill:#e3f2fd
    style P1 fill:#e8f5e9
    style T1 fill:#fff3e0
```

---

## 模板 5：B 端版本（6 阶段）

```mermaid
flowchart LR
    A[接收任务<br/>Task] --> B[准备<br/>Prepare]
    B --> C[执行<br/>Execute]
    C --> D{校对<br/>Review}
    D -->|需修改| C
    D -->|通过| E[提交<br/>Submit]
    E --> F[归档<br/>Archive]
    
    F -.追溯.-> G[审计<br/>Audit]
    G -.合规问题.-> H[整改]
    H -.更新.-> F
    
    style A fill:#e3f2fd
    style C fill:#fff3e0
    style E fill:#e8f5e9
    style F fill:#fce4ec
    style H fill:#ffebee
```

---

## 自检问题
- [ ] 是否覆盖了完整旅程（认知 → 传播 / 流失）？
- [ ] 触点是否具体（不是"用户想做什么"）？
- [ ] 关键节点是否有标注（情绪、Aha 时刻）？
- [ ] 流失路径是否清晰？
- [ ] 唤回路径是否包含？

---

## 实战技巧

### 添加痛点和机会点
可以用注释文字：
```mermaid
flowchart LR
    A[认知] -->|痛点:信息过载| B[考虑]
    B -->|机会:个性化推荐| C[使用]
```

### 用颜色表达情绪
- 红色系：负面情绪（😟😕）
- 黄色系：中性（😐）
- 绿色系：正面（😊🤩）

### 突出 Aha 时刻
用特殊节点符号（emoji + 颜色）：
```mermaid
D[🤩 Aha!<br/>首次成功]
style D fill:#ffeb3b,stroke:#f57f17,stroke-width:3px
```
