/**
 * Source-shaped architecture note.
 *
 * Retained source path: web/omni-console/src/generated/ia-pages.ts
 * System layer: Productization Boundary Layer - generated API/read-model contracts
 * Review role: operator page composition boundary.
 *
 * Structural signals retained from the implementation file:
 * - exported interfaces/types/classes: IaPageCard.
 * - exported functions/components/constants: IA_PAGES, IA_PAGE_MAP.
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
