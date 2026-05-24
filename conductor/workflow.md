# Project Workflow

## Guiding Principles

1. **The Plan is the Source of Truth:** All work must be tracked in `plan.md`
2. **The Tech Stack is Deliberate:** Changes to the tech stack must be documented in `tech-stack.md` *before* implementation
3. **Test-Driven Development:** Write unit tests before implementing functionality
4. **High Code Coverage:** Aim for >80% code coverage for all modules in the short term, with a planned maturity target of >90% coverage as the library stabilizes
5. **User Experience First:** Every decision should prioritize user experience
6. **Non-Interactive & CI-Aware:** Prefer non-interactive commands. Use `CI=true` for watch-mode tools (tests, linters) to ensure single execution.
7. **Transitional-State vs Intended-State Tooling:** Clearly distinguish temporary compatibility tooling from intended-state tooling. Do not describe legacy files, compatibility shims, or migration-only tools as authoritative once the replacement track has defined the target state.
8. **Roadmap Governance:** Large roadmap additions must be classified and sequenced using `roadmap-governance.md`. Do not mark roadmap, scaffold, or publication work complete unless the required contract and evidence exist.
9. **Subagent Accountability:** When subagents are used, assignments must follow `subagent-orchestration.md`. Delegated work must include implementation, tests or validation evidence, documentation, review, and handoff requirements where applicable.

## Task Workflow

All tasks follow a strict lifecycle:

### Standard Task Workflow

1. **Select Task:** Choose the next available task from `plan.md` in sequential order

   For roadmap-heavy work, first confirm that the track class, dependencies,
   contract, and completion evidence are stated. If they are missing, update the
   track before implementation.

   If using subagents, define their roles, model preference, owned files,
   out-of-scope areas, acceptance criteria, and handoff requirements before they
   start.

2. **Mark In Progress:** Before beginning work, edit `plan.md` and change the task from `[ ]` to `[~]`

3. **Write Failing Tests (Red Phase):**
   - Create a new test file for the feature or bug fix.
   - Write one or more unit tests that clearly define the expected behavior and acceptance criteria for the task.
   - **CRITICAL:** Run the tests and confirm that they fail as expected. This is the "Red" phase of TDD. Do not proceed until you have failing tests.

4. **Implement to Pass Tests (Green Phase):**
   - Write the minimum amount of application code necessary to make the failing tests pass.
   - Run the test suite again and confirm that all tests now pass. This is the "Green" phase.

5. **Refactor (Optional but Recommended):**
   - With the safety of passing tests, refactor the implementation code and the test code to improve clarity, remove duplication, and enhance performance without changing the external behavior.
   - Rerun tests to ensure they still pass after refactoring.

6. **Verify Coverage:** Run coverage reports using the project's chosen tools. For example, in a Python project, this might look like:
   ```bash
   uv sync --locked --group dev --group test --group coverage --group typing --group property --group mutation --group profiling --group docs
   uv run pytest --cov=nwau_py --cov-report=term-missing --cov-report=xml --cov-fail-under=80
   ```
   Target: >80% coverage for new code in the short term. As the library matures, raise the target toward >90% coverage, especially for core calculator logic, validation, and source-parity behavior. The specific tools and commands will vary by language and framework.

   For Rust code, run `cargo fmt --all --check`, `cargo clippy --all-targets --all-features -- -D warnings`, and `cargo test` against the committed workspace.

7. **Document Deviations:** If implementation differs from tech stack:
   - **STOP** implementation
   - Update `tech-stack.md` with a new design or a dated transitional-state note
   - Make it explicit whether the change is transitional-state compatibility or intended-state tooling
   - Resume implementation

8. **Commit Code Changes:**
   - Stage all code changes related to the task.
   - Propose a clear, concise commit message e.g, `feat(ui): Create basic HTML structure for calculator`.
   - Perform the commit.

9. **Attach Task Summary with Git Notes:**
   - **Step 9.1: Get Commit Hash:** Obtain the hash of the *just-completed commit* (`git log -1 --format="%H"`).
   - **Step 9.2: Draft Note Content:** Create a detailed summary for the completed task. This should include the task name, a summary of changes, a list of all created/modified files, and the core "why" for the change.
   - **Step 9.3: Attach Note:** Use the `git notes` command to attach the summary to the commit.
     ```bash
     # The note content from the previous step is passed via the -m flag.
     git notes add -m "<note content>" <commit_hash>
     ```

