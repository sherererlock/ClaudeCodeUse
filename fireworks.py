"""
烟花模拟程序 - 重构版

遵循面向对象设计原则：
- 单一职责原则：每个类只负责一项职责
- 依赖倒置原则：依赖抽象而非具体实现
- 开闭原则：对扩展开放，对修改关闭
"""
from __future__ import annotations
import tkinter as tk
import random
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Callable, Optional


# ============================================================================
# 常量定义
# ============================================================================

COLORS = ['red', 'blue', 'yellow', 'green', 'orange', 'purple', 'magenta', 'cyan', 'white']


# ============================================================================
# 数据模型层 - 纯物理实体，不依赖任何GUI框架
# ============================================================================

@dataclass
class Vector2D:
    """二维向量，用于表示位置和速度"""
    x: float
    y: float

    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> Vector2D:
        return Vector2D(self.x * scalar, self.y * scalar)

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)


@dataclass
class ParticleModel:
    """
    粒子数据模型 - 纯物理实体

    职责：管理粒子的物理状态（位置、速度、生命周期）
    """
    position: Vector2D
    velocity: Vector2D
    color: str
    life: int
    gravity: float = 0.1
    drag: float = 0.95
    size: float = 2.0

    def update(self) -> bool:
        """
        更新粒子物理状态

        Returns:
            bool: 粒子是否仍然存活
        """
        if self.life <= 0:
            return False

        # 应用速度
        self.position = self.position + self.velocity

        # 应用重力
        self.velocity.y += self.gravity

        # 应用空气阻力
        self.velocity = self.velocity * self.drag

        # 减少生命周期
        self.life -= 1

        return True


@dataclass
class FireworkModel:
    """
    烟花数据模型 - 纯物理实体

    职责：管理烟花的发射、爆炸和粒子系统
    """
    position: Vector2D
    velocity: Vector2D
    color: str
    target_height: float
    particles: List[ParticleModel] = field(default_factory=list)
    exploded: bool = False

    @classmethod
    def create_random(cls, width: int, height: int) -> FireworkModel:
        """工厂方法：创建随机参数的烟花"""
        x = random.randint(100, width - 100)
        target_y = random.randint(50, height // 2)
        launch_speed = random.uniform(8, 12)
        color = random.choice(COLORS)

        return cls(
            position=Vector2D(x, height),
            velocity=Vector2D(0, -launch_speed),
            color=color,
            target_height=target_y
        )

    def update(self) -> bool:
        """
        更新烟花状态

        Returns:
            bool: 烟花是否仍然活跃（有粒子存活或未爆炸）
        """
        if not self.exploded:
            return self._update_ascent()
        else:
            return self._update_particles()

    def _update_ascent(self) -> bool:
        """更新上升阶段"""
        # 应用速度
        self.position = self.position + self.velocity

        # 应用重力减速
        self.velocity.y += 0.2

        # 判断是否应该爆炸
        if self.position.y <= self.target_height or self.velocity.y >= 0:
            self._explode()

        return True  # 上升阶段总是活跃的

    def _update_particles(self) -> bool:
        """更新爆炸后的粒子"""
        self.particles = [p for p in self.particles if p.update()]
        return len(self.particles) > 0

    def _explode(self):
        """触发爆炸，生成粒子"""
        self.exploded = True
        num_particles = random.randint(30, 60)

        for _ in range(num_particles):
            speed = random.uniform(2, 6)
            angle = random.uniform(0, 2 * math.pi)
            velocity = Vector2D(
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )

            self.particles.append(ParticleModel(
                position=Vector2D(self.position.x, self.position.y),
                velocity=velocity,
                color=self.color,
                life=random.randint(30, 60)
            ))


# ============================================================================
# 渲染层 - 负责所有可视化操作
# ============================================================================

class Renderer(ABC):
    """渲染器抽象基类"""

    @abstractmethod
    def create_circle(self, x: float, y: float, radius: float, color: str) -> int:
        """创建圆形并返回其ID"""
        pass

    @abstractmethod
    def update_circle(self, circle_id: int, x: float, y: float, radius: float):
        """更新圆形位置"""
        pass

    @abstractmethod
    def delete(self, object_id: int):
        """删除对象"""
        pass


class TkinterRenderer(Renderer):
    """
    Tkinter 画布渲染器

    职责：将模型数据渲染到 tkinter Canvas 上
    """

    def __init__(self, canvas: tk.Canvas):
        self._canvas = canvas

    def create_circle(self, x: float, y: float, radius: float, color: str) -> int:
        return self._canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color,
            outline=""
        )

    def update_circle(self, circle_id: int, x: float, y: float, radius: float):
        self._canvas.coords(
            circle_id,
            x - radius, y - radius,
            x + radius, y + radius
        )

    def delete(self, object_id: int):
        self._canvas.delete(object_id)


