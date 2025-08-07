#!/usr/bin/env bash
node node/index.js &
PID=$!
until curl -s -f -o /dev/null "http://localhost:3000/health"; do sleep 0.5; done
curl -s "http://localhost:3000/mood?file=sample.wav"
curl -s "http://localhost:3000/safety?file=assets/demo_bike.mp4"
kill $PID

