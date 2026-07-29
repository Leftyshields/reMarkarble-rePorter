# Mission — reMarkable Weekly Notes

Turn handwritten **Daily Journal** pages from a reMarkable tablet into a reliable, paste-ready weekly markdown digest.

Every Friday (or on demand), the operator runs a headless job that pulls the latest journal pages, checks that handwritten dates land in the target ISO week, chops long scroll pages for vision, and asks Claude to produce clean categorized notes (to-dos vs meeting notes and related buckets). Output lands as a timestamped file under `weekly-notes/` for manual Confluence paste — no UI, no third-party OCR, no auto-publish in v1.

**Success looks like:** one command, one non-overwriting markdown artifact, trustworthy date warnings, and tests that stay green without live cloud tokens.
