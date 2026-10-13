# ER 图模板（Entity Relationship）

> 表达数据模型（B 端必备）

---

## 模板 1：基础 ER 图（语法提示）

> ⚠️ Mermaid 的 erDiagram 是简化版，复杂模型建议用 dbdiagram.io 或 PowerDesigner

---

## 模板 2：RAS 双语录入系统 ER 图

```mermaid
erDiagram
    USER ||--o{ REPORT : "writes"
    REPORT ||--|{ TRANSLATION : "has"
    REPORT ||--|{ VERSION_SNAPSHOT : "snapshotted as"
    REPORT ||--o{ AUDIT_LOG : "tracked by"
    USER ||--o{ AUDIT_LOG : "performed"
    TERM_LIBRARY ||--o{ TRANSLATION : "applied to"
    REPORT ||--o{ ATTACHMENT : "contains"
    
    USER {
        string user_id PK
        string name
        string role "合规专员/主管/审计"
        string department
        string email
        date created_at
    }
    
    REPORT {
        string report_id PK
        string user_id FK
        string title
        text content_zh
        text content_en
        string status "草稿/已翻译/已校对/已提交"
        date created_at
        date submitted_at
    }
    
    TRANSLATION {
        string translation_id PK
        string report_id FK
        text original_text
        text translated_text
        string engine "HPS/Manual"
        float confidence
    }
    
    VERSION_SNAPSHOT {
        string snapshot_id PK
        string report_id FK
        int version_no
        text content_snapshot
        string operator_id FK
        timestamp created_at
        boolean is_locked
    }
    
    AUDIT_LOG {
        string log_id PK
        string user_id FK
        string report_id FK
        string action "view/edit/submit/export"
        string ip_address
        timestamp created_at
    }
    
    TERM_LIBRARY {
        string term_id PK
        string source_term
        string target_term
        string domain "金融/法律/医疗"
        int usage_count
    }
    
    ATTACHMENT {
        string attachment_id PK
        string report_id FK
        string filename
        string file_url
        int file_size
    }
```

---

## 模板 3：电商订单 ER 图

```mermaid
erDiagram
    USER ||--o{ ORDER : "places"
    USER ||--o{ ADDRESS : "has"
    USER ||--o{ CART : "owns"
    ORDER ||--|{ ORDER_ITEM : "contains"
    ORDER ||--o{ PAYMENT : "settled by"
    PRODUCT ||--o{ ORDER_ITEM : "listed in"
    CATEGORY ||--o{ PRODUCT : "groups"
    
    USER {
        string user_id PK
        string email
        string name
        date created_at
    }
    
    ORDER {
        string order_id PK
        string user_id FK
        decimal total_amount
        string status
        timestamp created_at
        timestamp paid_at
    }
    
    ORDER_ITEM {
        string item_id PK
        string order_id FK
        string product_id FK
        int quantity
        decimal unit_price
    }
    
    PRODUCT {
        string product_id PK
        string category_id FK
        string name
        decimal price
        int stock
    }
    
    CATEGORY {
        string category_id PK
        string name
        string parent_id
    }
    
    PAYMENT {
        string payment_id PK
        string order_id FK
        string method "微信/支付宝/银行卡"
        decimal amount
        string status
    }
    
    CART {
        string cart_id PK
        string user_id FK
        string product_id FK
        int quantity
    }
    
    ADDRESS {
        string address_id PK
        string user_id FK
        string receiver
        string phone
        string detail
    }
```

---

## 模板 4：用户画像 + 行为数据

```mermaid
erDiagram
    USER ||--o{ USER_PROFILE : "has"
    USER ||--o{ USER_EVENT : "generates"
    USER ||--o{ USER_SESSION : "starts"
    USER_PROFILE ||--o{ PERSONA_TAG : "labeled"
    
    USER {
        string user_id PK
        string device_id
        timestamp registered_at
    }
    
    USER_PROFILE {
        string profile_id PK
        string user_id FK
        int age
        string gender
        string city
        string occupation
    }
    
    USER_EVENT {
        string event_id PK
        string user_id FK
        string event_type "click/view/purchase"
        string target_id
        timestamp occurred_at
        json properties
    }
    
    USER_SESSION {
        string session_id PK
        string user_id FK
        timestamp started_at
        timestamp ended_at
        int duration_sec
    }
    
    PERSONA_TAG {
        string tag_id PK
        string profile_id FK
        string tag_name "新手/活跃/VIP/流失"
        string source "rule/ml/manual"
        timestamp tagged_at
    }
```

---

## 实体关系符号

| 符号 | 含义 | 示例 |
|------|------|------|
| `\|\|--\|\|` | 一对一 | 用户 - 身份证 |
| `\|\|--o{` | 一对多 | 用户 - 订单 |
| `}o--o{` | 多对多 | 学生 - 课程 |
| `\|\|--o\|` | 一对零或一 | 订单 - 发票 |

---

## 自建问题

- [ ] 实体是否清晰（不重复定义）？
- [ ] 主外键是否正确？
- [ ] 关系基数是否准确（一/多/零或一）？
- [ ] 关键字段是否标注类型和说明？
- [ ] 是否考虑了软删除（is_deleted）？

---

## 实战技巧

### 命名规范
- 表名用单数（"User" 而非 "Users"）
- 字段名小写下划线（user_id）
- 主键统一以 `_id` 结尾
- 外键 = 关联表 + `_id`

### 字段类型标注
- PK：主键
- FK：外键
- 业务字段：标注数据类型 + 含义
- 枚举值：用注释列出（如 status）

### Mermaid erDiagram 的局限
- 不支持索引
- 不支持视图、存储过程
- 复杂模型建议用工具：dbdiagram.io、MySQL Workbench、Navicat

### B 端补充
- 加 `is_deleted`（软删除）
- 加 `created_at` / `updated_at` / `created_by` / `updated_by`
- 加 `version`（乐观锁）
- 加审计相关字段
