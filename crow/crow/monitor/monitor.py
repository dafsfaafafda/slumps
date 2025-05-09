from crow.events import LOG_MESSAGE, GENERATED_BC_VARIANT, EXPLORATION_RESULT
from crow.monitor.logger import ERROR
from crow.events.event_manager import Subscriber, subscriber_function, Publisher
import traceback
from crow.settings import config
from crow.monitor import MONITOR_QUEUE_NAME
from crow.utils import printProgressBar
import random

def log_system_exception():

    def Inner(func):

        def wrapper(*args, **kwargs):

            try:
                r = func(*args, **kwargs)
                return r
            except Exception as e:
                trace = traceback.format_exc()
                p = Publisher()

                p.publish(message=dict(
                    event_type=LOG_MESSAGE,
                    exception=f"{e} {trace}",
                    severity=ERROR
                ),
                routing_key="")

                print(f"{e} {trace}")

        return wrapper

    return Inner


# Monitor status
COUNT = 0
TENTATIVE_NUMBER = -1
HASHES = []

@subscriber_function(event_type="*")
def general_log(data):
    global COUNT
    global TENTATIVE_NUMBER
    global HASHES

    if data["event_type"] == GENERATED_BC_VARIANT:
        COUNT += 1
        HASHES.append(data["hash"])
        #if TENTATIVE_NUMBER == -1: # WARNING something happend with the exploration service
        #    print(f"WARNING something happend with the exploration service. Count: {COUNT}")
        #else:
        #printProgressBar(COUNT, TENTATIVE_NUMBER if TENTATIVE_NUMBER > -1 else COUNT, suffix=f"{COUNT}/{TENTATIVE_NUMBER}")
        print(f"{COUNT}/{TENTATIVE_NUMBER} UNIQUENESS BITCODE_LEVEL {len(set(HASHES))}/{len(HASHES)}")
    if data["event_type"] == EXPLORATION_RESULT:
        TENTATIVE_NUMBER = data["tentative_number"]

if __name__ == "__main__":
    id = f"monitor-{random.randint(0,2000)}"

    subscriber = Subscriber(1, MONITOR_QUEUE_NAME, config["event"].getint("port"), general_log)
    subscriber.setup()