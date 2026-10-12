# Share

因果推断 / 目标试验模拟（TTE）/ 临床研究方法的公开课讲义与代码复现物料。

在线访问：**https://zhangkaicr.github.io/share/**

## 目录

| 路径 | 内容 |
|---|---|
| [`policytree-cn/`](policytree-cn/) | 《policytree：从因果森林学到最优策略树》—— policytree 官方 vignette 中文译本（含示例 1–3、运行时间基准、混合搜索、术语对照），暗色主题 |
| [`grf-cn/`](grf-cn/) | 《grf 中文教程》—— grf 官网 12 篇教程全译（入门 / 方法导论 / 诊断 / 条件均值 / 生存 / ATE 迁移 / RATE 异质性 / 策略学习 / 局部线性森林 / Qini / 类别变量 / RATE-CV），每篇补充「背景与解释」框，明暗可切换 |
| [`evalITR-cn/`](evalITR-cn/) | 《evalITR 中文教程》—— evalITR 官网 8 篇文档全译（总览 / 安装 / 样本分割 / Caret·SuperLearner 样本分割 / 用户自定义 ITR / 规则比较 / 单一·多种算法交叉验证），核心指标 PAPE·AUPEC·GATEs，每篇补充「背景与解释」框，明暗可切换 |
| [`causal-tools-cn/`](causal-tools-cn/) | 《因果推断的三件工具》—— Harsha Kokel 博客《Tools for Causal Inference》中文译本，梳理 Pearl 的因果推断三件基础工具（DAG / do-算符 / 反事实），含公式与图示，补充「背景与解释」框衔接 HTE，明暗可切换 |
| [`model4you-cn/`](model4you-cn/) | 《model4you：个体化治疗效应估计的 R 包》—— JORS 2019 文章中文译本，模型树 + 个体化模型两件套 |
| [`hte-course/`](hte-course/) | 公开课《平均值的谎言：谁真正受益？》—— 异质性治疗效应（HTE）完整讲义 + 10 段 R 复现脚本索引 |
| `index.html` | 站点导航首页 |

每个子项目自成一个文件夹，互不干扰，用 GitHub Pages 发布后可独立访问。

## policytree-cn 简介

policytree 官方 vignette 的中文译本。承接本仓库 HTE 主题的下游问题：**算出 CATE 之后怎么办**——把个体化效应转成一条可执行的决策规则。

流水线：`grf` 拟合森林 → `double_robust_scores()` 得到 Γ 矩阵（每个人 × 每个行动的收益估计）→ `policy_tree()` 精确搜索全局最优浅树 → `predict()` 部署到新样本。

覆盖二元处置、三行动多臂、工具变量三种设定，并给出运行时间基准表（含 `split.step` 与 `round(X, 2)` 降基数的加速对比）和 `hybrid_policy_tree` 混合搜索的取舍。

## model4you-cn 简介

JORS 2019 文章的中文译本，主题与 hte-course 一脉相承：**当"所有人共享一个效应"的假定过于严格时怎么办**。它给出的路径很轻——不必换模型，直接把熟悉的 `lm()` / `glm()` / 生存模型塞进 `pmtree()`（分层树）或 `pmforest()` + `pmodel()`（个体化模型）。

示例（奥地利数学考试数据）很有教学价值：总体 −2.33 个百分比且不显著，但树切出的高分学生亚组是 −13.26。

## imputeTS-cn 简介

The R Journal 2017 文章的全文中文译本。核心问题：多重填补、EM、最近邻、热卡等主流方法依赖变量间相关性，单变量时间序列只有一个属性因而无法直接使用，必须转向时间维度的依赖。

## grf-cn 简介

grf（Generalized Random Forests，广义随机森林）官方站点 12 篇教程的中文全译本，是本站 HTE 主题的方法学底座。覆盖：

- **入门与方法论**：`grf`（速览）、`grf_guide`（正交化 / 标签权重 / 诚实估计的方法论文档）
- **诊断与异质性检验**：`diagnostics`（重叠性、协变量平衡）、`muhats`（回归森林与条件均值）、`rate` / `rate_cv`（RATE 与交叉验证判断异质性是否真实）
- **专门森林**：`survival`（右删失、RMST、因果生存森林）、`llf`（局部线性森林）
- **迁移、策略与扩展**：`ate_transport`（把 ATE 加权到新目标人群）、`policy_learning`（从 CATE 到最优决策树，衔接 policytree）、`maq`（Qini 曲线 / Uplift）、`categorical_inputs`（因子变量编码）

