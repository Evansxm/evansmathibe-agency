# MCP_SERVER.md - Multi-Agent Control Protocol

## Agent State
- **Status:** Active
- **Version:** 2.1.88
- **Mode:** Claude Code + OpenClaw Hybrid + KAIROS Daemon
- **Last Updated:** 2026-04-04

## Available Skills

| Skill | Path | Status | Version |
|-------|------|--------|---------|
| master-agent | ./skills/master-agent/ | Ready | 1.0.0 |
| web-research | ./skills/web-research/ | Ready | 1.0.0 |
| github-orchestrator | ./skills/github-orchestrator/ | Ready | 1.0.0 |
| terminal-master | ./skills/terminal-master/ | Ready | 1.0.0 |
| multi-agent-orchestrator | ./skills/multi-agent-orchestrator/ | Ready | 1.0.0 |
| self-improvement | ./skills/self-improvement/ | Ready | 1.0.0 |
| token-manager | ./skills/token-manager/ | Ready | 1.0.0 |
| computer-use-sim | ./skills/computer-use-sim/ | Ready | 1.0.0 |
| universal-research-agent | ./skills/universal-research-agent/ | Ready | 0.2.0 |
| research-orchestrator | ./skills/research-orchestrator/ | Ready | 1.0.0 |
| kairos-core | ./skills/kairos-core/ | Ready | 0.4.0 |
| memory-bank | ./skills/memory-bank/ | Ready | 0.4.0 |
| secure-governance | ./skills/secure-governance/ | Ready | 0.5.0 |
| mcp-orchestrator | ./skills/mcp-orchestrator/ | Ready | 0.7.0 |
| kairos-daemon | ./skills/kairos-daemon/ | Ready | 0.10-process-isolation |

## Active Tasks
- Core skills initialization: completed
- Universal Research Agent: v0.2-async released
- Research Orchestrator: v1.0 deployed
- KAIROS-Hybrid Super-Agent: v0.10-process-isolation — Subprocess isolation, resource limits, and GovernanceGuard verified

## Sub-Agent Pool
- Explore: available
- Bash: available
- Research: available
- Reviewer: available
- PersonalAssistant: available

## Task Queuing
- Use TODO.md for task tracking
- TodoWriteTool for status updates
- MCP_SERVER.md for agent registry

## Background Mode
- State persisted in memory.md
- Task continuity via task_id
- Session resumption supported

## LLM Switching
- Config via ~/.config/opencode/ or project-level
- Use /connect command if supported
- Fallback to default model on failure

## Capabilities Active
- Web crawling (websearch, webfetch, codesearch)
- GitHub integration (gh CLI, git)
- Terminal operations (bash, ssh, docker)
- Multi-agent orchestration (TaskTool, spawn, delegate)
- Self-improvement (analysis, refinement, learning)
- Token management (summarization, progressive disclosure)
- Computer use simulation (screenshot, automation)

## Bootstrap Complete
All Claude Code + OpenClaw abilities initialized and ready.