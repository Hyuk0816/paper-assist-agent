# PaperAssist

**Claude Code Agent Tool for Academic Paper Analysis**

Extract equations from PDF papers, analyze section by section in detail, evaluate citation value, and automatically generate research logs.

---

## Table of Contents

- [Key Features](#key-features)
- [Installation](#installation)
- [Project Initialization](#project-initialization)
- [Usage](#usage)
- [File Naming Convention](#file-naming-convention)
- [Analysis Log Structure](#analysis-log-structure)
- [Citation Value Assessment](#citation-value-assessment)
- [Hybrid Storage](#hybrid-storage)
- [MCP Server Integration](#mcp-server-integration)
- [CLI Commands](#cli-commands)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)

---

## Key Features

| Feature | Description |
|---------|-------------|
| **PDF Equation Extraction** | Automatically extract equations in LaTeX format using pix2tex |
| **Section-by-Section Analysis** | Identify paper structure and analyze important sections (Methodology, Experiments, etc.) in detail |
| **Citation Value Assessment** | Automatically classify as Must / Optional / Avoid |
| **Automatic Research Log Generation** | Save analysis results as structured markdown |
| **Hybrid Storage** | GitHub (text/logs) + Google Drive (PDF) synchronization |
| **Date-based Recording** | Systematic management in `YYYYMMDD_Author_Title` format |

---

## Installation

### Requirements

- **Python**: 3.10 or higher
- **Claude Code CLI**: Installed and logged in
- **Git**: For version control

### Recommended: Install with pipx (macOS/Linux)

`pipx` runs Python CLI tools in an isolated environment without touching system Python.

```bash
# 1. Install pipx (if not installed)
brew install pipx        # macOS
# or
apt install pipx         # Ubuntu/Debian
# or
pip install --user pipx  # Others

# Set up PATH
pipx ensurepath

# 2. Install paper-assist
pipx install paper-assist

# 3. Register agent (run once)
paper-assist install --global

# 4. Verify installation
paper-assist status
```

**After installation:**
```bash
# CLI available anywhere
paper-assist extract paper.pdf
paper-assist equations paper.pdf

# Use agent in Claude Code (no venv needed!)
claude
> @paper-assist Please analyze this paper
```

### Install with pip

#### macOS (PEP 668 Environment)

macOS requires a virtual environment due to system Python protection policy:

```bash
# Create and activate virtual environment
python3 -m venv ~/.paper-assist-venv
source ~/.paper-assist-venv/bin/activate

# Install
pip install paper-assist

# Register agent (with venv activated)
paper-assist install --global
```

> **Note**: Once registered, the agent (`@paper-assist`) works in Claude Code without venv.
> CLI tools (`paper-assist extract`, etc.) require venv activation.

#### Linux/Windows

```bash
# Direct installation possible
pip install paper-assist

# Register agent
paper-assist install --global
```

### Install from Source

```bash
git clone https://github.com/Hyuk0816/paper-assist-agent.git
cd paper-assist-agent

# Install with pipx
pipx install .

# Or install with venv
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Verify Installation

```bash
# Check CLI version
paper-assist --version

# Check agent installation status
paper-assist status
```

**Installation Locations:**
- Global agent: `~/.claude/agents/paper-assist.md`
- Local agent: `./.claude/agents/paper-assist.md`

---

## Project Initialization

To use PaperAssist in a new research project:

```bash
# Create project structure in current directory
paper-assist init

# Or create in a specific path
paper-assist init --path /path/to/my-research
```

### Generated Directory Structure

```
PaperAssist/
│
├── current_draft/                     # 📍 GitHub (paper draft)
│   ├── main.md                        # Paper body (integrated)
│   ├── sections/                      # Separated by section
│   │   ├── 01_introduction.md
│   │   ├── 02_related_work.md
│   │   ├── 03_methodology.md
│   │   ├── 04_experiments.md
│   │   └── 05_conclusion.md
│   └── bibliography.bib               # References (BibTeX)
│
├── references/
│   ├── PDF/                           # 📍 Google Drive (original PDFs)
│   │   └── YYYYMMDD_Author_Title.pdf
│   └── parsed/                        # 📍 GitHub (extracted results)
│       ├── YYYYMMDD_Author_Title_text.txt
│       └── YYYYMMDD_Author_Title_equations.md
│
├── logs/                              # 📍 GitHub (all logs)
│   ├── analysis/                      # Paper analysis logs
│   │   └── YYYYMMDD_Author_Title.md
│   ├── session/                       # Session logs
│   │   └── YYYYMMDD_session.md
│   └── decisions/                     # Decision logs
│       └── YYYYMMDD_decision_topic.md
│
└── .claude/
    └── agents/
        └── paper-assist.md            # Agent definition (local install)
```

---

## Usage

### Using the Agent in Claude Code

Call the agent with `@paper-assist` in Claude Code CLI:

#### Basic Paper Analysis

```
@paper-assist Please analyze this paper: references/PDF/20260205_Vaswani_Transformer.pdf
```

Tasks performed by the agent:
1. Check and create directory structure
2. Extract text from PDF
3. Extract equations from PDF (LaTeX)
4. Detailed section-by-section analysis
5. Citation value assessment
6. Generate analysis log
7. Git commit and push
8. Google Drive PDF backup (if MCP installed)

#### Comparative Analysis

```
@paper-assist Please analyze this paper compared to my draft
```

#### Search Previous Analyses

```
@paper-assist Find papers I've analyzed related to attention
```

#### Detailed Section Analysis

```
@paper-assist Please explain the Methodology section of this paper in more detail
```

#### Follow-up Questions (Interactive Study)

```
@paper-assist Why is softmax used in this equation?
```

```
@paper-assist How is this methodology different from my research?
```

### Direct CLI Usage

You can also use the CLI directly without the agent:

```bash
# Extract text from PDF
paper-assist extract references/PDF/paper.pdf
paper-assist extract references/PDF/paper.pdf -o output.txt

# Extract equations from PDF (LaTeX)
paper-assist equations references/PDF/paper.pdf
paper-assist equations references/PDF/paper.pdf -o equations.md

# Compare paper with draft
paper-assist compare references/parsed/paper_text.txt current_draft/main.md
```

---

## File Naming Convention

All files follow the **`YYYYMMDD_Author_Title`** format.

### Format Description

- **YYYYMMDD**: Analysis date (e.g., 20260205)
- **Author**: First author's last name (e.g., Vaswani, Kim, Lee)
- **Title**: 1-2 key keywords from the paper title (e.g., Transformer, BERT, GPT)

### Examples by File Type

| Type | Format | Example |
|------|--------|---------|
| **Original PDF** | `YYYYMMDD_Author_Title.pdf` | `20260205_Vaswani_Transformer.pdf` |
| **Analysis Log** | `YYYYMMDD_Author_Title.md` | `20260205_Vaswani_Transformer.md` |
| **Text Extraction** | `YYYYMMDD_Author_Title_text.txt` | `20260205_Vaswani_Transformer_text.txt` |
| **Equation Extraction** | `YYYYMMDD_Author_Title_equations.md` | `20260205_Vaswani_Transformer_equations.md` |
| **Session Log** | `YYYYMMDD_session.md` | `20260205_session.md` |

### Benefits of Naming Convention

- **Chronological Sorting**: See at a glance when each paper was analyzed
- **Easy Search**: Quick search by author name or keyword
- **GitHub/Google Drive Sync**: Managed with the same name on both sides

---

## Analysis Log Structure

PaperAssist performs **section-based analysis**.

### Analysis Principles

1. **Section-based**: Identify paper structure and summarize each section
2. **Important Section Selection**: Analyze sections directly related to problem-solving and experiments in detail
3. **Flexible Structure**: Adjust according to actual paper structure since section structure varies by paper

### Section Importance

| Importance | Sections | Analysis Depth |
|------------|----------|----------------|
| **Required** | Abstract, Introduction, Methodology, Experiments, Conclusion | Detailed analysis |
| **Optional** | Related Work, Discussion, Limitations | Summary of key points |
| **Reference** | Appendix, Acknowledgments | Mentioned when needed |

### Log Structure Example

```markdown
# 📄 Paper Analysis: Attention Is All You Need

## 📑 Section-by-Section Analysis

### Abstract
- Problem: Parallelization limitations of RNN/CNN-based sequence models
- Method: Propose Transformer architecture based on self-attention
- Results: SOTA in English-German translation, significant reduction in training time

### 1. Introduction
#### 1.1 Problem Definition
Parallelization constraints of sequential computation...

#### 1.2 Limitations of Existing Methods
- RNN: Cannot parallelize due to sequential processing
- CNN: Requires many layers to learn long-range dependencies

#### 1.3 Proposed Method (Key Idea)
Perform sequence transformation using only attention...

### 3. Methodology ⭐ (Detailed)
#### 3.3 Key Equations
**Scaled Dot-Product Attention**
$$
\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$
- Meaning: Calculate similarity between Query and Key to weighted sum of Values
- Role: Directly model relationships between all positions in the sequence

### 4. Experiments ⭐ (Detailed)
#### 4.2 Main Results
| Model | EN-DE BLEU | EN-FR BLEU |
|-------|------------|------------|
| Transformer (big) | **28.4** | **41.0** |

### 🏷️ Citation Value: Must 🔴 (0.85)
Essential citation for Transformer-based research
```

---

## Citation Value Assessment

### Grade Criteria

| Grade | Score | Meaning | Criteria |
|-------|-------|---------|----------|
| 🔴 **Must** | ≥ 0.7 | Essential citation | Core methodology, direct relevance, foundational paper |
| 🟡 **Optional** | 0.4-0.7 | Optional citation | Related techniques, comparison target, background knowledge |
| ⚪ **Avoid** | < 0.4 | Citation unnecessary | Low relevance, better alternatives exist |

### Assessment Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Keyword Overlap | 40% | Keyword similarity with my draft |
| Methodology Similarity | 30% | Similarity of approach |
| Citation Index | 20% | Citation count, academic impact |
| Venue Tier | 10% | Quality of publication venue |

### Venue Tiers

| Tier | Score | Venues |
|------|-------|--------|
| **A*** | 1.0 | NeurIPS, ICML, ICLR, CVPR, ICCV, ACL, EMNLP, Nature, Science |
| **A** | 0.8 | AAAI, IJCAI, ECCV, NAACL, COLING, TPAMI, JMLR |
| **B** | 0.6 | WACV, BMVC, CoNLL, TACL, Pattern Recognition |
| **C** | 0.4 | Other peer-reviewed venues |

---

## Hybrid Storage

PaperAssist recommends a hybrid storage structure using both **GitHub** and **Google Drive**.

### Storage Separation Principle

| Storage | Contents | Reason |
|---------|----------|--------|
| **GitHub** | Text, logs, extracted results, drafts | Version control, search, change history |
| **Google Drive** | Original PDFs | Large files, backup, date-based recording |

### Synchronization Workflow

```
Paper Analysis Start
       │
       ├── PDF Storage: Google Drive/PaperAssist/references/PDF/
       │
       ├── Text Extraction: GitHub repo/references/parsed/
       │
       ├── Equation Extraction: GitHub repo/references/parsed/
       │
       ├── Analysis Log: GitHub repo/logs/analysis/
       │
       └── Auto Commit/Push: GitHub
```

### Benefits

1. **Solve PDF Size Issues**: Bypass GitHub's large file restrictions
2. **Date-based Recording**: Track when each paper was viewed on both sides
3. **Easy Search**: Search log content on GitHub, check original PDFs on Drive
4. **Backup**: Safe with distributed storage in two locations

---

## MCP Server Integration

PaperAssist provides more powerful features through integration with MCP (Model Context Protocol) servers.

### Required MCP

**None** - Basic features work without MCP.

### Recommended MCP

#### GitHub MCP

Automatically commit/push analysis logs.

```json
// ~/.claude/settings.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-github-token"
      }
    }
  }
}
```

#### Google Drive MCP

Automatically backup PDFs to Google Drive.

```json
// ~/.claude/settings.json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@anthropic/server-gdrive"]
    }
  }
}
```

### Usage Without MCP

You can perform the same workflow with Git commands and manual backup without MCP:

```bash
# Manual Git commit/push
git add logs/ references/parsed/
git commit -m "📝 Add analysis: Vaswani 2017 - Transformer"
git push origin main

# Manual Google Drive upload
# Manually sync references/PDF/ folder to Google Drive
```

---

## CLI Commands

### Full Command List

```bash
paper-assist --help
```

| Command | Description | Example |
|---------|-------------|---------|
| `extract` | Extract text from PDF | `paper-assist extract paper.pdf` |
| `equations` | Extract equations from PDF | `paper-assist equations paper.pdf` |
| `compare` | Compare paper with draft | `paper-assist compare paper.txt draft.md` |
| `install` | Install agent | `paper-assist install --global` |
| `uninstall` | Remove agent | `paper-assist uninstall --all` |
| `status` | Check installation status | `paper-assist status` |
| `init` | Initialize project | `paper-assist init` |

### Command Details

#### extract

```bash
# Basic usage (auto output path)
paper-assist extract references/PDF/paper.pdf
# Output: references/parsed/paper_text.txt

# Specify output path
paper-assist extract paper.pdf -o /path/to/output.txt
```

#### equations

```bash
# Basic usage (LaTeX format)
paper-assist equations references/PDF/paper.pdf
# Output: references/parsed/paper_equations.md

# Specify output path
paper-assist equations paper.pdf -o equations.md
```

#### compare

```bash
# Compare paper text with draft
paper-assist compare references/parsed/paper_text.txt current_draft/main.md

# Specify output path
paper-assist compare paper.txt draft.md -o comparison.md
```

#### install / uninstall

```bash
# Global install (recommended)
paper-assist install
paper-assist install --global

# Local install (current project only)
paper-assist install --local

# Global uninstall
paper-assist uninstall

# Uninstall all
paper-assist uninstall --all
```

#### init

```bash
# Initialize in current directory
paper-assist init

# Initialize in specific path
paper-assist init --path /path/to/project
```

---

## Dependencies

### Required Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Python | >= 3.10 | Runtime |
| PyMuPDF | >= 1.23.0 | PDF text extraction |
| click | >= 8.0.0 | CLI framework |
| scikit-learn | >= 1.3.0 | Text comparison (TF-IDF) |

### Optional Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pix2tex | >= 0.1.0 | PDF equation → LaTeX conversion |

### Verify Installation

```bash
# Check dependencies
pip list | grep -E "pymupdf|click|scikit-learn|pix2tex"

# Install pix2tex (for equation extraction)
pip install pix2tex
```

---

## Troubleshooting

### Common Issues

#### 1. "command not found: paper-assist"

**Cause**: pip install path not in PATH

**Solution**:
```bash
# Check pip install path
python -m site --user-base

# Add to PATH (~/.bashrc or ~/.zshrc)
export PATH="$PATH:$(python -m site --user-base)/bin"
```

#### 2. Agent Not Recognized

**Cause**: Agent not installed or in wrong location

**Solution**:
```bash
# Check installation status
paper-assist status

# Reinstall
paper-assist uninstall --all
paper-assist install
```

#### 3. PDF Text Extraction Failed

**Cause**: Image-based PDF (scanned)

**Solution**:
- OCR-required PDFs are not currently supported
- Use text-based PDFs or process with OCR first

#### 4. Equation Extraction Not Working

**Cause**: pix2tex not installed

**Solution**:
```bash
pip install pix2tex
```

#### 5. Git Push Failed

**Cause**: Remote repository not configured or permission issue

**Solution**:
```bash
# Check remote repository
git remote -v

# Add remote repository
git remote add origin https://github.com/username/repo.git

# Manual push
git push -u origin main
```

#### 6. Google Drive MCP Not Connected

**Cause**: MCP server not configured

**Solution**:
- MCP configuration is optional
- You can manually upload PDFs to Google Drive
- See [MCP Server Integration](#mcp-server-integration) section for MCP setup

### Check Logs

For detailed logs when issues occur:

```bash
# CLI verbose output
paper-assist extract paper.pdf --verbose

# Python error trace
python -c "from paper_assist import extract_text; extract_text('paper.pdf')"
```

---

## Contributing

Issues and PRs are welcome!

### Development Environment Setup

```bash
# Clone repository
git clone https://github.com/Hyuk0816/paper-assist-agent.git
cd paper-assist-agent

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Code Style

```bash
# Formatting
black src/

# Linting
ruff check src/
```

---

## License

MIT License

---

## Related Links

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [MCP Server List](https://github.com/anthropics/mcp-servers)
- [pix2tex (LaTeX OCR)](https://github.com/lukas-blecher/LaTeX-OCR)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
