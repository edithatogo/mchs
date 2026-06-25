# Open VSX / Visual Studio Marketplace Access Checklist

This checklist captures the exact account steps required to complete publisher access for `mchs-tools`.

## Open VSX

1. Sign in to an Eclipse Foundation account that will own the publisher identity.
2. Complete the Open VSX Publisher Agreement.
   - Agreement: https://open-vsx.org/publisher-agreement-v1.1
3. Link GitHub account `edithatogo` to Eclipse account `edithatogo`.
   - Completed on 2026-06-12: Eclipse reports "Account successfully connected with Github Account" and "Connected as edithatogo".
   - Recheck on 2026-06-13: the Eclipse profile still has an empty disabled GitHub Username field, and the linked-account page renders "Connected as" with an empty visible value.
4. Confirm Open VSX can establish a logged-in session from GitHub OAuth.
   - Current state on 2026-06-13: Open VSX user settings can show login name `edithatogo`, but Access Tokens still reports no recognized Eclipse Foundation Open VSX Publisher Agreement.
5. Complete the Open VSX Profile page's "Log in with Eclipse" agreement-recognition flow if Open VSX still does not recognize the agreement after GitHub login.
   - Current state on 2026-06-13: Profile > Log in with Eclipse reaches the Eclipse Foundation password form for the `openvsx_publisher_agreement` scope. This requires user credentials.
6. Repair or relink the Eclipse GitHub account if Open VSX continues to reject namespace or token actions.
   - Current state on 2026-06-13: Open VSX Namespaces shows no namespaces; creating namespace `edithatogo` returns `Forbidden`.
7. Return to the Open VSX publisher settings and create an access token for publishing.
8. Store the token only as `OVSX_PAT` for the publish session.
9. Verify the account can view the publisher profile and token settings before attempting a publish.
10. Retry publishing `mchs-tools-0.1.0.vsix` only after namespace/agreement recognition succeeds.
    - Historical state on 2026-06-13: web upload of `mchs-tools-0.1.0.vsix` returned `Forbidden` before agreement/token recognition completed.
11. Completed after agreement/token recognition: Open VSX API now exposes `edithatogo.mchs-tools`, latest version `0.1.1`, and allVersions including `0.1.0`; the canonical `0.1.0` publication remains available.

## Visual Studio Marketplace

1. Sign in to the Visual Studio Marketplace publishing portal with the intended publisher identity.
2. Create or recover the publisher entry if one does not already exist.
3. Publish through either the Marketplace web upload dialog or a Personal Access Token with marketplace publish permissions.
4. Completed on 2026-06-12: the signed-in Marketplace page showed publisher `edithatogo` with Owner role, the Visual Studio Code upload dialog accepted `mchs-tools-0.1.0.vsix`, and the Gallery API returned public version `0.1.0`.
5. If using `vsce publish` for later releases, store the token only as `VSCE_PAT` for the publish session.
6. Current follow-up on 2026-06-16: Open VSX latest is `0.1.1`, and Visual Studio Marketplace latest is also `0.1.1`. Marketplace synchronization is verified by the publisher page and Gallery API.

## Publish commands

```bash
npx --yes ovsx publish microcosting_healthservices/integrations/vscode/mchs-tools-0.1.1.vsix --pat "$OVSX_PAT"
npx --yes @vscode/vsce publish --packagePath microcosting_healthservices/integrations/vscode/mchs-tools-0.1.1.vsix --pat "$VSCE_PAT"
```

For future Marketplace releases, upload the prepared artifact and verify the Gallery API reports the target version before claiming publication.

## Evidence to record

- Open VSX publisher agreement completion date
- Eclipse linked GitHub username evidence
- Open VSX publisher name and token creation confirmation
- Visual Studio Marketplace publisher ID
- Marketplace publisher ID and extension ID
- Publish command output or web-upload confirmation
- Public listing URLs for Open VSX and Marketplace version `0.1.1`

## Completion rule

Do not mark a future release complete until the tokens exist for that release or a web upload has completed, and public version evidence is visible in both registries if both destinations are required.
