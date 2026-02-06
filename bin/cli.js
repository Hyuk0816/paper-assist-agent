#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const AGENT_FILENAME = 'paper-assist.md';
const CLAUDE_AGENTS_DIR = path.join(os.homedir(), '.claude', 'agents');

function getSourceAgentPath() {
  // Try to find agent file relative to the script location
  const scriptDir = __dirname;
  const agentPath = path.join(scriptDir, '..', 'agent', AGENT_FILENAME);

  if (fs.existsSync(agentPath)) {
    return agentPath;
  }

  // Fallback for npx execution
  const npxPath = path.join(scriptDir, '..', 'agent', AGENT_FILENAME);
  if (fs.existsSync(npxPath)) {
    return npxPath;
  }

  return null;
}

function install() {
  console.log('📦 Installing paper-assist agent...\n');

  const sourcePath = getSourceAgentPath();
  if (!sourcePath) {
    console.error('❌ Error: Agent file not found.');
    console.error('   Please reinstall the package.');
    process.exit(1);
  }

  // Create ~/.claude/agents directory if it doesn't exist
  if (!fs.existsSync(CLAUDE_AGENTS_DIR)) {
    fs.mkdirSync(CLAUDE_AGENTS_DIR, { recursive: true });
    console.log(`📁 Created directory: ${CLAUDE_AGENTS_DIR}`);
  }

  const destPath = path.join(CLAUDE_AGENTS_DIR, AGENT_FILENAME);

  // Copy agent file
  try {
    fs.copyFileSync(sourcePath, destPath);
    console.log(`✅ Agent installed successfully!\n`);
    console.log(`   Location: ${destPath}\n`);
    console.log('🚀 Usage in Claude Code:');
    console.log('   @paper-assist Please analyze this paper: [PDF path]\n');
  } catch (err) {
    console.error(`❌ Error installing agent: ${err.message}`);
    process.exit(1);
  }
}

function uninstall() {
  console.log('🗑️  Uninstalling paper-assist agent...\n');

  const agentPath = path.join(CLAUDE_AGENTS_DIR, AGENT_FILENAME);

  if (fs.existsSync(agentPath)) {
    try {
      fs.unlinkSync(agentPath);
      console.log('✅ Agent uninstalled successfully!');
    } catch (err) {
      console.error(`❌ Error uninstalling agent: ${err.message}`);
      process.exit(1);
    }
  } else {
    console.log('ℹ️  Agent was not installed.');
  }
}

function status() {
  const agentPath = path.join(CLAUDE_AGENTS_DIR, AGENT_FILENAME);

  console.log('📊 paper-assist status\n');

  if (fs.existsSync(agentPath)) {
    const stats = fs.statSync(agentPath);
    console.log('✅ Agent is installed');
    console.log(`   Location: ${agentPath}`);
    console.log(`   Modified: ${stats.mtime.toISOString()}`);
  } else {
    console.log('❌ Agent is not installed');
    console.log('   Run: npx paper-assist install');
  }
}

function showHelp() {
  console.log(`
📄 paper-assist - Academic Paper Analysis Agent for Claude Code

Usage:
  npx paper-assist [command]

Commands:
  install     Install the agent to ~/.claude/agents/
  uninstall   Remove the agent
  status      Check installation status
  help        Show this help message

Examples:
  npx paper-assist install
  npx paper-assist status

After installation, use in Claude Code:
  @paper-assist Please analyze this paper: references/PDF/paper.pdf
`);
}

// Main
const args = process.argv.slice(2);
const command = args[0] || 'install';

switch (command) {
  case 'install':
    install();
    break;
  case 'uninstall':
    uninstall();
    break;
  case 'status':
    status();
    break;
  case 'help':
  case '--help':
  case '-h':
    showHelp();
    break;
  default:
    console.log(`Unknown command: ${command}\n`);
    showHelp();
    process.exit(1);
}
