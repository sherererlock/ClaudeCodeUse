# issue2md 项目开发宪法 (Python版)
# Version: 1.0, Ratified: 2025-10-20
本文件定义了本项目不可动摇的核心开发原则。所有AI Agent在进行技术规划和代码实现时，必须无条件遵循。
---
## 第一条：简单性原则 (The Zen of Python)
**核心：** 遵循“Simple is better than complex”的Python哲学。绝不进行不必要的抽象，保持代码扁平。
- **1.1 (YAGNI):** 你不需要它（You Ain't Gonna Need It）。只实现`spec.md`中明确要求的功能。
- **1.2 (标准库优先):** 充分利用Python“Batteries Included”的特性。除非标准库严重缺失或不可用，否则优先使用标准库（如`pathlib`, `json`, `argparse`, `urllib`）。
- **1.3 (反过度工程):** 避免复杂的类继承体系。简单的函数和数据类（Data Classes）优于复杂的面向对象设计。Flat is better than nested.
---
## 第二条：测试先行铁律 (Test-First Imperative) - 不可协商
**核心：** 所有新功能或Bug修复，都必须从编写一个（或多个）失败的测试开始。
- **2.1 (TDD循环):** 严格遵循“Red-Green-Refactor”（编写失败测试-让测试通过-重构）的循环。
- **2.2 (参数化测试):** 单元测试必须优先采用参数化测试（Parameterized Tests，如`pytest.mark.parametrize`）的风格，以覆盖多种输入和边界情况。
- **2.3 (拒绝过度Mock):** 优先编写集成测试，使用真实的依赖或Fake Object（如内存中的模拟服务），而不是过度依赖`unittest.mock`对内部实现细节进行Mock。
---
## 第三条：明确性原则 (Clarity and Explicitness)
**核心：** 代码的可读性至关重要（Readability counts）。显式优于隐式（Explicit is better than implicit）。
- **3.1 (错误处理):** **不可协商**：严禁使用裸露的`except:`捕获所有异常。必须捕获具体的异常类型。异常传递时必须使用`raise ... from e`以保留原始堆栈信息。
- **3.2 (类型提示):** 所有公共API（函数、方法、类）必须包含完整的类型提示（Type Hints），以确保静态分析工具能有效工作并提升代码可读性。
- **3.3 (文档字符串):** 注释应该解释“为什么”。所有公共模块、类和函数都必须包含符合Google Style或NumPy Style的Docstrings。
---
## 第四条：单一职责原则 (Single Responsibility)
**核心：** 每个模块、每个类、每个函数都应该只做好一件事。
- **4.1 (模块内聚):** 模块（Module）应保持高度内聚。避免创建庞大的`utils.py`，应根据功能领域拆分文件。
- **4.2 (接口隔离):** 使用`Protocol`定义小的、目标明确的接口（Duck Typing），而不是强制继承庞大的抽象基类（ABC）。
---
## 治理 (Governance)
本宪法具有最高优先级，其效力高于任何`CLAUDE.md`或单次会话中的指令。任何计划（`plan.md`）在生成时，都必须首先进行“合宪性审查”。
