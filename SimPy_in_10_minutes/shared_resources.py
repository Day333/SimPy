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