每篇都在关键概念处加了「背景与解释」框，专门面向医学研究者补充处理效应异质性、双稳健、删失、外部效度等铺垫。公式由 MathJax 渲染，右上角按钮可切换明暗主题。原文依 MIT 许可翻译并注明出处。

## evalITR-cn 简介

evalITR（评估个体化治疗规则，Individualized Treatment Rules）官方文档 8 篇的中文全译本，紧跟 grf-cn / policytree-cn 的脉络：**估计出 CATE 之后，如何真正评估"按规则分配治疗"比"千人一方"好多少**。

覆盖：

- **入门**：`overview`（包总览，PAPE / AUPEC / GATEs 指标与 Imai & Li 方法出处）、`install`（CRAN / GitHub 安装）
- **核心方法**：`sample_split`（为什么必须把训练与评估分两批数据以防乐观偏差）、`sample_split_caret`（用 caret / SuperLearner 拟合 ITR）、`user_itr`（用户自定义规则函数）、`user_itr_algs`（估计规则 vs 专家规则，AUPEC 曲线与模型摘要怎么读）
- **交叉验证评估**：`cv_single_alg`（K 折为何关键，如何得无偏 AUPEC）、`cv_multiple_alg`（多 ML 算法比较与模型选择）

每篇在关键概念处加「背景与解释」框，专门面向医学研究者补充 ITR 与 ATE 的区别、样本分割 / 交叉验证为何必要、预算约束与 AUPEC 的临床意义等。右上角按钮可切换明暗主题。原文依开源许可翻译并注明出处（源代码 github.com/MichaelLLi/evalITR）。

## causal-tools-cn 简介

Harsha Kokel 博客文章《Tools for Causal Inference》的中文译本，是对 Judea Pearl《因果推断的七件工具》与《为什么》一书的通俗梳理，正好补齐本站方法学底座的"概念入口"：

- **工具一**：用有向无环图（DAG / 贝叶斯网络）编码因果假设，并点明 $P(y \mid X)$ 与 $P(y \mid do(X))$ 的本质区别
- **工具二**：do-算符（do-calculus）与混杂控制——后门准则（去混杂）与前门准则（绕开不可观测混杂），含前门公式推导
- **工具三**：反事实的算法化——结构方程模型（SEM）+ 三步算法（溯因 / 干预 / 预测），用"Alice 的薪水"实例演示

站点内的「背景与解释」框专门面向医学研究者，把 DAG 条件独立性、后门 / 前门与流行病学混杂控制、反事实与个体化治疗（HTE / ITR）逐一衔接。公式由 MathJax 渲染，右上角按钮可切换明暗主题。原文依原站许可转载翻译并注明出处（harshakokel.com）。

## hte-course 简介

以一篇严重钝性创伤输血研究（FFP:RBC 比值，*Critical Care* 2025;29:436）为主线，讲清楚一件事：

> 全体患者的平均效应是 −3.3%，但当人群被切到「乳酸 ≥ 4.5 且 GCS ≤ 12」这个角落时，效应是 −13.3%，NNT 只有 7.5。

方法链条：**亚组分析 → IPTW + 聚类稳健标准误 → NNT → 因果森林估计个体 CATE → 3×3 热图定位治疗靶点 → 敏感性分析**。

讲义特点：

- 单文件 HTML，16 张图片以 base64 内嵌，**离线双击可用**，可直接发给学生
- 原文 Fig.1–4 高清图（开放获取）与其 R 复现图并列对照
- Table 1 / Table 2 为原生 HTML 表格，可搜索可复制
- 含 3 处课堂辩论材料：摘要与 Table 2 的 NNT 不一致、靶点切点的就近取整、局限中的永恒时间偏倚

## 新增页面时补上主题切换

全站共用一套明暗主题切换（右上角圆形按钮 / Alt+T，偏好存 `localStorage["share-theme"]`，跨页面共享）。
新建页面后跑一次即可注入（幂等，已有按钮会跳过）：

```bash
python _tools/add_theme.py <新页面.html> light   # 或 dark 作为该页默认
```

## 本地重新构建

讲义由模板 + 图片构建而成，替换 `assets/` 里的图片后重新生成即可：

```bash
cd hte-course
python build.py      # 读 course_template.html + assets/，输出 index.html
```

复现代码主体（10 段 R 脚本）在配套的 R 项目目录中，非本仓库收录范围。

## 声明

各译文均已注明原文出处、作者与许可：imputeTS 源自 The R Journal（CC BY 4.0），policytree 源自该包官方 vignette，HTE 讲义中的论文图表取自开放获取文献（CC BY）。所有复现图表由本地 R 流水线生成。模拟数据仅用于教学，不代表真实临床结论。
