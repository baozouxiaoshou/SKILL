# 甘特图模板（Gantt Chart）

> 项目计划、Sprint 排期

---

## 模板 1：单 Sprint 计划

```mermaid
gantt
    title 健身 App MVP - Sprint 1
    dateFormat YYYY-MM-DD
    axisFormat %m/%d
    
    section 引导流程
    问卷设计      :a1, 2026-10-13, 2d
    问卷开发      :a2, after a1, 3d
    
    section 计划生成
    规则引擎      :b1, 2026-10-15, 2d
    API 开发      :b2, after b1, 2d
    前端展示      :b3, after b2, 2d
    
    section 推荐系统
    推荐算法      :c1, 2026-10-18, 3d
    集成测试      :c2, after c3, 2d
    
    section 测试上线
    QA 测试       :d1, 2026-10-22, 3d
    Bug 修复      :d2, after d1, 2d
    灰度发布      :d3, after d2, 1d
```

---

## 模板 2：多 Sprint 路线图

```mermaid
gantt
    title RAS 双语录入 - 项目计划
    dateFormat YYYY-MM-DD
    
    section Sprint 1: MVP
    需求澄清      :s1a, 2026-10-13, 1d
    翻译引擎接入  :s2a, after s1a, 3d
    关键字段录入  :s3a, after s2a, 3d
    双语展示      :s4a, after s3a, 2d
    集成测试      :s5a, after s4a, 2d
    
    section Sprint 2: 完善
    勘误功能      :s1b, after s5a, 3d
    术语库后台    :s2b, after s1b, 2d
    版本快照      :s3b, after s2b, 3d
    UAT          :s4b, after s3b, 2d
    
    section Sprint 3: 扩展
    批量翻译      :s1c, after s4b, 3d
    多语言扩展    :s2c, after s1c, 3d
    数据脱敏      :s3c, after s2c, 2d
    全面上线      :s4c, after s3c, 2d
```

---

## 模板 3：含里程碑

```mermaid
gantt
    title 产品发布路线图
    dateFormat YYYY-MM-DD
    
    section 准备
    内测        :active, des1, 2026-10-13, 14d
    
    section 灰度
    5% 流量     :des2, after des1, 3d
    20% 流量    :des3, after des2, 3d
    50% 流量    :des4, after des3, 4d
    
    section 全量
    100% 流量   :des5, after des4, 5d
    
    section 里程碑
    内测完成    :milestone, m1, 2026-10-27, 0d
    灰度完成    :milestone, m2, after des4, 0d
    全量发布    :milestone, m3, after des5, 0d
```

---

## 模板 4：含依赖关系

```mermaid
gantt
    title 跨团队协作项目
    dateFormat YYYY-MM-DD
    
    section 设计
    UI 设计      :ds, 2026-10-13, 3d
    
    section 后端
    API 设计     :be1, 2026-10-13, 2d
    DB 设计      :be2, after be1, 1d
    API 开发     :be3, after be2, 5d
    
    section 前端
    前端开发     :fe1, after ds, 5d
    
    section 联调
    后端联调     :it1, after be3, 3d
    集成测试     :it2, after fe1, 2d
    
    section 发布
    预发环境     :rel1, after it2, 1d
    灰度发布     :rel2, after rel1, 2d
```

---

## 甘特图语法

### 任务定义
```
任务名 : 任务ID, 开始日期, 持续天数
任务名 : 任务ID, after 任务ID, 持续天数
```

### 任务状态
- 关键任务：`crit, 任务ID, ...`
- 当前进行：`active, 任务ID, ...`
- 已完成：`done, 任务ID, ...`

### 里程碑
```
里程碑名 :milestone, m1, 2026-10-27, 0d
```

### 分组
```
section 章节名
  任务 : 任务ID, ...
```

---

## 自检问题
- [ ] 任务粒度是否合适（1-5 天）？
- [ ] 任务依赖是否清晰？
- [ ] 关键路径是否标注？
- [ ] 里程碑是否齐全？
- [ ] 是否有 buffer 时间（应对延期）？