class RenderEntity:
    """
    渲染实体 - 连接模型和渲染器

    职责：管理单个可视化对象的生命周期
    """

    def __init__(self, renderer: Renderer, x: float, y: float, radius: float, color: str):
        self._renderer = renderer
        self._x = x
        self._y = y
        self._radius = radius
        self._color = color
        self._id: Optional[int] = None

    def show(self):
        """在画布上显示"""
        if self._id is None:
            self._id = self._renderer.create_circle(
                self._x, self._y, self._radius, self._color
            )

    def update(self, x: float, y: float, radius: Optional[float] = None):
        """更新位置和大小"""
        self._x = x
        self._y = y
        if radius is not None:
            self._radius = radius

        if self._id is not None:
            self._renderer.update_circle(self._id, self._x, self._y, self._radius)

    def hide(self):
        """从画布上移除"""
        if self._id is not None:
            self._renderer.delete(self._id)
            self._id = None


class ParticleView:
    """
    粒子视图 - 负责粒子的渲染

    职责：将 ParticleModel 的状态可视化
    """

    def __init__(self, renderer: Renderer, model: ParticleModel):
        self._renderer = renderer
        self._model = model
        self._entity = RenderEntity(
            renderer,
            model.position.x,
            model.position.y,
            model.size,
            model.color
        )

    def update(self) -> bool:
        """
        更新粒子

        Returns:
            bool: 粒子是否仍然存活
        """
        alive = self._model.update()

        if alive:
            self._entity.update(
                self._model.position.x,
                self._model.position.y
            )
        else:
            self._entity.hide()

        return alive


class FireworkView:
    """
    烟花视图 - 负责烟花的渲染

    职责：将 FireworkModel 的状态可视化
    """

    def __init__(self, renderer: Renderer, model: FireworkModel):
        self._renderer = renderer
        self._model = model
        self._rocket_entity: Optional[RenderEntity] = None
        self._particle_views: List[ParticleView] = []

    def update(self) -> bool:
        """
        更新烟花

        Returns:
            bool: 烟花是否仍然活跃
        """
        was_exploded = self._model.exploded
        alive = self._model.update()

        # 处理爆炸时刻
        if not was_exploded and self._model.exploded:
            if self._rocket_entity:
                self._rocket_entity.hide()
                self._rocket_entity = None
            self._create_particle_views()
            return alive

        # 上升阶段
        if not self._model.exploded:
            if self._rocket_entity is None:
                self._rocket_entity = RenderEntity(
                    self._renderer,
                    self._model.position.x,
                    self._model.position.y,
                    2.0,
                    self._model.color
                )
                self._rocket_entity.show()
            else:
                self._rocket_entity.update(
                    self._model.position.x,
                    self._model.position.y
                )
        # 爆炸后阶段
        else:
            self._particle_views = [v for v in self._particle_views if v.update()]

        return alive

    def _create_particle_views(self):
        """为所有粒子创建视图"""
        for particle in self._model.particles:
            self._particle_views.append(
                ParticleView(self._renderer, particle)
            )


# ============================================================================
# 应用层 - 协调模型和视图
# ============================================================================

class FireworksController:
    """
    烟花控制器

    职责：协调模型和视图，处理用户交互
    """

    def __init__(self, renderer: Renderer, width: int, height: int):
        self._renderer = renderer
        self._width = width
        self._height = height
        self._fireworks: List[FireworkView] = []

    def launch_firework(self):
        """发射一个新的烟花"""
        model = FireworkModel.create_random(self._width, self._height)
        view = FireworkView(self._renderer, model)
        self._fireworks.append(view)

    def update(self):
        """更新所有烟花"""
        self._fireworks = [f for f in self._fireworks if f.update()]

    @property
    def firework_count(self) -> int:
        return len(self._fireworks)


class FireworksApp:
    """
    烟花应用程序主类

    职责：应用程序初始化、事件循环、用户交互
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Python 烟花小程序 (OOP重构版)")

        # 配置
        self.width = 800
        self.height = 600
        self.auto_launch_probability = 0.05
        self.frame_interval_ms = 30

        # 创建渲染层
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='black')
        self.canvas.pack()

        # 创建控制器（注入渲染器依赖）
        renderer = TkinterRenderer(self.canvas)
        self.controller = FireworksController(renderer, self.width, self.height)

        # 绑定事件
        self._bind_events()

        # 启动动画循环
        self._animate()

    def _bind_events(self):
        """绑定用户交互事件"""
        self.canvas.bind("<Button-1>", self._on_click)

    def _on_click(self, event):
        """处理鼠标点击事件"""
        self.controller.launch_firework()

    def _animate(self):
        """动画循环"""
        # 随机自动发射
        if random.random() < self.auto_launch_probability:
            self.controller.launch_firework()

        # 更新所有烟花
        self.controller.update()

        # 调度下一帧
        self.root.after(self.frame_interval_ms, self._animate)


# ============================================================================
# 程序入口
# ============================================================================

def main():
    """程序入口点"""
    root = tk.Tk()
    app = FireworksApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
