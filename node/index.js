const express = require('express');
const path = require('path');
const { spawn } = require('child_process');

const app = express();
const PORT = process.env.PORT || 3000;
const PYTHON_SERVICE_URL = process.env.PYTHON_SERVICE_URL || 'http://localhost:5000';

app.get('/', (req, res) => {
  res.json({ status: 'AI Pin API ready' });
});

app.get('/mood', async (req, res) => {
  const file = req.query.file;
  if (!file || /[^\w.-]/.test(file)) {
    return res.status(400).json({ error: 'Missing or invalid file parameter' });
  }

  const audioPath = path.join(__dirname, '..', file);

  try {
    const url = new URL('/mood', PYTHON_SERVICE_URL);
    url.searchParams.set('file', audioPath);
    const response = await fetch(url);
    const text = await response.text();

    if (!response.ok) {
      console.error('Python service error:', response.status, text);
      return res
        .status(response.status)
        .json({ error: 'Python service error', details: text });
    }

    let data;
    try {
      data = JSON.parse(text);
    } catch (parseErr) {
      console.error('Invalid JSON from Python service:', text);
      return res.status(500).json({ error: 'Invalid response from Python service' });
    }

    res.json(data);
  } catch (err) {
    console.error('Failed to call Python service:', err);
    res
      .status(500)
      .json({ error: 'Python service request failed', details: err.message });
  }
});

app.get('/safety', (req, res) => {
  const file = req.query.file;
  if (!file || /[^\w./-]/.test(file)) {
    return res.status(400).json({ error: 'Missing or invalid file parameter' });
  }

  const clipPath = path.join(__dirname, '..', file);
  const scriptPath = path.join(__dirname, '..', 'python', 'safety_analysis.py');

  const py = spawn('python', [scriptPath, clipPath]);
  let stdout = '';
  let stderr = '';

  py.stdout.on('data', (data) => {
    stdout += data.toString();
  });

  py.stderr.on('data', (data) => {
    stderr += data.toString();
  });

  py.on('close', (code) => {
    if (code !== 0) {
      console.error('Python script error:', code, stderr);
      return res.status(500).json({ error: 'Python script failed', details: stderr });
    }

    try {
      const data = JSON.parse(stdout || '{}');
      res.json(data);
    } catch (err) {
      console.error('Invalid JSON from safety script:', stdout);
      res.status(500).json({ error: 'Invalid response from Python script' });
    }
  });
});

app.use((req, res) => {
  res.status(404).json({ error: 'Not Found' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
