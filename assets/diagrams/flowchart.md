# 流程图模板（Flowchart）

> 业务流程、操作流程的通用表达

---

## 模板 1：基础决策流

```mermaid
flowchart TD
    A([开始]) --> B[选择计划]
    B --> C[确认信息]
    C --> D{验证成功?}
    D -->|是| E[执行计划]
    D -->|否| F[提示错误]
    F --> B
    E --> G([结束])
    
    style A fill:#c8e6c9
    style G fill:#ffcdd2
    style D fill:#fff9c4
```

---

## 模板 2：多分支流程

```mermaid
flowchart LR
    A[提交订单] --> B{支付方式}
    B -->|微信| C[微信支付]
    B -->|支付宝| D[支付宝支付]
    B -->|银行卡| E[银联支付]
    
    C --> F{支付结果}
    D --> F
    E --> F
    
    F -->|成功| G[生成订单]
    F -->|失败| H[提示失败]
    F -->|超时| I[取消订单]
    
    H --> B
    I --> J[结束]
    G --> J
    
    style B fill:#fff9c4
    style F fill:#fff9c4
    style G fill:#c8e6c9
```

---

## 模板 3：含子流程

```mermaid
flowchart TD
    A[用户下单] --> B[创建订单]
    B --> C[[支付流程]]
    
    subgraph 支付流程
        C1[选择支付] --> C2[扫码支付]
        C2 --> C3{支付成功?}
        C3 -->|是| C4[回调通知]
        C3 -->|否| C5[支付失败]
    end
    
    C --> C1
    C4 --> D[更新订单状态]
    C5 --> E[取消订单]
    D --> F[发送通知]
    
    style A fill:#e3f2fd
    style F fill:#c8e6c9
```

---

## 模板 4：异常处理流程

```mermaid
flowchart TD
    A[发起请求] --> B{网络正常?}
    B -->|是| C[发送数据]
    B -->|否| B1[重试 1]
    B1 -->|重试 3 次失败| B2[本地缓存]
    
    C --> D{服务器响应}
    D -->|200 OK| E[成功]
    D -->|500 错误| D1[重试]
    D -->|404 未找到| D2[提示用户]
    D -->|超时| D3[超时提示]
    
    D1 --> D
    D2 --> F[结束]
    D3 --> D1
    E --> F
    B2 --> F
    
    style B fill:#fff9c4
    style D fill:#fff9c4
    style E fill:#c8e6c9
    style B2 fill:#ffcdd2
```

---

## 模板 5：B 端审批流程

```mermaid
flowchart TD
    A[提交申请] --> B[初审]
    B --> C{材料完整?}
    C -->|否| C1[退回补充]
    C -->|是| D[主管审核]
    C1 --> A
    
    D --> E{审核通过?}
    E -->|是| F[财务审批]
    E -->|否| D1[驳回]
    D1 --> C1
    
    F --> G{金额超限?}
    G -->|是| H[总监审批]
    G -->|否| I[财务终审]
    H --> I
    
    I --> J{通过?}
    J -->|是| K[放款]
    J -->|否| D1
    K --> L[结束]
    
    style A fill:#e3f2fd
    style K fill:#c8e6c9
    style D1 fill:#ffcdd2
```

---

## 模板 6：登录注册流程

```mermaid
flowchart TD
    A[打开 App] --> B{已登录?}
    B -->|是| C[进入主页]
    B -->|否| D[登录页]
    
    D --> E{登录方式}
    E -->|手机号| F[输入手机号]
    E -->|微信| G[微信授权]
    E -->|Apple ID| G
    
    F --> H[发送验证码]
    H --> I[输入验证码]
    I --> J{验证通过?}
    J -->|是| K[进入主页]
    J -->|否| L[重试/找回密码]
    
    G --> K
    
    C --> M([正常使用])
    K --> M
    
    style A fill:#e3f2fd
    style M fill:#c8e6c9
```

---

## 自检问题
- [ ] 起点和终点是否明确？
- [ ] 判断节点是否清晰（菱形 + 条件）？
- [ ] 异常路径是否覆盖？
- [ ] 子流程是否合理封装？
- [ ] 是否太复杂（超过 20 个节点考虑拆分）？

---

## 实战技巧

### 颜色规范
- 起点/终点：绿色（`#c8e6c9`）
- 判断节点：黄色（`#fff9c4`）
- 成功路径：绿色
- 失败/异常路径：红色（`#ffcdd2`）
- 异常流程：橙色

### 文字规范
- 节点标题 ≤8 字
- 判断条件 ≤15 字
- 路径标签清晰（如"是/否"、"成功/失败"）

### 复杂度控制
- 单图不超过 15 个节点
- 超过则用子图（subgraph）或拆分成多张图
