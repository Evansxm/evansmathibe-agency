# Evans Home Directory - Agent Guidelines

---

## Hybrid Agent: Claude Code + OpenClaw v2.1.88

**Identity:** Autonomous CLI + personal agent with persistent local-first capabilities

**Core Rules:**
- Technical truth, precision, minimalism
- Read-before-write, no over-engineering
- Safety first: refuse destructive actions, no force pushes
- PlanMode for non-trivial tasks (Explore → Plan → Execute → Verify)

**Tools:** Full terminal, web crawling, file ops, GitHub integration, multi-agent orchestration

**Persistence:** AGENTS.md, TODO.md, skills/, memory.md

---

## Branding Notes
- All work is done under **Evans Mathibe AI** (not just "EvansMathibe Agency"). Use "Evans Mathibe AI" as the brand name in all outputs.
- "Evans Mathibe AI" refers to the full AI-powered agency system. "EvansMathibe Agency" can be used interchangeably for the website but AI tasks cite "Evans Mathibe AI".

## Available Skills

| Skill | Purpose |
|-------|---------|
| master-agent | Core orchestration, task planning, delegation |
| web-research | Web crawling, search, browsing, summarization |
| github-orchestrator | Clone, commit, PRs, issues, gh CLI integration |
| terminal-master | Bash, SSH, docker, persistent sessions |
| multi-agent-orchestrator | Spawn/manage sub-agents, background tasks |
| self-improvement | Analyze performance, refine prompts, update skills |
| token-manager | Context summarization, progressive disclosure |
| computer-use-sim | Screenshot capture, GUI automation |
| universal-research-agent | Async parallel web crawling, multi-query research |
| research-orchestrator | Multi-agent research orchestration, synthesis, reporting |
| kairos-core | KAIROS-Hybrid Super-Agent with caching, dream/reflection, proactive |
| memory-bank | Persistent vector/memory storage for long-term context |
| secure-governance | Security governance with tool allow-lists, permissions, isolation |
| mcp-orchestrator | Model Context Protocol orchestration with real-time streaming |
| kairos-daemon | Persistent background daemon with tick cycles, autoDream, and persistent session state |
| secure-credentials | Encrypted credential vault with AES-256 + just-in-time injection (zero leaks) |
| multi-llm-router | Autonomous LLM routing based on risk/complexity assessment (high-speed vs high-reasoning) |
| tenant-isolation-benchmark | Process-level isolation and multi-tenant benchmarking |

---

# Project Overview

| Project | Type | Location | Package Manager |
|---------|------|----------|-----------------|
| **EvansMathibe Agency** | Static Website (GitHub Pages) | `/home/ev/EvansMathibe_Agency/` | N/A |
| **Website Backups** | Python/SQLite | `/home/ev/Projects/website_backups/` | pip |
| **buzznewz** | Node.js/Express API | `/home/ev/buzznewz/` | npm |
| **openclaw** | TypeScript/Node | `/home/ev/openclaw/` | pnpm |
| **openwork** | TypeScript/Tauri/SolidJS | `/home/ev/openwork/` | pnpm |

---

## Quick Reference Commands

### Website Backup System (Primary Integration)

```bash
# Check backup status
evans-backup status
python3 /home/ev/Projects/website_backups/scripts/opencode_agent.py status

# Create backup before making changes
evans-backup backup "description of changes"

# Restore website (latest or specific)
evans-backup restore
evans-backup restore 1

# List all backups
evans-backup list

# Verify site is live
evans-backup verify
```

### Live Website

- **URL:** https://evansxm.github.io/evansmathibe-agency/
- **GitHub Repo:** https://github.com/Evansxm/evansmathibe-agency
- **Branch:** gh-pages

---

## Project-Specific Guidelines

### EvansMathibe Agency (Website)

**Type:** Static HTML/CSS/JS (GitHub Pages)

**Key Files:**
- `/home/ev/EvansMathibe_Agency/website/index.html` - Main landing page
- `/home/ev/EvansMathibe_Agency/website/images/` - Gallery images
- `/home/ev/EvansMathibe_Agency/website/videos/` - Video assets
- `/home/ev/EvansMathibe_Agency/website/logo.png` - Logo

**Before Making Changes:**
```bash
# Always backup first
evans-backup backup "before making website changes"
```

**After Changes:**
```bash
# Commit and push to GitHub
cd /tmp/evansmathibe-agency
git add .
git commit -m "Description of changes"
git push origin gh-pages
```

**Testing:** Open https://evansxm.github.io/evansmathibe-agency/ in browser

---

### Website Backups (Python)

**Type:** Python 3 / SQLite

**Key Files:**
- `/home/ev/Projects/website_backups/scripts/backup_manager.py` - Main backup logic
- `/home/ev/Projects/website_backups/scripts/opencode_agent.py` - CLI wrapper
- `/home/ev/Projects/website_backups/backup_database.db` - SQLite database

**Commands:**
```bash
# Run backup manager directly
python3 /home/ev/Projects/website_backups/scripts/backup_manager.py

# Check status
python3 /home/ev/Projects/website_backups/scripts/opencode_agent.py status

# List backups
python3 /home/ev/Projects/website_backups/scripts/opencode_agent.py list
```

