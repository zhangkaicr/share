# metalearner-cn 翻译规范（spec）

## 源
- 原文：https://jzhou.org/posts/metalearner/ （Meta-Learners，作者 Junyi Zhou / 周骏毅）
- 类型：单篇技术综述博客（Hugo 生成）
- 内容结构：通用框架 → 多臂处理效应估计（Q-learning: S/T-learner；A-learning: X/R/无参照组 R/de-Centralized）→ 最优治疗推荐（最优治疗策略、DTR）
- 含 1 张图（ReviewCausal_1.png）、92 个行内公式、11 个显示公式、32 条参考文献（保留英文）
- 渲染：MathJax v3（tex-mml-chtml）

## 术语约定
- CATE 条件平均处理效应；HTE 异质处理效应 / 处理效应异质性；ITE 个体处理效应
- Meta-learner 元学习器（保留英文并括注）
- Q-learning / A-learning / S-learner / T-learner / X-learner / R-learner 保留英文专名
- g-computation g-计算；g-formula g-公式；propensity score 倾向得分
- potential outcome 潜在结局；unconfoundedness 无混杂（假设）
- dynamic treatment regime (DTR) 动态治疗策略；ITR 个体化治疗规则
- SMART 序贯多分配随机试验；simplex 单纯形；Robinson decomposition Robinson 分解

## 模板
- 亮色默认 + 暗色切换（share-theme / Alt+T / 太阳月亮按钮），复用 causal-tools-cn 模板
- 必须包含 MathJax v3 配置（inlineMath 含 `\(\)`，displayMath 含 `\[\]`）
- 译文中的「背景与解释」note 框为译者所加（面向医学研究者，连接 HTE/ITR/TTE 工作），须标注非原作者观点

## 保真要求
- 所有数学公式（LaTeX）逐字保留，仅翻译周围散文
- 参考文献条目保留英文原文，但 id="ref-..." 锚点须与正文引用一一对应
- 外链（原站其他文章、GitHub、DOI）保留并新窗口打开
- 图片绝对化为 https://jzhou.org/images/...
- 不增删原文学术结论，仅补充解释性注释
