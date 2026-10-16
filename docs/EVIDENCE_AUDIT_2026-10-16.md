# Public Cybrary training evidence — integrity review (2026-10-16)

**Repository:** Original (nonfork), public `JimBLogic/Cybrary-IT-Cybersecurity-Certificates-and-Labs`.
**Baseline:** `14f106337351eca1c38cf94561a719c51c66cb7e`. **Branch:** `audit/evidence-link-integrity-20261016`.
**Scope:** No merge, release, portfolio deployment, PDF edits, certification claim upgrades or media uploads.

## Verified inventory
- README lists **9 linked course PDFs** in `Certificates/` and **7 linked training/lab PDFs** in `Labs/`. All referenced paths existed during the repository inspection.
- A separate `Labs/cybrary-cert-welcome-to-cybrary.pdf` exists but is not a listed lab credential. This is intentional, not proof of missing training.
- The original repository had no CI run or automated regression checks for its credential links. This is a **preventive integrity gap**, not evidence of a compromised or broken PDF.
- The README says “Security+: ...” for Cybrary modules. These labels must **not** be confused with passing the independent CompTIA Security+ certification exam.

## Review-only controls
- Four dependency-free stdlib tests confirm exact case-sensitive PDF file names, non-placeholder sizes, uniqueness, ISO date syntax and the one unlisted welcome resource, without opening the PDF bytes.
- GitHub Actions runs tests **only for pull requests**, read-only with pinned `actions/checkout` full SHA and no persisted token. No artifact publishing, PDF parse or external tooling.
- The README clarifies training vs professional certification and explicitly states that path validation cannot authenticate a credential.

## Residual limitations
- These tests do **not** confirm that PDF contents are legitimate, correct for the linked title, issued on the README date, or free of private metadata. Original media and dates remain unchanged.
- The repository is already public: before adding any new personal certificates, the owner should review privacy and permitted disclosure.
- No browser/manual recruitment link-check was run. The automated integrity check verifies only internal paths, not external platform availability.

**DRAFT review only. NO-GO for merge or publication without explicit owner approval.**