**Code Style:**
- Python 3
- Type hints where beneficial
- Classes for stateful operations (BackupManager)
- Clear docstrings for functions

---

### buzznewz (Node.js API)

**Type:** Express.js backend API

**Location:** `/home/ev/buzznewz/`

**Commands:**
```bash
cd /home/ev/buzznewz

# Install dependencies
npm install

# Start development server
npm run dev
# or
node server.js

# Run tests (if any)
npm test
```

**Code Style:**
- JavaScript (ES6+)
- Express.js patterns
- Async/await for async operations
- Environment variables in `.env`

---

### openclaw (TypeScript)

**Type:** Node.js CLI application

**Location:** `/home/ev/openclaw/`

**Commands:**
```bash
cd /home/ev/openclaw

# Install dependencies
pnpm install

# Build
pnpm build

# TypeScript checks
pnpm tsgo

# Lint/format
pnpm check
pnpm format       # check only
pnpm format:fix   # apply fixes

# Run tests
pnpm test
pnpm test:coverage

# Run CLI
pnpm openclaw ...
pnpm dev
```

**Code Style:**
- TypeScript (strict typing, avoid `any`)
- Oxlint and Oxfmt for linting/formatting
- Vitest for testing
- Files under ~700 LOC
- Brief comments for tricky logic

---

### openwork (TypeScript/Tauri)

**Type:** Desktop application (Tauri + SolidJS)

**Location:** `/home/ev/openwork/`

**Commands:**
```bash
cd /home/ev/openwork

# Install dependencies
pnpm install

# Development
pnpm dev              # Full dev stack
pnpm dev:ui           # UI only

# Build
pnpm build
pnpm build:ui

# TypeScript checks
pnpm typecheck

# Run tests
pnpm test:e2e
pnpm test:refactor
# ... many more test commands - see package.json

# Tauri commands
pnpm tauri dev
pnpm tauri build
```

**Code Style:**
- TypeScript with strict typing
- SolidJS for UI
- TailwindCSS for styling
- Tauri 2.x for desktop shell
- Follow PRINCIPLES.md, PRODUCT.md, ARCHITECTURE.md

---

## Code Style Guidelines

### Python

```python
# Use type hints
def process_backup(backup_id: int) -> dict:
    """Process a backup by ID.
    
    Args:
        backup_id: The backup identifier
        
    Returns:
        Dictionary with backup data
    """
    pass

# Classes for stateful operations
class BackupManager:
    def __init__(self, config: dict):
        self.config = config
    
    def create_backup(self, description: str) -> str:
        """Create new backup with description."""
        pass
```

### JavaScript/TypeScript

```typescript
// Strict typing - avoid any
interface Backup {
  id: number;
  timestamp: string;
  description: string;
  files: string[];
}

// Async/await pattern
async function fetchBackup(id: number): Promise<Backup> {
  const response = await fetch(`/api/backups/${id}`);
  return response.json();
}

// Clear naming
const backupManager = new BackupManager(config);
const isValid = backupManager.validate(backup);
```

### HTML/CSS

```html
<!-- Semantic HTML -->
<header>
  <nav>
    <ul>
      <li><a href="#home">Home</a></li>
    </ul>
  </nav>
</header>

<!-- Accessibility -->
<img src="logo.png" alt="EvansMathibe Agency Logo">
<button aria-label="Open menu">☰</button>
```

---

## Error Handling

### Python
```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise CustomError("Fallback message") from e
```

### JavaScript
```javascript
try {
  const result = await riskyOperation();
} catch (error) {
  console.error('Operation failed:', error);
  throw new CustomError('Fallback message');
}
```

---

## Git Workflow

### Before Making Changes
```bash
# Always backup website first
evans-backup backup "before making changes"
```

### Commit Messages
- Use clear, action-oriented messages
- Example: `Add new gallery images`, `Fix contact form submission`

### Branch Strategy
- **Website:** Push directly to `gh-pages` branch
- **Other projects:** Use feature branches, PRs

---

## Security Notes

- Never commit secrets, API keys, or credentials
- Use environment variables for sensitive data
- `.env` files should be in `.gitignore`

---

## File Organization

```
/home/ev/
├── EvansMathibe_Agency/     # Website source
│   └── website/
├── Projects/
│   └── website_backups/    # Backup system
├── buzznewz/              # Node.js API
├── openclaw/              # TypeScript CLI
├── openwork/              # Desktop app
└── .local/bin/
    └── evans-backup        # CLI wrapper
```

---

## Common Tasks

### Update Website
1. `evans-backup backup "before update"`
2. Edit files in `/home/ev/EvansMathibe_Agency/website/`
3. Push to GitHub
4. Verify at https://evansxm.github.io/evansmathibe-agency/

### Restore Website
1. `evans-backup restore`
2. Verify restoration

### Add New Feature to Project
1. Check existing patterns in the codebase
2. Follow the project's code style
3. Test locally before pushing

---

## Troubleshooting

### Website not updating?
- Check GitHub Pages build status
- Verify commit pushed to `gh-pages` branch
- Clear browser cache

### Backup failing?
- Check `/home/ev/Projects/website_backups/logs/`
- Verify SQLite database exists
- Check disk space

### Dependencies missing?
- Run `npm install` / `pnpm install` / `pip install -r requirements.txt`
