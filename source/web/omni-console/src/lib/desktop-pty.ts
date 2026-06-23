/**
 * Source-shaped architecture note.
 *
 * Retained source path: web/omni-console/src/lib/desktop-pty.ts
 * System layer: Productization Boundary Layer - typed UI client, fail-closed state, and read-model helpers
 * Review role: desktop host integration surface.
 *
 * Structural signals retained from the implementation file:
 * - exported interfaces/types/classes: none visible at this abstraction level.
 * - exported functions/components/constants: listenPtyOutput, listenPtyExit, listenWorkspaceSync, DESKTOP_PTY_OUTPUT_EVENT, DESKTOP_PTY_EXIT_EVENT, DESKTOP_WORKSPACE_EVENT, createDesktopPtySession, listDesktopPtySessions, writeDesktopPtySession, resizeDesktopPtySession, closeDesktopPtySession.
 * - local helper functions: none visible at this abstraction level.
 *
 * Reviewable responsibilities:
 * - Defines reusable UI-side contracts, gateway helpers, runtime adapters, or state normalization.
 * - Keeps backend interaction typed and centralized rather than embedded across pages.
 * - Provides a stable surface for operator pages, generated clients, and validation tests.
 * - Exposes named TypeScript/React symbols that make the module boundary inspectable.
 * - Participates in a composed dependency graph; import targets are not copied into this file body.
 *
 * Deliberate redaction boundary:
 * - implementation body, component markup, request details, constants, thresholds, credentials, local paths, and runtime data are not included.
 * - the retained value is the real file name, real module ownership, and real top-level structural shape.
 */
