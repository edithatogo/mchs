const fs = require('fs');
const path = require('path');
const vscode = require('vscode');

const REGISTRY_ID = 'vscode_openvsx';
const CONTRACT_PATH = path.join(
  'contracts',
  'language-registry-submissions',
  'language-registry-submissions.contract.json'
);
const ROADMAP_PATH = path.join('docs', 'roadmaps', 'language-registry-external-gates.md');
const VSIX_PATH = path.join('integrations', 'vscode', 'mchs-tools-0.1.1.vsix');

function fileExists(candidate) {
  try {
    return fs.statSync(candidate).isFile();
  } catch {
    return false;
  }
}

function findMchsWorkspaceRoot() {
  const workspaceFolders = vscode.workspace.workspaceFolders || [];
  for (const folder of workspaceFolders) {
    const folderPath = folder.uri.fsPath;
    const directContract = path.join(folderPath, CONTRACT_PATH);
    const nestedContract = path.join(folderPath, 'microcosting_healthservices', CONTRACT_PATH);

    if (fileExists(directContract)) {
      return folderPath;
    }
    if (fileExists(nestedContract)) {
      return path.join(folderPath, 'microcosting_healthservices');
    }
  }

  return undefined;
}

function readRegistry(root) {
  const contractFile = path.join(root, CONTRACT_PATH);
  const contract = JSON.parse(fs.readFileSync(contractFile, 'utf8'));
  const registry = contract.registries.find((entry) => entry.id === REGISTRY_ID);
  if (!registry) {
    throw new Error(`Registry entry ${REGISTRY_ID} was not found in ${CONTRACT_PATH}.`);
  }
  return registry;
}

function statusLines(registry) {
  return [
    `Package: ${registry.package}@${registry.version}`,
    `Registry: ${registry.registry}`,
    `Status: ${registry.current_status}`,
    `Publication claimed: ${registry.publicationClaimed === true ? 'yes' : 'no'}`,
    `Submission URL: ${registry.submission_url || 'none recorded'}`,
    `Blocker: ${registry.blocker || 'none recorded'}`
  ];
}

async function openWorkspaceFile(relativePath) {
  const root = findMchsWorkspaceRoot();
  if (!root) {
    await vscode.window.showWarningMessage(
      'Open the MCHS repository workspace to use MCHS helper commands.'
    );
    return;
  }

  const target = path.join(root, relativePath);
  if (!fileExists(target)) {
    await vscode.window.showErrorMessage(`MCHS helper could not find ${relativePath}.`);
    return;
  }

  const document = await vscode.workspace.openTextDocument(target);
  await vscode.window.showTextDocument(document);
}

async function showRegistryStatus(outputChannel) {
  const root = findMchsWorkspaceRoot();
  if (!root) {
    await vscode.window.showWarningMessage(
      'Open the MCHS repository workspace to read the registry gate status.'
    );
    return;
  }

  try {
    const registry = readRegistry(root);
    outputChannel.clear();
    outputChannel.appendLine('MCHS VS Code/Open VSX registry gate');
    outputChannel.appendLine('');
    for (const line of statusLines(registry)) {
      outputChannel.appendLine(line);
    }
    outputChannel.show(true);
    await vscode.window.showInformationMessage(
      `MCHS ${registry.package} is ${registry.current_status}. Publication evidence is recorded in the contract.`
    );
  } catch (error) {
    await vscode.window.showErrorMessage(`MCHS helper failed: ${error.message}`);
  }
}

async function copyOpenVsxPublishCommand() {
  const root = findMchsWorkspaceRoot();
  const vsixPath = root ? path.join(root, VSIX_PATH) : VSIX_PATH;
  const command = `npx --yes ovsx publish "${vsixPath}" --pat "$OVSX_PAT"`;
  await vscode.env.clipboard.writeText(command);
  await vscode.window.showInformationMessage(
    'Copied the gated Open VSX publish command. Run it only after publisher agreement and token setup.'
  );
}

function activate(context) {
  const outputChannel = vscode.window.createOutputChannel('MCHS Registry Gates');

  context.subscriptions.push(
    outputChannel,
    vscode.commands.registerCommand('mchs.showRegistryStatus', () =>
      showRegistryStatus(outputChannel)
    ),
    vscode.commands.registerCommand('mchs.openLanguageRegistryContract', () =>
      openWorkspaceFile(CONTRACT_PATH)
    ),
    vscode.commands.registerCommand('mchs.openExternalGateRoadmap', () =>
      openWorkspaceFile(ROADMAP_PATH)
    ),
    vscode.commands.registerCommand('mchs.copyOpenVsxPublishCommand', copyOpenVsxPublishCommand)
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
