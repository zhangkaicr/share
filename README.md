# Share

因果推断 / 目标试验模拟（TTE）/ 临床研究方法的公开课讲义与代码复现物料。

在线访问：**https://zhangkaicr.github.io/share/**

## 目录

| 路径 | 内容 |
|---|---|
| [`policytree-cn/`](policytree-cn/) | 《policytree：从因果森林学到最优策略树》—— policytree 官方 vignette 中文译本（含示例 1–3、运行时间基准、混合搜索、术语对照），暗色主题 |
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

## hte-course 简介

以一篇严重钝性创伤输血研究（FFP:RBC 比值，*Critical Care* 2025;29:436）为主线，讲清楚一件事：

> 全体患者的平均效应是 −3.3%，但当人群被切到「乳酸 ≥ 4.5 且 GCS ≤ 12」这个角落时，效应是 −13.3%，NNT 只有 7.5。

方法链条：**亚组分析 → IPTW + 聚类稳健标准误 → NNT → 因果森林估计个体 CATE → 3×3 热图定位治疗靶点 → 敏感性分析**。

讲义特点：

- 单文件 HTML，16 张图片以 base64 内嵌，**离线双击可用**，可直接发给学生
- 原文 Fig.1–4 高清图（开放获取）与其 R 复现图并列对照
- Table 1 / Table 2 为原生 HTML 表格，可搜索可复制
- 含 3 处课堂辩论材料：摘要与 Table 2 的 NNT 不一致、靶点切点的就近取整、局限中的永恒时间偏倚

## 本地重新构建

讲义由模板 + 图片构建而成，替换 `assets/` 里的图片后重新生成即可：

```bash
cd hte-course
python build.py      # 读 course_template.html + assets/，输出 index.html
```

复现代码主体（10 段 R 脚本）在配套的 R 项目目录中，非本仓库收录范围。

## 声明

各译文均已注明原文出处、作者与许可：imputeTS 源自 The R Journal（CC BY 4.0），policytree 源自该包官方 vignette，HTE 讲义中的论文图表取自开放获取文献（CC BY）。所有复现图表由本地 R 流水线生成。模拟数据仅用于教学，不代表真实临床结论。