10. **Get and Record Task Commit SHA:**
    - **Step 10.1: Update Plan:** Read `plan.md`, find the line for the completed task, update its status from `[~]` to `[x]`, and append the first 7 characters of the *just-completed commit's* commit hash.
    - **Step 10.2: Write Plan:** Write the updated content back to `plan.md`.

11. **Commit Plan Update:**
    - **Action:** Stage the modified `plan.md` file.
    - **Action:** Commit this change with a descriptive message (e.g., `conductor(plan): Mark task 'Create user model' as complete`).

### Phase Completion Verification and Checkpointing Protocol

**Trigger:** This protocol is executed immediately after a task is completed that also concludes a phase in `plan.md`.

**Mandatory Automation Rule:** Every phase boundary must automatically invoke
`conductor-review` before checkpointing. The phase is not complete until
`conductor-review` has inspected the phase against the active `spec.md`,
`plan.md`, `workflow.md`, changed files, and validation commands; applied every
high-confidence fix directly; rerun the narrowest validation that proves those
fixes; and returned control without unresolved blockers. Do not ask for manual
confirmation between phase completion, review, fix application, validation,
checkpointing, and progression to the next phase unless the bounded retry budget
is exhausted or a risky design decision cannot be resolved from local context.

1.  **Announce Protocol Start:** Inform the user that the phase is complete and the verification and checkpointing protocol has begun.

2.  **Ensure Test Coverage for Phase Changes:**
    -   **Step 2.1: Determine Phase Scope:** To identify the files changed in this phase, you must first find the starting point. Read `plan.md` to find the Git commit SHA of the *previous* phase's checkpoint. If no previous checkpoint exists, the scope is all changes since the first commit.
    -   **Step 2.2: List Changed Files:** Execute `git diff --name-only <previous_checkpoint_sha> HEAD` to get a precise list of all files modified during this phase.
    -   **Step 2.3: Verify and Create Tests:** For each file in the list:
        -   **CRITICAL:** First, check its extension. Exclude non-code files (e.g., `.json`, `.md`, `.yaml`).
        -   For each remaining code file, verify a corresponding test file exists.
        -   If a test file is missing, you **must** create one. Before writing the test, **first, analyze other test files in the repository to determine the correct naming convention and testing style.** The new tests **must** validate the functionality described in this phase's tasks (`plan.md`).

3.  **Execute Automated Tests with Proactive Debugging:**
    -   Before execution, you **must** announce the exact shell command you will use to run the tests.
    -   **Example Announcement:** "I will now run the automated test suite to verify the phase. **Command:** `uv run pytest --cov=nwau_py --cov-report=term-missing --cov-report=xml`"
    -   Execute the announced command.
    -   If tests fail, you **must** inform the user and begin debugging. You may attempt to propose a fix a **maximum of two times**. If the tests still fail after your second proposed fix, you **must stop**, report the persistent failure, and ask the user for guidance.

4.  **Run `conductor-review` and Auto-Fix:**
    -   Automatically use the `conductor-review` skill to inspect the current phase or track against the spec, plan, workflow, tests, changed files, and applicable validation commands.
    -   Apply every high-confidence fix directly without asking for permission.
    -   Rerun the narrowest validation that proves the fix, escalating to broader validation only when the changed surface requires it.
    -   Re-review the updated diff and validation output after each fix.
    -   Repeat the review-fix-validation loop until the work is stable or the bounded retry budget is exhausted.
    -   If `conductor-review` reports no unresolved blockers, continue directly to checkpointing.
    -   If `conductor-review` reports an unresolved blocker after bounded retries, stop, report findings first, and do not checkpoint or advance.

5.  **Create Checkpoint Commit:**
    -   Stage all changes. If no changes occurred in this step, proceed with an empty commit.
    -   Perform the commit with a clear and concise message (e.g., `conductor(checkpoint): Checkpoint end of Phase X`).

