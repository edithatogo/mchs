# Playwright Runtime Smoke Scaffold

This folder defines the runtime smoke contract for the Power Platform app. It is
not a production pass claim.

The smoke suite replaces new investment in deprecated Test Engine assumptions
with browser-level checks that can run against the real Power Apps URL once NSW
app component and sharing evidence exists.

Required smoke coverage:

- App launches for an authorized NSW user.
- Connector consent or preconsented connection state is visible.
- Happy-path synthetic calculation submission succeeds.
- Validation failure is shown for invalid synthetic input.
- Evidence export flow is reachable.
- No private NSW patient or operational data is stored in the app or flow.
- Visual function is reviewed for responsive layout, loading states, error
  clarity, keyboard navigation, contrast, and support correlation IDs.
