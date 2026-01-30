import tkinter as tk
import random
import math

# 颜色列表，用于烟花爆炸时的随机颜色
COLORS = ['red', 'blue', 'yellow', 'green', 'orange', 'purple', 'magenta', 'cyan', 'white']

class Particle:
    """
    表示烟花爆炸后的单个火花点。
    """
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        # 随机生成初始速度和方向
        speed = random.uniform(2, 6)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        # 重力加速度
        self.gravity = 0.1
        # 阻力系数
        self.drag = 0.95
        # 生命周期（剩余帧数）
        self.life = random.randint(30, 60)
        # 在画布上创建小球
        self.id = self.canvas.create_oval(x-2, y-2, x+2, y+2, fill=color, outline="")

    def update(self):
        """
        更新火花的位置和生命状态。
        """
        if self.life > 0:
            # 应用速度和重力
            self.x += self.vx
            self.y += self.vy
            self.vy += self.gravity
            # 应用空气阻力
            self.vx *= self.drag
            self.vy *= self.drag
            
            # 更新画布上的位置
            self.canvas.coords(self.id, self.x-2, self.y-2, self.x+2, self.y+2)
            
            # 随生命值减少而逐渐变淡（这里简单处理为缩小或改变透明度，tkinter对透明度支持较差，我们直接减少生命）
            self.life -= 1
            return True
        else:
            # 生命周期结束，从画布删除
            self.canvas.delete(self.id)
            return False

class Firework:
    """
    表示整个烟花：从发射到爆炸。
    """
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        # 初始发射位置（底部随机位置）
        self.x = random.randint(100, width - 100)
        self.y = height
        # 发射目标高度
        self.target_y = random.randint(50, height // 2)
        # 发射速度
        self.vy = -random.uniform(8, 12)
        self.color = random.choice(COLORS)
        # 是否已经爆炸
        self.exploded = False
        self.particles = []
        # 发射时的小圆点
        self.id = self.canvas.create_oval(self.x-2, self.y-2, self.x+2, self.y+2, fill=self.color, outline="")

    def update(self):
        """
        更新烟花状态。
        """
        if not self.exploded:
            # 还在上升阶段
            self.y += self.vy
            self.canvas.coords(self.id, self.x-2, self.y-2, self.x+2, self.y+2)
            
            # 到达目标高度或速度降为0时爆炸
            if self.y <= self.target_y or self.vy >= 0:
                self.explode()
            else:
                self.vy += 0.2 # 模拟重力减速
            return True
        else:
            # 爆炸后更新所有火花
            self.particles = [p for p in self.particles if p.update()]
            return len(self.particles) > 0

    def explode(self):
        """
        产生爆炸效果。
        """
        self.exploded = True
        self.canvas.delete(self.id)
        # 生成数十个火花粒子
        num_particles = random.randint(30, 60)
        for _ in range(num_particles):
            self.particles.append(Particle(self.canvas, self.x, self.y, self.color))

class FireworksApp:
    """
    烟花程序主类。
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Python 烟花小程序")
        self.width = 800
        self.height = 600
        
        # 创建画布
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='black')
        self.canvas.pack()
        
        self.fireworks = []
        self.animate()
        
        # 绑定点击事件，点击屏幕也可以发射烟花
        self.canvas.bind("<Button-1>", self.launch_firework)

    def launch_firework(self, event=None):
        """
        手动或自动发射烟花。
        """
        self.fireworks.append(Firework(self.canvas, self.width, self.height))

    def animate(self):
        """
        主循环动画。
        """
        # 随机概率自动发射烟花
        if random.random() < 0.05:
            self.launch_firework()
            
        # 更新所有烟花状态
        self.fireworks = [f for f in self.fireworks if f.update()]
        
        # 30毫秒后再次调用，形成动画
        self.root.after(30, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = FireworksApp(root)
    root.mainloop()
