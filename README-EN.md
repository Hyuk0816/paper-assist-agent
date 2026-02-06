# PaperAssist

**Claude Code Agent for Academic Paper Analysis**

Extract equations from PDF papers, analyze section by section in detail, evaluate citation value, and automatically generate research logs.

---

## Installation

```bash
npx paper-assist
```

This single command installs the agent to `~/.claude/agents/paper-assist.md`.

### Check Status

```bash
npx paper-assist status
```

### Uninstall

```bash
npx paper-assist uninstall
```

---

## Usage

Call the agent with `@paper-assist` in Claude Code:

```
@paper-assist Please analyze this paper: references/PDF/20260205_Vaswani_Transformer.pdf
```

### Key Features

| Feature | Description |
|---------|-------------|
| **PDF Analysis** | Direct paper analysis using Claude's PDF reading capability |
| **Section-by-Section Analysis** | Detailed analysis of important sections like Methodology, Experiments |
| **Citation Value Assessment** | Automatic classification as Must / Optional / Avoid |
| **Automatic Research Log** | Systematic markdown storage of analysis results |
| **Git Integration** | Automatic commit/push of analysis logs |

### Examples

```
# Basic analysis
@paper-assist Please analyze this paper: paper.pdf

# Comparative analysis
@paper-assist Please analyze this paper compared to my draft

# Detailed section analysis
@paper-assist Please explain the Methodology section in more detail

# Search previous analyses
@paper-assist Find papers I've analyzed related to attention
```

---

## Project Structure

Directory structure created/managed by the agent:

```
PaperAssist/
├── references/
│   ├── PDF/                    # Original PDFs
│   └── parsed/                 # Extracted results (text, equations)
├── logs/
│   └── analysis/               # Paper analysis logs
└── current_draft/              # My paper draft (for comparison)
```

---

## Citation Value Assessment

| Grade | Score | Meaning |
|-------|-------|---------|
| 🔴 **Must** | ≥ 0.7 | Essential citation (core methodology, direct relevance) |
| 🟡 **Optional** | 0.4-0.7 | Optional citation (related techniques, background) |
| ⚪ **Avoid** | < 0.4 | Citation unnecessary (low relevance) |

---

## File Naming Convention

All files follow `YYYYMMDD_Author_Title` format:

- `20260205_Vaswani_Transformer.pdf` (original)
- `20260205_Vaswani_Transformer.md` (analysis log)
- `20260205_Vaswani_Transformer_equations.md` (equations)

---

## License

MIT License