6.  **Attach Auditable Verification Report using Git Notes:**
    -   **Step 6.1: Draft Note Content:** Create a detailed verification report including the automated test command, the `conductor-review` findings, and the fixes applied.
    -   **Step 6.2: Attach Note:** Use the `git notes` command and the full commit hash from the previous step to attach the full report to the checkpoint commit.

7.  **Get and Record Phase Checkpoint SHA:**
    -   **Step 7.1: Get Commit Hash:** Obtain the hash of the *just-created checkpoint commit* (`git log -1 --format="%H"`).
    -   **Step 7.2: Update Plan:** Read `plan.md`, find the heading for the completed phase, and append the first 7 characters of the commit hash in the format `[checkpoint: <sha>]`.
    -   **Step 7.3: Write Plan:** Write the updated content back to `plan.md`.

8. **Commit Plan Update:**
    - **Action:** Stage the modified `plan.md` file.
    - **Action:** Commit this change with a descriptive message following the format `conductor(plan): Mark phase '<PHASE NAME>' as complete`.

9.  **Auto-Advance:** Once the checkpoint is recorded, automatically continue with the next incomplete task or next track. If the active track still has incomplete work, continue with the next incomplete phase or task inside that track before moving on. Do not pause for manual confirmation unless the workflow is blocked by missing context, a failing bounded retry, or a risky design decision that cannot be resolved from local context.

10.  **Announce Completion:** Inform the user that the phase is complete and the checkpoint has been created, with the detailed automated review report attached as a git note.

### Quality Gates

Before marking any task complete, verify:

