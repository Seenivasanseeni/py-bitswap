import asyncio
import sys
from libp2p import new_node


async def read_data(stream):
    while True:
        read_string = await stream.read()
        if read_string is not None:
            read_string = read_string.decode()
            if read_string != "\n":
                # Green console colour: 	\x1b[32m
                # Reset console colour: 	\x1b[0m
                print("\n\x1b[32m %s\x1b[0m " % read_string, end="")


async def write_data(stream):
    loop = asyncio.get_event_loop()
    while True:
        line = await loop.run_in_executor(None, sys.stdin.readline)
        await stream.write(line.encode())


async def run(port):
    host = await new_node(transport_opt=["/ip4/127.0.0.1/tcp/%s" % port])

    async def stream_handler(stream):
        asyncio.ensure_future(read_data(stream))
        asyncio.ensure_future(write_data(stream))

    host.set_stream_handler(PROTOCOL_ID, stream_handler)

    port = None
    for listener in host.network.listeners.values():
        for addr in listener.get_addrs():
            port = int(addr.value_for_protocol('tcp'))

    if not port:
        raise RuntimeError("was not able to find the actual local port")
    print("Destination to connect:", f"/ip4/127.0.0.1/tcp/{port}/p2p/{host.get_id().pretty()}")
    print("You can replace 127.0.0.1 with public IP as well.")
    print("\nWaiting for incoming connection\n\n")


def main(port):
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(run(port))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


if __name__ == '__main__':
    PROTOCOL_ID = '/chat/1.0.0'
    port = 9001
    main(port)
