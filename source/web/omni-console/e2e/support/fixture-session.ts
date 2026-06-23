/**
 * Source-shaped architecture note.
 *
 * Retained source path: web/omni-console/e2e/support/fixture-session.ts
 * System layer: Validation Layer - browser-level workflow and host-safety checks
 * Review role: test fixture and session boundary.
 *
 * Structural signals retained from the implementation file:
 * - exported interfaces/types/classes: none visible at this abstraction level.
 * - exported functions/components/constants: installFixtureSessionState, resolveAppUrl, gotoAppRoute, LAUNCH_GATE_STATE_KEY, SESSION_STORAGE_KEY, launchGateState, sessionState.
 * - local helper functions: none visible at this abstraction level.
 *
 * Reviewable responsibilities:
 * - Defines browser validation support for host-safe console workflows.
 * - Captures test-session contracts and fixture wiring without runtime secrets or local state.
 * - Checks product surfaces through stable selectors and typed expectations.
 * - Exposes named TypeScript/React symbols that make the module boundary inspectable.
 * - Participates in a composed dependency graph; import targets are not copied into this file body.
 *
 * Deliberate redaction boundary:
 * - implementation body, component markup, request details, constants, thresholds, credentials, local paths, and runtime data are not included.
 * - the retained value is the real file name, real module ownership, and real top-level structural shape.
 */
