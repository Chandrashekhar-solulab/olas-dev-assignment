import threading
import time
from agent.Agent import agent_1, agent_2

# global stop event
stop_event = threading.Event()

def main():
    # Start both agents threads
    thread_1 = threading.Thread(target=agent_1, args=(stop_event,))
    thread_2 = threading.Thread(target=agent_2, args=(stop_event,))

    thread_1.start()
    thread_2.start()

    try:
      
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Stopping agents...")
        stop_event.set()
    except Exception as e:
        print(f"Unexpected error: {e}")
        stop_event.set()
    finally:
        
        print("Ensuring threads are stopped.")
        try:
            thread_1.join(timeout=5)
            thread_2.join(timeout=5)
            if thread_1.is_alive() or thread_2.is_alive():
                print("Forcing threads to stop.")
        except Exception as join_exception:
            print(f"Error stopping threads: {join_exception}")

        print("Agents stopped successfully.")

if __name__ == "__main__":
    main()
