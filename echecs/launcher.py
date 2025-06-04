import subprocess, multiprocessing, time
import server, client

def start_cli():
    subprocess.run(
        [
            "/bin/python",
            client.__file__,
            f"localhost:{server.PORT}"
        ]
    )

def main() -> None:
    t1 = multiprocessing.Process(target=server.main)
    t2 = multiprocessing.Process(target=start_cli)
    t3 = multiprocessing.Process(target=start_cli)
    t1.start()
    time.sleep(0.1)
    t2.start()
    t3.start()
    t2.join()
    t3.join()
    t1.terminate()
    print("Server closed!")

if __name__ == "__main__":
    main()