- [ ] All tests pass
- [ ] Code coverage meets requirements (>80%)
- [ ] Code follows project's code style guidelines (as defined in `code_styleguides/`)
- [ ] All public functions/methods are documented (e.g., docstrings, JSDoc, GoDoc)
- [ ] Type safety is enforced (e.g., type hints, TypeScript types, Go types)
- [ ] No linting or static analysis errors (using the project's configured tools)
- [ ] Works correctly on mobile (if applicable)
- [ ] Documentation updated if needed
- [ ] No security vulnerabilities introduced
- [ ] Track class, dependencies, explicit contract, and completion evidence are recorded for roadmap or governance work
- [ ] Pricing-year validation claims include SAS parity and Excel formula parity where those sources are available, or explicit gap records where they are not
- [ ] Bindings, apps, and examples consume shared contracts rather than duplicating formula logic
- [ ] Subagent handoffs include changed files, validations, documentation updates, review findings, and residual risks when subagents were used

## Development Commands

Use the locked Python commands below for setup, daily development, and pre-commit verification.

### Setup
```bash
uv sync --locked --group dev --group test --group coverage --group typing --group property --group mutation --group profiling --group docs
uv lock
```

### Daily Development
```bash
uv sync --locked --group dev --group test --group coverage --group typing --group property --group mutation --group profiling --group docs
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest
uv run pytest --cov=nwau_py --cov-report=term-missing --cov-report=xml --cov-fail-under=80
cd rust && cargo fmt --all --check
cd rust && cargo clippy --all-targets --all-features -- -D warnings
cd rust && cargo test
uv run vale conductor README.md docs
```

### Slow Validation
The repository also defines a manual and scheduled slow-validation workflow for property, mutation, and profiling checks.

- Trigger it with `workflow_dispatch` or the weekly schedule in `.github/workflows/slow-validation.yml`.
- Property checks use `uv sync --locked --group test --group property` followed by `uv run pytest`.
- Mutation checks use `uv sync --locked --group test --group mutation` followed by `uv run mutmut run`.
- Profiling checks use `uv sync --locked --group test --group profiling` followed by `mkdir -p .cache/validation/scalene && uv run scalene --cli --outfile .cache/validation/scalene/scalene.out --html python -m pytest`.
- Treat `.cache/validation/scalene/` as generated output and do not commit the profiling artifacts.

### Maintenance Automation
Phase 4 treats maintenance automation as part of the quality gate, not as a separate afterthought.

- **Renovate** keeps dependency and GitHub Actions updates flowing through reviewable pull requests; treat each update as a validation event when it can affect calculator behavior, tooling, or documentation output.
- **Vale** enforces prose quality and validation-language discipline; run it locally before committing and require it to pass when phase 4 documents or claims validation status changes.
- Phase 4 is complete only when the Renovate configuration is in place, Vale is wired into the documentation gate, and the workflow text makes their roles explicit.

### Before Committing
```bash
uv sync --locked --group dev --group test --group coverage --group typing --group property --group mutation --group profiling --group docs
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest --cov=nwau_py --cov-report=term-missing --cov-report=xml --cov-fail-under=80
cd rust && cargo fmt --all --check
cd rust && cargo clippy --all-targets --all-features -- -D warnings
cd rust && cargo test
uv run vale conductor README.md docs
```

## Testing Requirements

### Unit Testing
- Every module must have corresponding tests.
- Use appropriate test setup/teardown mechanisms (e.g., fixtures, beforeEach/afterEach).
- Mock external dependencies.
- Test both success and failure cases.

### Integration Testing
- Test complete user flows
- Verify database transactions
- Test authentication and authorization
- Check form submissions

### Mobile Testing
- Test on actual iPhone when possible
- Use Safari developer tools
- Test touch interactions
- Verify responsive layouts
- Check performance on 3G/4G

## Code Review Process

### Self-Review Checklist
Before requesting review:

1. **Functionality**
   - Feature works as specified
   - Edge cases handled
   - Error messages are user-friendly

2. **Code Quality**
   - Follows style guide
   - DRY principle applied
   - Clear variable/function names
   - Appropriate comments

3. **Testing**
   - Unit tests comprehensive
   - Integration tests pass
   - Coverage adequate (>80%)

4. **Security**
   - No hardcoded secrets
   - Input validation present
   - SQL injection prevented
   - XSS protection in place

5. **Performance**
   - Database queries optimized
   - Images optimized
   - Caching implemented where needed

6. **Mobile Experience**
   - Touch targets adequate (44x44px)
   - Text readable without zooming
   - Performance acceptable on mobile
   - Interactions feel native

## Commit Guidelines

### Message Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Maintenance tasks

### Examples
```bash
git commit -m "feat(auth): Add remember me functionality"
git commit -m "fix(posts): Correct excerpt generation for short posts"
git commit -m "test(comments): Add tests for emoji reaction limits"
git commit -m "style(mobile): Improve button touch targets"
```

## Definition of Done

A task is complete when:

1. All code implemented to specification
2. Unit tests written and passing
3. Code coverage meets project requirements
4. Documentation complete (if applicable)
5. Code passes all configured linting and static analysis checks
6. Works beautifully on mobile (if applicable)
7. Implementation notes added to `plan.md`
8. Changes committed with proper message
9. Git note with task summary attached to the commit

## Emergency Procedures

### Critical Bug in Production
1. Create hotfix branch from main
2. Write failing test for bug
3. Implement minimal fix
4. Test thoroughly including mobile
5. Deploy immediately
6. Document in plan.md

### Data Loss
1. Stop all write operations
2. Restore from latest backup
3. Verify data integrity
4. Document incident
5. Update backup procedures

### Security Breach
1. Rotate all secrets immediately
2. Review access logs
3. Patch vulnerability
4. Notify affected users (if any)
5. Document and update security procedures

## Deployment Workflow

### Pre-Release Checklist
- [ ] `uv run ruff format --check .` passes
- [ ] `uv run ruff check .` passes
- [ ] `uv run ty check` passes
- [ ] `uv run pytest --cov=nwau_py --cov-report=term-missing --cov-report=xml --cov-fail-under=80` passes
- [ ] `uv run vale conductor README.md docs` passes
- [ ] Coverage report is uploaded to Codecov from CI

### Release Steps
1. Merge the validated feature branch to `main`
2. Tag the release with the package version
3. Build the distribution with `uv build`
4. Verify installability with `uv sync --locked`
5. Publish the release artifacts and associated checksums
6. Verify the release notes capture calculator, data bundle, and validation changes

### Post-Release
1. Confirm CI is green on the release commit
2. Check source checksum and artifact provenance records
3. Record any follow-up validation work in `plan.md`

## Continuous Improvement

- Review workflow weekly
- Update based on pain points
- Document lessons learned
- Optimize for user happiness
- Keep things simple and maintainable
