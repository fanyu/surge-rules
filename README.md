# surge-assets

Private source repository for self-managed Surge assets.
Contains only static rule files, self-hosted modules, and icon files.

## Layout
- `rules/ads/`: ad blocking rule sets
- `rules/ai/`: AI-related rule sets
- `rules/apple/`: Apple service rule sets split by policy target
- `rules/china/`: China direct-connect rule sets
- `rules/entertainment/`: gaming and streaming rule sets
- `rules/platforms/`: platform-specific rule sets
- `rules/social/`: social platform rule sets
- `rules/network/`: final catch-all proxy rules
- `rules/archive/`: disabled or archived rule sets
- `modules/`: self-hosted `.sgmodule` files, with their scripts in `modules/scripts/`
- `icons/`: strategy group icons

## Self-hosting policy for modules

Modules are code that tracks third-party app APIs, so mirroring everything means
inheriting maintenance for all of it. Vendor a module here only when one of these holds:

1. Upstream is unmaintained or has disappeared.
2. It has been modified locally and upstream updates would overwrite the change.
3. It MITMs a hostname that carries credentials.

Otherwise keep pointing at upstream so fixes arrive automatically.

No subscriptions, credentials, GeoIP databases, domain sets, or config snapshots are stored here.
