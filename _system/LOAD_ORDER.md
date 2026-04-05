# Load Order

Use this order to bootstrap quickly without wasting context.

## Tier 0: Operating contract

1. `AGENTS.md`
2. `_system/INSTRUCTION_PRECEDENCE_CONTRACT.md`
3. `_system/REPO_OPERATING_PROFILE.md`
4. `_system/PROJECT_PROFILE.md`
5. `_system/CONTEXT_INDEX.md`
6. `_system/KEY.md`
7. `_system/LOAD_ORDER.md`
8. `_system/WORKING_FILES_GUIDE.md`
9. `_system/TEMPLATE_NEUTRALITY_POLICY.md`
10. `_system/MASTER_SYSTEM_PROMPT.md`
11. `_system/PROJECT_RULES.md`
12. `_system/MEMORY_RULES.md`
13. `_system/EXECUTION_PROTOCOL.md`
14. `_system/MULTI_AGENT_COORDINATION.md`
15. `_system/AGENT_ROLE_CATALOG.md`
16. `_system/AGENT_DISCOVERY_MATRIX.md`
17. `_system/SYSTEM_AWARENESS_PROTOCOL.md`
18. `_system/HALLUCINATION_DEFENSE_PROTOCOL.md`

## Tier 1: Current working state

19. `WHERE_LEFT_OFF.md`
20. `TODO.md`
21. `FIXME.md`
22. `PLAN.md`
23. `PRODUCT_BRIEF.md`
24. `ROADMAP.md`
25. `DESIGN_NOTES.md`
26. `ARCHITECTURE_NOTES.md`
27. `RESEARCH_NOTES.md`
28. `TEST_STRATEGY.md`
29. `RISK_REGISTER.md`
30. `RELEASE_NOTES.md`
31. `CHANGELOG.md`
32. `_system/context/CURRENT_STATUS.md`
33. `_system/context/DECISIONS.md`
34. `_system/context/MEMORY.md`
35. `_system/context/ARCHITECTURAL_INVARIANTS.md`
36. `_system/context/ASSUMPTIONS.md`
37. `_system/context/INTEGRATION_SURFACES.md`
38. `_system/context/OPEN_QUESTIONS.md`
39. `_system/context/QUALITY_DEBT.md`

## Tier 2: Execution references

40. `_system/VALIDATION_GATES.md`
41. `_system/HANDOFF_PROTOCOL.md`
42. `_system/DEBUG_REPAIR_PLAYBOOK.md`
43. `_system/CHECKPOINT_PROTOCOL.md`
44. `_system/REPO_BOUNDARY_AND_BACKUP.md`
45. `_system/GIT_REMOTE_AND_SYNC_PROTOCOL.md` — remotes, SSH, fetch/pull/push when sharing work
46. `_system/MCP_CONFIG.md`
47. `_system/SECURITY_REDACTION_AND_AUDIT.md`
48. `_system/PROVENANCE_AND_EVIDENCE.md`
49. `_system/DESIGN_EXCELLENCE_FRAMEWORK.md`
50. `_system/RELEASE_READINESS_PROTOCOL.md`
51. `_system/FAILURE_MODES_AND_RECOVERY.md`
52. `_system/CODING_STANDARDS.md`
53. `_system/PERFORMANCE_BUDGET.md`
54. `_system/ACCESSIBILITY_STANDARDS.md`
55. `_system/API_DESIGN_STANDARDS.md`
56. `_system/DEPENDENCY_GOVERNANCE.md`
57. `_system/MODERN_UI_PATTERNS.md`
58. `_system/OBSERVABILITY_STANDARDS.md`
59. `_system/SECURITY_HARDENING_CONTRACT.md`
60. `_system/THREAT_MODEL_TEMPLATE.md`
61. `_system/INSTALLATION_GUIDE.md`
62. `_system/PACKAGING_GUIDE.md`
63. `_system/CROSS_PLATFORM_DISTRIBUTION_AND_INSTALLER_STANDARD.md`
64. `_system/SUB_AGENT_HOST_DELEGATION.md`
65. `_system/MOBILE_GUIDE.md`
66. `_system/CHATBOT_GUIDE.md`
67. `_system/PLUGIN_CONTRACT.md`
68. `_system/SYSTEM_REGISTRY.json`

## Tier 3: Prompting and tooling

69. `_system/PROMPTS_INDEX.md`
70. `_system/PROMPT_EMISSION_CONTRACT.md`
71. `_system/SKILLS_INDEX.md`
72. `_system/review-playbooks/`
73. `_system/prompt-templates/`
74. `_system/prompt-packs/`
75. `_system/ci/`
76. `_system/packaging/`
77. `_system/systemd/`
78. `_system/starter-blueprints/`
79. `bootstrap/system-doctor.sh`
80. `bootstrap/validate-instruction-layer.sh`
81. `bootstrap/detect-instruction-conflicts.sh`
82. `bootstrap/check-runtime-foundations.sh`
83. `bootstrap/check-evidence-quality.sh`
84. `bootstrap/check-working-file-staleness.sh`
85. `bootstrap/check-bootstrap-permissions.sh`
86. `.cursor/` rules, commands, skills, and agents if using Cursor (include Composer-oriented rules when using Composer)

## Targeted optional load

When the task is greenfield bootstrap, system evolution, prompt-authoring, skill-authoring, or working-file drafting, also load:

87. `_system/GOLDEN_EXAMPLES_POLICY.md`
88. `_system/golden-examples/PATTERN_INDEX.md`
89. relevant files under `_system/golden-examples/patterns/` or `_system/golden-examples/working-files/`
90. `_system/HOST_ADAPTER_POLICY.md` when the task changes tool-entry or adapter-load surfaces
91. `_system/HOST_BUNDLE_CONTRACT.md` when the task changes external host-export or bundle surfaces
92. `_system/design-system/THEME_GOVERNANCE.md` when changing global theme tokens or doing a visual overhaul
93. `_system/ports/PORT_POLICY.md` when adding Docker Compose, host publishes, or systemd socket ports
94. `_system/AUTH_AND_ONBOARDING_PATTERNS.md` when adding login, registration, guest mode, or dev-only seed admins

## Onboarding (load on demand)

95. `_system/INSTALLER_AND_UPGRADE_CONTRACT.md` — install, upgrade, repair, and state preservation
96. `_system/QUICKSTART.md` — 1-page onboarding
97. `_system/ARCHITECTURE_DIAGRAM.md` — visual system overview
98. `_system/TROUBLESHOOTING.md` — symptom-based FAQ
99. `_system/MIGRATION_GUIDE.md` — migration paths from other setups

## Fast path

If capacity is tight, load Tier 0 first, then `WHERE_LEFT_OFF.md`, `TODO.md`, `FIXME.md`, `PLAN.md`, and `PRODUCT_BRIEF.md`.

For context-budget-constrained models, use `bootstrap/emit-tiered-context.sh . --tier <A|B|C|D>` or `--model <name>` to get the appropriate load sequence. See `_system/CONTEXT_BUDGET_STRATEGY.md` for tier definitions.
