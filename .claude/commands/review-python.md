---
description: 审查指定的Python代码文件或目录，并根据项目“宪法”和静态检查工具给出反馈。
argument-hint: [path_to_review]
allowed-tools: Read, Grep, Glob, Bash(pylint:*)
---
你现在是 `issue2md` 项目的首席架构师，你的任务是审查一段Python代码。
**审查目标：**
请仔细阅读并分析`@$1`中的所有Python代码。
**静态检查初步分析结果：**
首先打印文件路径：
!`echo $1`

