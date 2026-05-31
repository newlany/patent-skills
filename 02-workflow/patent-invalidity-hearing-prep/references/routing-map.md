# 无效案件路由表

对外只保留 `patent-invalidity-hearing-prep` 这一个公开 skill。

## 路由规则

- 用户要“无效过程梳理”“案卷梳理”“程序时间线”“攻击框架变化”
  - 进入 case-sorting mode
  - 读取 `case-sorting.md` 和 `case-sorting-prompts.md`
- 用户要“口审准备”“开庭陈述”“正式抗辩”“请求人可能观点”“审查员追问”“总结陈述”
  - 进入 hearing-prep mode
  - 读取 `prompt-templates.md`
- 用户要完整准备
  - 先梳理案卷，再进入口审准备

## 约束

- 如果案卷整理还没做，不要直接开始正式抗辩稿。
- 一定区分原权利要求和修改后权利要求。
