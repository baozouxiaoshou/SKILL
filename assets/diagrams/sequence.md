# 时序图模板（Sequence Diagram）

> 表达系统间调用顺序与交互

---

## 模板 1：基础用户登录

```mermaid
sequenceDiagram
    participant U as 用户
    participant App as App 端
    participant Server as 服务端
    participant DB as 数据库
    
    U->>App: 输入账号密码
    App->>Server: 发送登录请求
    Server->>DB: 查询用户信息
    DB-->>Server: 返回用户对象
    Server-->>App: 验证通过 + Token
    App-->>U: 显示登录成功
    
    Note over App,Server: Token 有效期 7 天
```

---

## 模板 2：RAS 双语录入

```mermaid
sequenceDiagram
    participant U as 合规专员
    participant Web as Web 端
    participant API as RAS API
    participant HPS as HPS 翻译引擎
    participant Term as 术语库
    participant DB as 数据库
    
    U->>Web: 输入中文风险概述
    Web->>API: POST /risk-input
    API->>HPS: 请求翻译
    HPS->>Term: 查询术语
    Term-->>HPS: 返回术语映射
    HPS-->>API: 返回英文翻译
    API->>API: 双语合并存储
    API->>DB: 写入双语版本
    DB-->>API: 写入成功
    API-->>Web: 返回双语结果
    Web-->>U: 显示双语预览
```

---

## 模板 3：支付流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant Order as 订单系统
    participant Pay as 支付系统
    participant Bank as 银行
    
    U->>Order: 创建订单
    Order->>Pay: 请求支付单
    Pay-->>Order: 返回支付链接
    Order-->>U: 显示支付二维码
    
    U->>Bank: 扫码支付
    Bank->>Pay: 支付回调
    Pay->>Pay: 验证签名
    Pay-->>Bank: 确认成功
    
    Pay->>Order: 通知支付结果
    Order->>Order: 更新订单状态
    Order-->>U: 通知用户
```

---

## 模板 4：勘误流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant UI as UI
    participant API as 后端
    participant V1 as v1 存储
    participant V2 as v2 存储
    participant Term as 术语库
    
    U->>UI: 点击勘误
    UI-->>U: 进入编辑模式
    U->>UI: 修改译文
    UI->>API: PATCH /correction
    API->>V1: 读取原文
    V1-->>API: 返回原文
    API->>V2: 创建新版本
    V2-->>API: 保存成功
    API->>Term: 学习新术语?
    Term-->>API: 返回接受/拒绝
    API-->>UI: 返回成功
    UI-->>U: 显示新版本
```

---

## 模板 5：异步批量任务

```mermaid
sequenceDiagram
    participant U as 用户
    participant API as API
    participant Queue as 队列
    participant Worker as Worker
    participant Engine as HPS
    participant DB as 数据库
    
    U->>API: 提交批量翻译 50 份
    API->>Queue: 入队 50 个任务
    API-->>U: 返回任务 ID
    
    loop 异步 Worker 处理
        Worker->>Queue: 拉取任务
        Queue-->>Worker: 返回任务
        Worker->>Engine: 调用翻译
        Engine-->>Worker: 返回译文
        Worker->>DB: 存储双语
        Worker->>Queue: 标记完成
    end
    
    API->>U: 推送完成通知
```

---

## 模板 6：含错误处理

```mermaid
sequenceDiagram
    participant U as 用户
    participant Client as 客户端
    participant Server as 服务端
    participant Cache as 缓存
    
    U->>Client: 触发操作
    Client->>Server: 发送请求
    
    alt 正常流程
        Server->>Cache: 查询
        Cache-->>Server: 命中
        Server-->>Client: 返回数据
    else 服务异常
        Server-->>Client: 500 错误
        Client->>Client: 重试 3 次
        Client->>Server: 再次请求
        Server-->>Client: 返回数据
    else 缓存未命中
        Server->>Server: 读数据库
        Server->>Cache: 写入缓存
        Server-->>Client: 返回数据
    end
    
    Client-->>U: 显示结果
```

---

## 自检问题
- [ ] 所有角色是否都列出来了？
- [ ] 消息方向是否清晰（请求 vs 响应）？
- [ ] 异步 / 同步是否区分？
- [ ] 错误处理路径是否包含？
- [ ] 是否过于复杂（参与者 > 6 个考虑拆）？

---

## 实战技巧

### 方向箭头
- `->>` 实线箭头（同步请求）
- `-->>` 虚线箭头（异步响应）
- `-x` 失败带叉（错误）
- `-)` 开放箭头（异步消息）

### 标注
- `Note over A,B`: A 和 B 之间的注释
- `Note right of A`: A 右侧的注释
- `loop ... end`: 循环
- `alt ... else ... end`: 条件分支
- `par ... and ... end`: 并行

### 命名规范
- 参与者名简洁（人用首字母、系统用简称）
- 消息动词清晰（"查询"、"返回"、"通知"）
- 顺序编号（如 "1. 验证 → 2. 存储"）
