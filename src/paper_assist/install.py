"""
PaperAssist agent installation management module
"""

import os
import platform
import shutil
from pathlib import Path
from importlib import resources


def get_agent_source_path() -> Path:
    """Returns the bundled agent file path."""
    # Python 3.9+ importlib.resources
    try:
        with resources.files('paper_assist.agent').joinpath('paper-assist.md') as p:
            return Path(p)
    except (TypeError, AttributeError):
        # Fallback: find directly in package directory
        package_dir = Path(__file__).parent
        return package_dir / 'agent' / 'paper-assist.md'


def get_global_agents_dir() -> Path:
    """Returns the OS-specific global agent directory."""
    system = platform.system()

    if system == 'Windows':
        # Windows: %USERPROFILE%\.claude\agents
        base = Path(os.environ.get('USERPROFILE', Path.home()))
    else:
        # macOS, Linux: ~/.claude/agents
        base = Path.home()

    return base / '.claude' / 'agents'


def get_local_agents_dir() -> Path:
    """Returns the local agent directory in current directory."""
    return Path.cwd() / '.claude' / 'agents'


def install_agent(location: str = 'global') -> str:
    """Install the agent.

    Args:
        location: 'global' or 'local'

    Returns:
        Installed path
    """
    source_path = get_agent_source_path()

    if not source_path.exists():
        raise FileNotFoundError(f"Agent file not found: {source_path}")

    if location == 'global':
        target_dir = get_global_agents_dir()
    else:
        target_dir = get_local_agents_dir()

    # Create directory
    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy agent file
    target_path = target_dir / 'paper-assist.md'
    shutil.copy2(source_path, target_path)

    return str(target_path)


def uninstall_agent(location: str = 'global') -> str:
    """Uninstall the agent.

    Args:
        location: 'global' or 'local'

    Returns:
        Result message
    """
    if location == 'global':
        target_dir = get_global_agents_dir()
    else:
        target_dir = get_local_agents_dir()

    target_path = target_dir / 'paper-assist.md'

    if target_path.exists():
        target_path.unlink()
        return f"Agent uninstalled: {target_path}"
    else:
        return f"Agent not installed: {target_path}"


def check_status() -> dict:
    """Check agent installation status.

    Returns:
        Installation status dictionary
    """
    global_path = get_global_agents_dir() / 'paper-assist.md'
    local_path = get_local_agents_dir() / 'paper-assist.md'

    return {
        'global': global_path.exists(),
        'global_path': str(global_path) if global_path.exists() else None,
        'local': local_path.exists(),
        'local_path': str(local_path) if local_path.exists() else None,
    }
