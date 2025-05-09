
from crow.commands.stages import LLToBC
from crow.entrypoints import EXPLORE_KEY, STORE_KEY, GENERATE_BC_KEY, BC2WASM_KEY, LL_KEY, SPLIT_MESSAGE, SPLIT_KEY
from crow.events import LL2BC_MESSAGE, BC2Candidates_MESSAGE, BC2WASM_MESSAGE, STORE_MESSAGE, LL_QUEUE
from crow.events.event_manager import Publisher, Subscriber, subscriber_function
from crow.settings import config
import random

import sys

from crow.monitor.monitor import log_system_exception

@log_system_exception()
def ll2bc(ll1, program_name):

    lltobc = LLToBC(program_name, debug=False)
    bc = lltobc(std=ll1)

    publisher = Publisher()

    # Call for candidates exploration

    if config["DEFAULT"].getint("split-module-in") > 0:
        publisher.publish(message=dict(
            event_type=SPLIT_MESSAGE,
            bc=bc,
            program_name=program_name
        ), routing_key=SPLIT_KEY)
    else:
        publisher.publish(message=dict(
            event_type=BC2Candidates_MESSAGE,
            bc=bc,
            program_name=program_name
        ), routing_key=EXPLORE_KEY)

    # Explicitly saving bitcode file

    if config["DEFAULT"].getboolean("keep-bc-files"):
        publisher.publish(message=dict(
            event_type=STORE_MESSAGE,
            stream=bc,
            program_name=f"{program_name}",
            file_name=f"{program_name}.bc",
            path="bitcodes"
        ), routing_key=STORE_KEY)

    if not config["DEFAULT"].getboolean("generate-bc-only") and config["DEFAULT"].getboolean("keep-wasm-files"):
        # Call for original program Wasm creation
        publisher.publish(message=dict(
            event_type=BC2WASM_MESSAGE,
            bc=bc,
            program_name=f"{program_name}",
            file_name=f"{program_name}.original"
        ), routing_key=BC2WASM_KEY)



@log_system_exception()
@subscriber_function(event_type=LL2BC_MESSAGE)
def subscriber_func(data):
    print("LL to bitcode")
    ll2bc(data["ll"], data["program_name"])


def main(files = []):

    if len(files) <= 1:
        id = f"fromll-{random.randint(0, 2000)}"
        subscriber = Subscriber(id, LL_QUEUE,LL_KEY,  config["event"].getint("port"), subscriber_func)
        subscriber.setup()
    else:
        program_name = sys.argv[1]
        program_name = program_name.split("/")[-1].split(".")[0]
        ll2bc(sys.stdin.read(), program_name)

if __name__ == "__main__":
    main(sys.argv)