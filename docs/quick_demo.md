# Quick Demo

1. **Install requirements**

   ```bash
   pip install -r python/requirements.txt
   npm install --prefix node
   ```

2. **Start the Node server**

   ```bash
   node node/index.js
   ```

3. **Call the mood endpoint**

   ```bash
   curl "http://localhost:3000/mood?file=sample.wav"
   # {"stress_level":"low","suggestion":"You're sounding relaxed. Keep it up!"}
   ```

4. **Call the safety endpoint**

   ```bash
   curl "http://localhost:3000/safety?file=assets/demo_bike.mp4"
   # {"danger":true,"direction":"left","eta":3}
   ```

5. **Stop the server** with `Ctrl+C`.

