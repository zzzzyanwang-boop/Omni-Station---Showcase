/**
 * Source-shaped architecture note.
 *
 * Retained source path: web/omni-console/src/components/pages/ui027-model-zoo.tsx
 * System layer: Productization Boundary Layer - operator console pages and research workflow surfaces
 * Review role: operator page composition boundary.
 *
 * Structural signals retained from the implementation file:
 * - exported interfaces/types/classes: none visible at this abstraction level.
 * - exported functions/components/constants: Ui027ModelZooPage.
 * - local helper functions: normalizeModelFamily, asObject, asArray, asBoolean, parseTsMs, normalizeStatus, statusTone, toControlState, parseJsonObject, extractJobId, normalizeTrainingCurve, normalizeReadinessChecksFromRow, plus 11 more.
 *
 * Reviewable responsibilities:
 * - Owns the ui027-model-zoo console page boundary and page-level composition.
 * - Connects user-visible state to typed gateway/read-model contracts.
 * - Keeps operational actions behind explicit policy, availability, or fail-closed signals.
 * - Exposes named TypeScript/React symbols that make the module boundary inspectable.
 * - Uses local helpers behind the exported boundary; helper names are retained only as structural signals.
 * - Participates in a composed dependency graph; import targets are not copied into this file body.
 *
 * Deliberate redaction boundary:
 * - implementation body, component markup, request details, constants, thresholds, credentials, local paths, and runtime data are not included.
 * - the retained value is the real file name, real module ownership, and real top-level structural shape.
 */
