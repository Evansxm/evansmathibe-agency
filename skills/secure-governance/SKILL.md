---
name: secure-governance
description: Secure governance layer with tool allow-lists, permission checks, and task isolation (inspired by KiloClaw enterprise security)
keywords: [security, governance, permissions, allow-list, isolation, sandbox]
version: 0.5.0
author: KAIROS-Hybrid Super-Agent v0.5
---

# Secure Governance Skill

## Purpose
Provides security governance for the KAIROS agent, inspired by KiloClaw's secure always-on enterprise features:
- Tool allow-lists for controlled execution
- Permission checks for sensitive operations
- Task isolation (sandboxed execution)
- Audit logging for compliance

## Architecture

### Components
1. **ToolAllowList** - Controls which tools can be executed
2. **PermissionChecker** - Validates sensitive operations
3. **TaskIsolator** - Provides sandboxed execution environment
4. **AuditLogger** - Logs all operations for compliance

## Capabilities

### Tool Allow-Lists
Define which tools are allowed in different contexts:
- Safe: read, grep, glob, websearch
- Restricted: edit, write, bash (require confirmation)
- Dangerous: ssh, docker, delete (require explicit approval)

### Permission System
```python
from secure_governance import PermissionChecker

checker = PermissionChecker()
result = checker.check('bash', 'rm -rf /')
# Returns: {'allowed': False, 'reason': 'Dangerous command requires approval'}
```

### Task Isolation
Each task runs in an isolated workspace:
- Separate filesystem view
- No access to sensitive directories by default
- Timeouts for long-running operations

### Audit Logging
All operations logged with:
- Timestamp
- User/Agent
- Tool used
- Parameters (sanitized)
- Result/Status

## Usage

### CLI
```bash
python3 secure_governance.py check "rm -rf /"
python3 secure_governance.py allowlist --add bash
python3 secure_governance.py audit --recent
```

### Python API
```python
from secure_governance import SecureGovernor

governor = SecureGovernor()
result = governor.execute_task({
    'tool': 'bash',
    'command': 'ls',
    'isolated': True
})
```

## Default Policies

| Tool Category | Default | Requires Approval |
|---------------|---------|-------------------|
| read/grep/glob | ✅ Allow | No |
| websearch | ✅ Allow | No |
| edit/write | ⚠️ Warn | Yes |
| bash (safe) | ⚠️ Warn | Optional |
| bash (dangerous) | ❌ Block | Always |
| ssh/docker | ❌ Block | Always |
| delete | ❌ Block | Always |

## Files
- `secure_governance.py` - Main module
- `allow_lists.py` - Tool allow-list management
- `isolator.py` - Task isolation
- `audit.py` - Audit logging