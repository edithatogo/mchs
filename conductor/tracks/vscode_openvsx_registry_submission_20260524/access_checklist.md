# Open VSX / Visual Studio Marketplace Access Checklist

This checklist captures the account and token state required to complete publisher access and publication evidence for `mchs-tools`.

Current status: Open VSX API exposes `edithatogo.mchs-tools` version `0.1.1`. Visual Studio Marketplace `0.1.1` was manually uploaded through the publisher portal and still needs stable public API/page propagation evidence before the combined track can close.

## Open VSX

1. Sign in to an Eclipse Foundation account that will own the publisher identity.
2. Complete the Open VSX Publisher Agreement.
   - Agreement: https://open-vsx.org/publisher-agreement-v1.1
3. Link GitHub account `edithatogo` to Eclipse account `edithatogo`.
   - Completed on 2026-06-12: Eclipse reported "Account successfully connected with Github Account" and "Connected as edithatogo".
4. Complete the Open VSX Profile page's agreement-recognition flow.
   - Resolved on 2026-06-13: publisher agreement recognition allowed token creation.
5. Return to the Open VSX publisher settings and create an access token for publishing.
   - Completed for the current repository: `OVSX_PAT` is configured as a GitHub repository secret.
6. Verify the Open VSX public API exposes the latest intended version before claiming completion.
   - Verified evidence: `https://open-vsx.org/api/edithatogo/mchs-tools` exposes version `0.1.1`.

## Visual Studio Marketplace

1. Sign in to the Visual Studio Marketplace publishing portal with the intended publisher identity.
2. Create or recover the publisher entry if one does not already exist.
3. Create a Personal Access Token with marketplace publish permissions if automated publication is required.
4. Store the token only as `VSCE_PAT` for the publish session.
5. Verify the publisher profile can access the token management page before attempting an automated publish.
6. If the package is uploaded manually through the publisher portal, record portal validation state and public API propagation separately.

## Publish commands

```bash
npx --yes ovsx publish microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix --pat "$OVSX_PAT"
npx --yes @vscode/vsce publish --packagePath microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix --pat "$VSCE_PAT"
```

## Evidence to record

- Open VSX publisher agreement completion date
- Eclipse linked GitHub username evidence
- Open VSX publisher name, token creation confirmation, and public API version evidence
- Visual Studio Marketplace publisher ID
- Marketplace PAT scope and expiry, or manual-upload portal evidence
- Publish command output
- Public listing URLs for Open VSX and Marketplace version `0.1.0`

## Completion rule

Do not mark the track complete until public version evidence is visible in every required registry. Open VSX and Visual Studio Marketplace may have different completion states; record partial publication without treating it as full completion.
