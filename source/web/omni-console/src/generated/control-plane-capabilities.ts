/**
 * Source-shaped architecture note.
 *
 * Retained source path: web/omni-console/src/generated/control-plane-capabilities.ts
 * System layer: Productization Boundary Layer - generated API/read-model contracts
 * Review role: control-plane API and read-model boundary.
 *
 * Structural signals retained from the implementation file:
 * - exported interfaces/types/classes: ControlPlanePageCapability, SemanticPermissionCapability, AutoUnblockActionCapability, AutomationTaskCapability, SkillProfileCapability, PermissionModeCapability, UiRoleModeCapability, CommandPermissionRuleCapability, SessionStoreCapability, RuntimeCapability, PagePathParamBindingCapability, PageContractAdapterCapability, plus 1 more.
 * - exported functions/components/constants: CONTROL_PLANE_PAGE_CAPABILITIES, CONTROL_PLANE_PAGE_FALLBACK_OPERATION_IDS, CONTROL_PLANE_SEMANTIC_PERMISSIONS, AUTOMATION_AUTO_UNBLOCK_ACTION_CAPABILITIES, AUTOMATION_RAIL_TASK_CAPABILITIES, CONTROL_PLANE_SKILL_PROFILES, CONTROL_PLANE_PERMISSION_MODES, CONTROL_PLANE_UI_ROLE_CURRENT_MODES, CONTROL_PLANE_COMMAND_PERMISSION_RULES, CONTROL_PLANE_SESSION_STORE, CONTROL_PLANE_RUNTIME_CAPABILITIES, CONTROL_PLANE_PAGE_CONTRACT_ADAPTERS, plus 1 more.
 * - local helper functions: none visible at this abstraction level.
 *
 * Reviewable responsibilities:
 * - Represents generated client or catalog surface used by the console.
 * - Keeps API shape reviewable without exposing backend implementation logic.
 * - Separates generated read-model access from hand-written page behavior.
 * - Exposes named TypeScript/React symbols that make the module boundary inspectable.
 * - Participates in a composed dependency graph; import targets are not copied into this file body.
 *
 * Deliberate redaction boundary:
 * - implementation body, component markup, request details, constants, thresholds, credentials, local paths, and runtime data are not included.
 * - the retained value is the real file name, real module ownership, and real top-level structural shape.
 */
