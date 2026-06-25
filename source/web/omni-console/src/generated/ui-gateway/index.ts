/**
 * Source-shaped architecture note.
 *
 * Retained source path: web/omni-console/src/generated/ui-gateway/index.ts
 * System layer: Productization Boundary Layer - generated API/read-model contracts
 * Review role: gateway client and backend contract boundary.
 *
 * Structural signals retained from the implementation file:
 * - exported interfaces/types/classes: none visible at this abstraction level.
 * - exported functions/components/constants: none visible at this abstraction level.
 * - local helper functions: none visible at this abstraction level.
 *
 * Reviewable responsibilities:
 * - Represents generated client or catalog surface used by the console.
 * - Keeps API shape reviewable without exposing backend implementation logic.
 * - Separates generated read-model access from hand-written page behavior.
 *
 * Contract shape:
 * - Inputs: typed request state, read-model payload, operator action, route parameter, or gateway response fixture.
 * - Outputs: normalized UI state, typed client result, fail-closed error state, validation signal, or reviewable read-model update.
 * Deliberate redaction boundary:
 * - implementation body, component markup, request details, constants, thresholds, credentials, local paths, and runtime data are not included.
 * - the retained value is the real file name, real module ownership, and real top-level structural shape.
 */
