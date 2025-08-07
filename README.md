# AI Pin Reinvented

This repository re-envisions the Humane AI Pin by developing four novel prototypes that leverage its ultrawide camera, always-on microphone array, Personic speakers, and Laser Ink projector. The goal is to explore gaps beyond current translation and nutrition features and bridge into Samsung's ecosystem.

## Prototype Concepts
1. **Mood-Mirror Coach** – detects vocal stress and posture using the mic and IMU; projects breathing patterns and logs mood to Samsung Health.
2. **Spatial Safety Bubble** – fuses Doppler audio and vision to alert pedestrians of fast approaching bikes or scooters; risk scores can trigger Samsung Watch/SmartThings emergency features.
3. **Stealth Palm-Prompter** – listens to your speech, matches it against your outline and lasers the next bullet onto your hand; syncs notes with Samsung DeX.
4. **Point-&-Pair SmartThings Assist** – reads an appliance's logo/QR code with the camera, fetches pairing instructions from SmartThings, and displays voice commands on your hand; one tap pairs the device via BLE/Wi‑Fi.

## Quick Start
### Python
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r python/requirements.txt
```

Run the mood analysis service:

```bash
cd python
gunicorn -b 0.0.0.0:5000 mood_service:app
```
The above uses Gunicorn for a production-ready server. For quick local testing you can still run `python mood_service.py`.

### Node
```bash
cd node
npm install
npm start
```

Once both servers are running, try the Mood-Mirror API:

```bash
curl "http://localhost:3000/mood?file=sample.wav"
```

Or open the notebook at `python/notebooks/demo_mood_mirror.ipynb`.

## Spatial Safety Bubble
Detect fast-approaching bikes or scooters and warn the pedestrian.

### Example
Generate the sample clip and query the API:
```bash
python assets/generate_demo_bike.py
curl "http://localhost:3000/safety?file=assets/demo_bike.mp4"
```

See the notebook `python/notebooks/demo_spatial_safety.ipynb` for a demo calling the API.

## Sprint Cadence
| Sprint | Duration | Focus | Deliverables | Fidelity & Support |
|--------|----------|-------|--------------|--------------------|
| Sprint 0 | Week 0 | Set up dev kits, define stories & storyboards | Persona & journey maps; hardware rig | Low-mid fidelity; requires 1 designer |
| Sprint 1 | Weeks 1–2 | Build Mood-Mirror & Safety Bubble prototypes | Functional PoC videos; user testing reports | Mid-fidelity; occasional ML engineer for tuning |
| Sprint 2 | Weeks 3–4 | Build Palm-Prompter & SmartThings Assist | Integrated demos; developer handoff docs | Mid-high fidelity; integrator to link with SmartThings |
