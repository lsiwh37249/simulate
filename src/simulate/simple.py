import simpy
from datetime import datetime
import time
import random
# 고객 클래스

class Customer:
    def __init__(self, name):
        self.name = name

    def log_event(self, event, current_time,):
        """로그 메시지를 통일된 형식으로 출력하는 함수"""
        print(f"[{current_time}] {self.name} {event}")

    def shop(self, env, cashier):
        # 고객이 들어오는 시간
        self.log_event("entered the shop", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # 계산원과 대기 후 상호작용하는 시간
        with cashier.request() as req:
            yield req
            self.log_event("started talking to the cashier", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            # 계산 과정 (SimPy timeout으로 계산 시간 모사)
            yield env.timeout(2)  # 계산에 2시간 소요
            self.log_event("completed the payment", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # 가게에서 나가는 시간
        self.log_event("left the shop", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# 시뮬레이션 환경 및 계산원 설정
def coffee_shop_simulation(env, num_cashiers):
    # 계산원 리소스 생성 (여러 계산원이 있을 수 있음)
    cashier = simpy.Resource(env, capacity=num_cashiers)
    # 5명의 손님 생성
    random_value = random.randint(150, 170)

    customers = [Customer(f"Customer{i}") for i in range(random_value)]
    
    for customer in customers:
        # 각 손님을 일정 시간마다 가게에 들어오게 설정
        env.process(customer.shop(env, cashier))
        yield env.timeout(3)  # 손님 간에 3분 간격

# 시뮬레이션 실행
env = simpy.Environment()
env.process(coffee_shop_simulation(env, num_cashiers=1))  # 계산원 1명
env.run(until=1000)  # 시뮬레이션 10분 실행
