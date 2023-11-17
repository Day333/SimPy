# 十分钟使用SimPy
SimPy 库（一种流行的 Python 离散事件模拟框架）
## 1 下载

> pip install simpy

## 2 基础概念

这里用一个例子说明：

```python
import simpy

def car(env):
    while True:
        print('停车时间点： %d' % env.now)
        parking_duration = 5
        yield env.timeout(parking_duration)

        print('启动时间点：%d' % env.now)
        trip_duration = 2
        yield env.timeout(trip_duration)

env = simpy.Environment()
env.process(car(env))
env.run(until=15)
```

在上面的代码中，实现了这样的功能：一个汽车具有启动、停车和行进三种状态。在函数中，设定该车停车时将持续5个单位时间，行进将持续2两个时间点。 

运行代码后会看到15个单位时间内汽车的状态，结如下所示：

> 停车时间点： 0
启动时间点：5
停车时间点： 7
启动时间点：12
停车时间点： 14

## 2 进程交互

```python
import simpy

class Car(object):
    def __init__(self, env):
        self.env = env
        # 当一个实例被创建后，启动一个名为run的进程
        self.action = env.process(self.run())

    def run(self):
        while True:
            print('开始停车充电的时间点： %d' % self.env.now)
            charge_duration = 5
            yield self.env.process(self.charge(charge_duration))

            print('开始启动的时间点： %d' % self.env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)

    def charge(self, duration):
        yield self.env.timeout(duration)

env = simpy.Environment()
car = Car(env)
env.run(until=15)
```

这个 Car 类模拟了一辆在停车和充电之后行驶的车辆。以下是代码中每个部分的工作原理：

**1. 初始化（__init__ 方法）：**
- 当创建 `Car` 类的实例时，会调用此初始化方法。 
- 它接受一个 `SimPy` 环境对象 env 并将其存储在实例变量中。 
- 然后，它启动了一个名为 `run` 的过程。在 `SimPy` 中，过程是通过调用环境的 `process` 方法并传入一个生成器函数来创建的。
**2. `run` 方法：**
- 这是一个生成器方法，它使用 `while True` 无限循环来模拟车辆的周期性活动。 
- 首先打印出车辆开始停车和充电的消息，并记录当前时间。 
- `charge_duration` 变量被设置为 5，表示充电持续的时间。 
- 使用 `yield` 来等待充电过程完成，它通过调用 `charge` 方法并传入充电时长来实现。
**3. `charge` 方法：**
- 这也是一个生成器方法，它模拟了充电的过程。
- 它仅仅使环境在指定的充电时长内暂停。
**4. 行驶过程：**
- 一旦充电完成，会打印出开始行驶的消息，并记录当前时间。
- `trip_duration` 变量被设置为 2，表示行驶的时间。
- 使用 `yield self.env.timeout(trip_duration)` 来使环境在行驶时长内暂停。

## 3 资源分享

```python
import simpy


def car(env, name, bcs, driving_time, charge_duration):
    # 模拟行驶到电车充电站
    yield env.timeout(driving_time)

    # 请求一个充电点
    print('%s 到达在时间点 %d' % (name, env.now))
    with bcs.request() as req:
        yield req

        # 充电付费
        print('%s 开始充电在时间点： %s' % (name, env.now))
        yield env.timeout(charge_duration)
        print('%s 离开充电站在时间点： %s' % (name, env.now))

env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2)

for i in range(4):
    env.process(car(env, 'Car %d' % i, bcs, i*2, 5))

env.run()
```

模拟了四辆车在一个电车充电站进行充电的过程。下面是代码的详细解释：

1. `car` 函数：
这个函数代表每辆车的行为模式。
- `env` 是 `SimPy` 环境对象。
- `name` 是车辆的名称。
- `bcs` 代表充电站资源。
- `driving_time` 是车辆驾驶到充电站的时间。
- `charge_duration` 是车辆充电所需的时间。
2. 模拟行驶：
- 使用 `env.timeout(driving_time)`来模拟每辆车行驶到充电站的时间。
- 到达充电站并请求充电点： 
  - 当车辆到达充电站时，会打印它的到达时间。
  - 使用 `bcs.request()` 来请求一个充电点。这是一个资源请求，其中 `bcs` 是一个有限容量的资源（充电站）。
3. 充电过程：
- 一旦获得充电点，车辆开始充电，并打印开始充电的时间。
- 使用 `env.timeout(charge_duration)` 来模拟充电所需的时间。
- 充电完成后，打印车辆离开充电站的时间。
4. 创建环境和充电站资源： 
- 创建一个 `SimPy` 环境 `env`。
- 创建一个充电站资源 `bcs`，它是一个有两个充电点的资源`（capacity=2）`。
5. 创建并运行车辆进程： 
- 对于四辆车，使用循环创建并启动它们的 `SimPy` 过程。
- 每辆车的行驶时间递增`（i*2）`，而充电时间对所有车辆都是相同的（5个时间单位）。 
6. 运行模拟：
- 使用 `env.run()` 启动并运行模拟。

运行结果：
> Car 0 到达在时间点 0
Car 0 开始充电在时间点： 0
Car 1 到达在时间点 2
Car 1 开始充电在时间点： 2
Car 2 到达在时间点 4
Car 0 离开充电站在时间点： 5
Car 2 开始充电在时间点： 5
Car 3 到达在时间点 6
Car 1 离开充电站在时间点： 7
Car 3 开始充电在时间点： 7
Car 2 离开充电站在时间点： 10
Car 3 离开充电站在时间点： 12