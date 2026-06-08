#!/usr/bin/env python3
"""
KAIROS Tick Worker v0.11
Isolated subprocess worker with model awareness.
"""

import sys
import os
import resource
import time

def set_limits(cpu_timeout=10, mem_limit_mb=512):
    """Set process resource limits (Linux only)."""
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_timeout, cpu_timeout + 1))
        mem_limit = mem_limit_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (mem_limit, mem_limit))
    except (ValueError, ImportError, OSError):
        pass

def main():
    if len(sys.argv) < 2:
        print("Usage: tick_worker.py <task_description> [model]")
        sys.exit(1)

    task = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "default"
    
    # Set resource limits
    set_limits(cpu_timeout=10, mem_limit_mb=256)

    print(f"Worker starting task: {task[:50]} using model: {model}")
    
    try:
        if "simulate high cpu" in task.lower():
            while True: pass
        
        elif "simulate high memory" in task.lower():
            data = [" " * (1024 * 1024)] * 1000
            
        elif "summarize" in task.lower() or "analyze" in task.lower() or "check" in task.lower() or "date" in task.lower():
            time.sleep(1)
            print(f"Worker processed task: {task[:50]} (Model: {model})")
            sys.exit(0)

        else:
            time.sleep(1)
            print(f"Worker finished task: {task[:50]}")
            sys.exit(0)
            
    except MemoryError:
        print("Worker caught MemoryError!", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Worker error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
