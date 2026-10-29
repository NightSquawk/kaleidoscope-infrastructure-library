# Kaleidoscope Infrastructure Library

Community hardware definitions, original SVG faceplates and port-level layouts for infrastructure digital twins.

## Starter contents
- Five generic devices: 2U server, 24-port switch, 24-port patch panel, 2U UPS and 0U vertical PDU.
- Eight original connector SVGs: RJ45, SFP, USB-A, USB-C, VGA, HDMI, IEC C14 inlet and IEC C13 outlet.
- Front/rear faceplates and separate port IDs, positions, dimensions and roles.
- A byte-preserved NetBox Dell R750 definition with pinned revision and provenance. It is not yet a verified visual R750 template.
- An offline interactive preview with view switching, keyboard-selectable ports and clearly labeled simulated health states.
- License/file-integrity checks, template validation, release packaging and regression tests.

## Run (Python 3.11+, no dependencies)
```sh
python tooling/validate.py
python -m unittest discover -s tests -v
python tooling/preview.py
# Open dist/preview.html in your browser.
python tooling/release.py
```

All generic dimensions and layouts are illustrative, not manufacturer specifications. Actual measurements must be verified before physical planning. Empty generic rear views do not mean a real device has no rear ports. No runtime observations or customer inventory belong in this library.

## Authoring
Edit templates in catalog/kaleidoscope/CC0-1.0/devices/. Artwork uses a 1000-wide front/rear viewBox (0U PDU uses a tall viewBox). Each port has a stable ID, role, connector and face-local bounding box. Metadata references connector artwork; background faceplates contain no permanent health colors. Preview inserts clickable connectors and status markers at runtime.

Use a distinct template or future module variant for changed hardware; do not silently move port IDs. Width and depth are explicit millimetres, separate from U height. A 0U PDU has physical height but consumes no rack units. Generic presets do not establish actual rack clearance.

## Contribution workflow
See CONTRIBUTING.md and LICENSING.md. Register new files in asset-manifest.json with correct origin and rights information. Then explicitly refresh hashes with `python tooling/refresh_hashes.py`, review the diff and run checks. CI never refreshes hashes automatically.

## Next milestones
Verify model-specific layouts; add a module-slot schema and authoring editor; add approved imports and assets; integrate a renderer with Kaleidoscope SVG/Three.js views. These are not implemented in this starter.
