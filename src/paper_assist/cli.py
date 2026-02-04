"""
PaperAssist CLI: Academic paper analysis command-line interface
"""

import warnings
import os

# Suppress dependency warnings before importing
os.environ["NO_ALBUMENTATIONS_UPDATE"] = "1"
warnings.filterwarnings("ignore", category=UserWarning, module="albumentations")
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

import click
import sys
from pathlib import Path

from .install import install_agent, uninstall_agent, check_status
from .extract_text import extract_text
from .extract_equations import extract_equations
from .compare_papers import compare_papers


@click.group()
@click.version_option()
def main():
    """PaperAssist: Academic Paper Analysis Tool

    Extract equations from PDF papers, assess citation value,
    and automatically generate research logs for Claude Code agent.
    """
    pass


@main.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def extract(pdf_path: str, output: str | None):
    """Extract text from PDF."""
    try:
        result = extract_text(pdf_path, output)
        click.echo(f"Text extraction complete: {result}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', '-f', type=click.Choice(['latex', 'mathml']), default='latex', help='Equation format')
def equations(pdf_path: str, output: str | None, format: str):
    """Extract equations from PDF."""
    try:
        result = extract_equations(pdf_path, output, format)
        click.echo(f"Equation extraction complete: {result}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('paper_path', type=click.Path(exists=True))
@click.argument('draft_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def compare(paper_path: str, draft_path: str, output: str | None):
    """Compare paper with draft."""
    try:
        result = compare_papers(paper_path, draft_path, output)
        click.echo(f"Comparison complete: {result}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--global', 'global_install', is_flag=True, help='Global install (~/.claude/agents/)')
@click.option('--local', 'local_install', is_flag=True, help='Local install (.claude/agents/)')
def install(global_install: bool, local_install: bool):
    """Install PaperAssist agent.

    Default: Global install (available in all projects)
    """
    if local_install and global_install:
        click.echo("Error: --global and --local cannot be used together.", err=True)
        sys.exit(1)

    location = 'local' if local_install else 'global'

    try:
        result = install_agent(location)
        click.echo(f"Agent installed: {result}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--global', 'global_uninstall', is_flag=True, help='Uninstall global agent')
@click.option('--local', 'local_uninstall', is_flag=True, help='Uninstall local agent')
@click.option('--all', 'remove_all', is_flag=True, help='Uninstall all agents')
def uninstall(global_uninstall: bool, local_uninstall: bool, remove_all: bool):
    """Uninstall PaperAssist agent."""
    if remove_all:
        locations = ['global', 'local']
    elif local_uninstall:
        locations = ['local']
    else:
        locations = ['global']

    try:
        for loc in locations:
            result = uninstall_agent(loc)
            click.echo(result)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
def status():
    """Check agent installation status."""
    try:
        status_info = check_status()
        click.echo("\n=== PaperAssist Installation Status ===\n")
        click.echo(f"Global agent: {'Installed' if status_info['global'] else 'Not installed'}")
        if status_info['global']:
            click.echo(f"  Path: {status_info['global_path']}")
        click.echo(f"Local agent: {'Installed' if status_info['local'] else 'Not installed'}")
        if status_info['local']:
            click.echo(f"  Path: {status_info['local_path']}")
        click.echo()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--path', '-p', type=click.Path(), default='.', help='Parent directory path')
@click.option('--name', '-n', type=str, default='PaperAssist', help='Project folder name')
def init(path: str, name: str):
    """Initialize PaperAssist directory structure in project.

    Creates a PaperAssist folder with hybrid storage structure:
    - GitHub: Text, logs, extracted results (version control)
    - Google Drive: Original PDFs (large file backup)
    """
    parent_path = Path(path).resolve()
    project_path = parent_path / name

    # Check if project already exists
    if project_path.exists():
        click.echo(f"\n⚠️  Directory already exists: {project_path}")
        click.echo("Use --name to specify a different project name.")
        return

    click.echo(f"\n📁 Creating PaperAssist project: {project_path}\n")

    # Create required directories
    directories = [
        # references (PDF on Google Drive, parsed on GitHub)
        project_path / 'references' / 'PDF',
        project_path / 'references' / 'parsed',
        # logs (all on GitHub)
        project_path / 'logs' / 'analysis',
        project_path / 'logs' / 'session',
        project_path / 'logs' / 'decisions',
        # current_draft (GitHub)
        project_path / 'current_draft' / 'sections',
    ]

    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)
        rel_path = dir_path.relative_to(project_path)
        click.echo(f"  📂 {rel_path}/")

    # Create current_draft/main.md
    draft_file = project_path / 'current_draft' / 'main.md'
    if not draft_file.exists():
        draft_file.write_text("""# Paper Draft

> This file was auto-generated by PaperAssist.
> Section files are in the `sections/` directory.

## Overview

[Write your research overview here]

## Related Work

[Analysis results of cited papers will be added here]

## Methodology

[Write your methodology here]

## Experiments

[Write your experimental design and results here]

## Conclusion

[Write your conclusion here]

---

## References

[See bibliography.bib]
""", encoding='utf-8')
        click.echo(f"  📄 current_draft/main.md")

    # Create section files
    sections = [
        ('01_introduction.md', '# Introduction\n\n[Write introduction here]\n'),
        ('02_related_work.md', '# Related Work\n\n[Write related work here - use PaperAssist analysis results]\n'),
        ('03_methodology.md', '# Methodology\n\n[Write methodology here]\n'),
        ('04_experiments.md', '# Experiments\n\n[Write experimental design and results here]\n'),
        ('05_conclusion.md', '# Conclusion\n\n[Write conclusion here]\n'),
    ]

    for filename, content in sections:
        section_file = project_path / 'current_draft' / 'sections' / filename
        if not section_file.exists():
            section_file.write_text(content, encoding='utf-8')
            click.echo(f"  📄 current_draft/sections/{filename}")

    # Create bibliography.bib
    bib_file = project_path / 'current_draft' / 'bibliography.bib'
    if not bib_file.exists():
        bib_file.write_text("""% PaperAssist Bibliography
% BibTeX entries for analyzed papers will be added here.

% Example:
% @article{vaswani2017attention,
%   title={Attention is all you need},
%   author={Vaswani, Ashish and others},
%   journal={NeurIPS},
%   year={2017}
% }
""", encoding='utf-8')
        click.echo(f"  📄 current_draft/bibliography.bib")

    # Create .gitkeep files for empty directories
    gitkeep_dirs = [
        project_path / 'references' / 'PDF',
        project_path / 'logs' / 'session',
        project_path / 'logs' / 'decisions',
    ]
    for dir_path in gitkeep_dirs:
        gitkeep = dir_path / '.gitkeep'
        if not gitkeep.exists():
            gitkeep.write_text('')

    click.echo("\n" + "=" * 50)
    click.echo("✅ Project initialization complete!")
    click.echo("=" * 50)

    click.echo("\n📂 Generated structure:")
    click.echo(f"""
{name}/
├── current_draft/                # 📍 GitHub
│   ├── main.md
│   ├── sections/
│   │   ├── 01_introduction.md
│   │   ├── 02_related_work.md
│   │   ├── 03_methodology.md
│   │   ├── 04_experiments.md
│   │   └── 05_conclusion.md
│   └── bibliography.bib
├── references/
│   ├── PDF/                      # 📍 Google Drive (backup)
│   └── parsed/                   # 📍 GitHub
├── logs/                         # 📍 GitHub
│   ├── analysis/
│   ├── session/
│   └── decisions/
""")

    click.echo(f"\n📋 Usage:")
    click.echo(f"  1. cd {project_path}")
    click.echo("  2. Put PDF papers to analyze in references/PDF/")
    click.echo("     (Filename format: YYYYMMDD_Author_Title.pdf)")
    click.echo("  3. Run '@paper-assist Please analyze this paper' in Claude Code")
    click.echo("  4. Check analysis results in logs/analysis/")

    click.echo("\n📦 Required MCP servers:")
    click.echo("  - GitHub MCP: Auto commit/push logs")
    click.echo("  - Google Drive MCP: PDF backup (optional)")
    click.echo("\n  See README for MCP installation instructions.")


if __name__ == '__main__':
    main()
