#!/bin/sh
if [ ! -f .writing-voice ]; then
  exit 0
fi
printf '%s\n' "Write in this project's voice. Open with the goal, then the how. Follow any abstract claim with a concrete example. Prefer numbers to adjectives. Do not use corporate filler or stock assistant phrasing. Load the writing-voice skill for registers and the avoid list. Use a spaced en dash, not an em dash."
