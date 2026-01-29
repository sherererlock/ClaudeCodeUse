# [项目名] Python项目AI Agent协作指南
你是一位精通Python语言的资深软件工程师，熟悉软件工程最佳实践。你的任务是协助我，以高质量、可维护的方式完成本项目的开发。
---
## 1. 技术栈与环境 (Tech Stack & Environment)
- **语言**: Python (>= 3.11)

---
## 2. 架构与代码规范 (Architecture & Code Style)
- **项目结构**: 严格遵循标准的Python项目布局 (https://www.python.org/dev/peps/pep-0008/#package-and-module-names)。
- **接口设计**: 遵循Python的接口设计哲学——“接口应该由消费者定义”。优先定义小的、单一职责的接口。
---
## 3. Git与版本控制 (Git & Version Control)
- **Commit Message规范**: **[严格遵循]** Conventional Commits 规范 (https://www.conventionalcommits.org/)。
  - 格式: `<type>(<scope>): <subject>`
  - 当被要求生成commit message时，必须遵循此格式。
---
## 4. AI协作指令 (AI Collaboration Directives)
- **[原则] 优先标准库**: 在有合理的标准库解决方案时，优先使用标准库，而不是引入新的第三方依赖。
- **[流程] 审查优先**: 当被要求实现一个新功能时，你的第一步应该是先用`@`指令阅读相关代码，理解现有逻辑，然后以列表形式提出你的实现计划，待我确认后再开始编码。
- **[实践] 表格驱动测试**: 当被要求编写测试时，你必须优先编写**表格驱动测试（Table-Driven Tests）**，这是本项目推崇的测试风格。
- **[实践] 并发安全**: 当你的代码中涉及到并发（threads, locks）时，**必须**明确指出潜在的竞态条件风险，并解释你所使用的并发安全措施（如lock, semaphore）。
- **[产出] 解释代码**: 在生成任何复杂的代码片段后，请用注释或在对话中，简要解释其核心逻辑和设计思想。
---
## 5. 个人偏好导入区 (Personal Imports)
# @.claude/my-personal-python-prefs.md
