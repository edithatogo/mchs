const vscode = require('vscode');

function activate(context) {
  const disposable = vscode.commands.registerCommand('mchs.showRegistryStatus', () => {
    vscode.window.showInformationMessage('MCHS registry status is governed by contracts/language-registry-submissions.');
  });
  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = { activate, deactivate };
