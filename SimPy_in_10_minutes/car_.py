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