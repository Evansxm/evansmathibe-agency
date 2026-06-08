---
name: kairos-daemon
description: Persistent background daemon for always-on proactive mode with Multi-LLM Routing, process-level isolation, governance guard, and secure credential management.
keywords: [daemon, always-on, background, tick, routing, isolation, governance, persistent, credentials]
version: 0.14-mesh
author: KAIROS-Hybrid Super-Agent v0.14-mesh
---

# KAIROS Daemon Skill

## Purpose
Persistent background daemon for true always-on proactive mode. Runs in background with periodic tick cycles, Multi-LLM Routing, full security governance, secure credential vault, and decentralized mesh synchronization.

## Architecture

### Components
1. **DaemonCore** (`kairos_daemon.py`) - Background service with tick loop.
2. **MeshManager** (`mesh_manager.py`) - **New**: Decentralized P2P synchronization and heartbeat.
3. **CredentialVault** (`skills/secure-credentials/credential_vault.py`) - Encrypted storage for secrets.
4. **MultiLLMRouter** (`skills/multi-llm-router/router.py`) - Autonomously selects optimal model and retrieves API keys from vault.
5. **GovernanceGuard** (`governance_guard.py`) - Pre-execution audit of all tasks.
6. **TickWorker** (`tick_worker.py`) - Isolated subprocess for task execution with just-in-time secret injection.

## Usage

### Mesh Networking
```bash
# Set port for local node (default 5000)
export KAIROS_MESH_PORT=5001
python3 kairos_daemon.py start

# Join a peer
python3 kairos_daemon.py mesh join 127.0.0.1:5000

# List peers and status
python3 kairos_daemon.py mesh list

# Force sync
python3 kairos_daemon.py mesh sync
```
