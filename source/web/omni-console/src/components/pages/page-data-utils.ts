/**
 * Source-shaped architecture note.
 *
 * Retained source path: web/omni-console/src/components/pages/page-data-utils.ts
 * System layer: Productization Boundary Layer - operator console pages and research workflow surfaces
 * Review role: operator page composition boundary.
 *
 * Structural signals retained from the implementation file:
 * - exported interfaces/types/classes: none visible at this abstraction level.
 * - exported functions/components/constants: asObject, asArray, asString, asNumber, asBoolean, unwrapData, extractObjectArray, toPrettyJson.
 * - local helper functions: none visible at this abstraction level.
 *
 * Reviewable responsibilities:
 * - Owns the page data utils console page boundary and page-level composition.
 * - Connects user-visible state to typed gateway/read-model contracts.
 * - Keeps operational actions behind explicit policy, availability, or fail-closed signals.
 * - Exposes named TypeScript/React symbols that make the module boundary inspectable.
 *
 * Deliberate redaction boundary:
 * - implementation body, component markup, request details, constants, thresholds, credentials, local paths, and runtime data are not included.
 * - the retained value is the real file name, real module ownership, and real top-level structural shape.
 */
