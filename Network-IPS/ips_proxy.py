# ips_proxy.py
import asyncio, re, time, argparse
SQLI_RE = re.compile(rb"(union\s+select|'or'|'1'='1|-- |/\*|\bselect\b.*\bfrom\b)", re.IGNORECASE)
CONN_LIMIT = 50
WINDOW = 60
clients = {}

async def handle_client(reader, writer, backend_host, backend_port):
    peer = writer.get_extra_info('peername')
    client_ip = peer[0] if peer else 'unknown'
    now = time.time()
    timestamps = clients.get(client_ip, [])
    timestamps = [t for t in timestamps if now - t < WINDOW]
    if len(timestamps) >= CONN_LIMIT:
        print(f"Rate limit: blocking {client_ip}")
        writer.close(); await writer.wait_closed(); return
    timestamps.append(now)
    clients[client_ip] = timestamps
    try:
        backend_reader, backend_writer = await asyncio.open_connection(backend_host, backend_port)
    except Exception as e:
        writer.close(); await writer.wait_closed(); return

    async def pipe(src_reader, dst_writer, inspect=False):
        try:
            while True:
                data = await src_reader.read(4096)
                if not data:
                    break
                if inspect and SQLI_RE.search(data):
                    print(f"SQLi detected from {client_ip}; dropping connection")
                    return False
                dst_writer.write(data)
                await dst_writer.drain()
            return True
        except:
            return True

    task1 = asyncio.create_task(pipe(reader, backend_writer, inspect=True))
    task2 = asyncio.create_task(pipe(backend_reader, writer, inspect=False))
    done, pending = await asyncio.wait([task1, task2], return_when=asyncio.FIRST_COMPLETED)
    for t in pending: t.cancel()
    backend_writer.close(); writer.close()
    await backend_writer.wait_closed(); await writer.wait_closed()

async def main(listen_host, listen_port, backend_host, backend_port):
    server = await asyncio.start_server(lambda r,w: handle_client(r,w,backend_host,backend_port), listen_host, listen_port)
    print(f"Proxy listening on {listen_host}:{listen_port}, forwarding to {backend_host}:{backend_port}")
    async with server:
        await server.serve_forever()

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--listen','-l',default='127.0.0.1:8080')
    parser.add_argument('--backend','-b',default='127.0.0.1:80')
    args=parser.parse_args()
    lh,lp = args.listen.split(':'); bh,bp = args.backend.split(':')
    asyncio.run(main(lh,int(lp),bh,int(bp)))
