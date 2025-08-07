const express = require('express');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({ status: 'AI Pin API ready' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
