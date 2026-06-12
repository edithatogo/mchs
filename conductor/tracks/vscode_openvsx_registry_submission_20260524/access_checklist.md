# Open VSX / Visual Studio Marketplace Access Checklist

This checklist captures the exact account steps required to complete publisher access for `mchs-tools`.

## Open VSX

1. Sign in to an Eclipse Foundation account that will own the publisher identity.
2. Complete the Open VSX Publisher Agreement.
   - Agreement: https://open-vsx.org/publisher-agreement-v1.1
3. Link GitHub account `edithatogo` to Eclipse account `edithatogo`.
   - Completed on 2026-06-12: Eclipse reports "Account successfully connected with Github Account" and "Connected as edithatogo".
4. Complete the Open VSX Profile page's "Log in with Eclipse" agreement-recognition flow.
   - Current state on 2026-06-12: Open VSX GitHub login succeeds, but Access Tokens still reports no signed Publisher Agreement and Log in with Eclipse reaches an Eclipse Foundation username/password prompt.
5. Return to the Open VSX publisher settings and create an access token for publishing.
6. Store the token only as `OVSX_PAT` for the publish session.
7. Verify the account can view the publisher profile and token settings before attempting a publish.

## Visual Studio Marketplace

1. Sign in to the Visual Studio Marketplace publishing portal with the intended publisher identity.
2. Create or recover the publisher entry if one does not already exist.
3. Create a Personal Access Token with marketplace publish permissions.
4. Store the token only as `VSCE_PAT` for the publish session.
5. Verify the publisher profile can access the token management page before attempting a publish.

## Publish commands

```bash
npx --yes ovsx publish microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix --pat "$OVSX_PAT"
npx --yes @vscode/vsce publish --packagePath microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix --pat "$VSCE_PAT"
```

## Evidence to record

- Open VSX publisher agreement completion date
- Eclipse linked GitHub username evidence
- Open VSX publisher name and token creation confirmation
- Visual Studio Marketplace publisher ID
- Marketplace PAT scope and expiry
- Publish command output
- Public listing URLs for Open VSX and Marketplace version `0.1.0`

## Completion rule

Do not mark the track complete until the tokens exist, the publish commands have run, and public version evidence is visible in both registries if both destinations are required.
