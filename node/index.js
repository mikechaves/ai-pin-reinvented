const express = require('express');
const path = require('path');

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
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    res.status(500).json({ error: 'Python service request failed' });
  }
});

app.use((req, res) => {
  res.status(404).json({ error: 'Not Found' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
