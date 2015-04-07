import asyncio
import sys

import pudb;

queue = asyncio.Queue()


class State:
    def __init__(self, name):
        self.name = name

    def run(self):
        pass


class ZeroState(State):
    def __init__(self):
        super(ZeroState, self).__init__('zero')
        
    @asyncio.coroutine
    def run(self):
        print('Running zero state')
        return FirstState()


class FirstState(State):
    def __init__(self):
        super(FirstState, self).__init__('first')

    @asyncio.coroutine
    def run(self):
        print('Running first state')
        return SecondState()


class SecondState(State):
    def __init__(self):
        super(SecondState, self).__init__('second')

    @asyncio.coroutine
    def run(self):
        print('Running second state: waiting for input...')
        text = yield from queue.get()
        print('The text is: ' + text)
        return FinalState()


class FinalState(State):
    def __init__(self):
        super(FinalState, self).__init__('final')

    @asyncio.coroutine
    def run(self):
        print('Running final state')


class StateMachine:
    @asyncio.coroutine
    def run(self):
        state = ZeroState()
        while state:
            pu.db
            state = yield from state.run()


# def _tick():
#     data = yield from queue.get()
#     print(data)
#     yield

# def tick():
#     while 1:
#         data = yield from _tick()
#         print(data)

def handle_stdin():
    data = sys.stdin.readline()
    asyncio.async(queue.put(data))

def main():
    machine = StateMachine()
    loop = asyncio.get_event_loop()
    loop.add_reader(sys.stdin, handle_stdin)
    loop.run_until_complete(machine.run())

if __name__ == '__main__':
    main()
