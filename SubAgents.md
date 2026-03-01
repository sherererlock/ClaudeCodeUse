
## why subagents

### 普通agent的问题
- 注意力预算、上下文污染

### Subagent
- 上下文隔离
- 过滤噪声

## what is subagent

具有独立上下文的agent，主agent创建子agent，子agent负责特定任务，主agent只需要subagent的结果，不需要知道子agent是如何实现的

## 核心价值

- 上下文隔离
- 约束
- 复用

## when to use subagents

- 高噪声的任务，主对话只需要一个结论

- 角色边界必须非常明确的任务

- 可以并行展开的研究型任务

- 可以拆成清晰阶段的流水线式任务

## how to use subagents

### 定义subagent

Markdown + YAML frontmatter  格式
