const express = require('express');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({ status: 'AI Pin API ready' });
});

app.get('/mood', (req, res) => {
  const file = req.query.file;
  if (!file || /[^\w.-]/.test(file)) {
    return res.status(400).json({ error: 'Missing or invalid file parameter' });
  }

  const scriptPath = path.join(__dirname, '..', 'python', 'mood_analysis.py');
  const py = spawn('python3', [scriptPath, file]);

  let stdout = '';
  let stderr = '';

  py.stdout.on('data', (data) => {
    stdout += data;
  });

  py.stderr.on('data', (data) => {
    stderr += data;
  });

  py.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: stderr.trim() || 'Python process failed' });
    }
    try {
      const result = JSON.parse(stdout);
      res.json(result);
    } catch (err) {
      res.status(500).json({ error: 'Invalid JSON from Python script' });
    }
  });
});

app.use((req, res) => {
  res.status(404).json({ error: 'Not Found' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
