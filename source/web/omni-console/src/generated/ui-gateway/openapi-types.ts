/**
 * Source-shaped architecture note.
 *
 * Retained source path: web/omni-console/src/generated/ui-gateway/openapi-types.ts
 * System layer: Productization Boundary Layer - generated API/read-model contracts
 * Review role: gateway client and backend contract boundary; generated OpenAPI type boundary.
 *
 * Structural signals retained from the implementation file:
 * - exported interfaces/types/classes: paths, components, operations, webhooks, $defs.
 * - exported functions/components/constants: none visible at this abstraction level.
 * - local helper functions: none visible at this abstraction level.
 *
 * Reviewable responsibilities:
 * - Represents generated client or catalog surface used by the console.
 * - Keeps API shape reviewable without exposing backend implementation logic.
 * - Separates generated read-model access from hand-written page behavior.
 * - Exposes named TypeScript/React symbols that make the module boundary inspectable.
 *
 * Deliberate redaction boundary:
 * - implementation body, component markup, request details, constants, thresholds, credentials, local paths, and runtime data are not included.
 * - the retained value is the real file name, real module ownership, and real top-level structural shape.
 */
