#!/usr/bin/env bash
node node/index.js &
PID=$!
sleep 1
curl -s "http://localhost:3000/mood?file=sample.wav"
curl -s "http://localhost:3000/safety?file=assets/demo_bike.mp4"
kill $PID

