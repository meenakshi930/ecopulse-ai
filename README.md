# 🌱 EcoPulse — AI Bio-Blitz

EcoPulse is an AI-powered biodiversity exploration application that encourages people to step outdoors, discover living organisms, and learn about the biodiversity around them.

Instead of using AI only to keep users on a screen, EcoPulse uses AI to encourage real-world exploration.

## 🌿 The Idea

The core idea is simple:

> **Use AI as a reason to go outside, not as a reason to stay on the screen.**

EcoPulse generates outdoor biodiversity missions based on the user's environment, difficulty, and preferred biodiversity type.

The user then goes outside, finds something interesting, takes a photo, and uploads it to the application.

The vision AI analyzes the image and provides a possible identification. EcoPulse then uses the iNaturalist API to retrieve additional biodiversity and taxonomic information.

Users can complete missions and earn BioPoints as they explore.

---

## ✨ Features

- 🤖 AI-generated biodiversity missions
- 🌳 Environment-based missions
- 🎯 Difficulty-based missions
- 🌸 Biodiversity-type selection
- 📸 Discovery image upload
- 🔎 AI-based organism identification
- 📊 AI confidence level
- 🌿 iNaturalist biodiversity information
- 🎯 Mission completion tracking
- 🌱 BioPoints
- 📈 Exploration progress
- 🛡️ Fallback handling for AI/API failures

---

## 🔄 How EcoPulse Works

```text
User selects preferences
        ↓
AI generates 5 missions
        ↓
User goes outside
        ↓
User discovers an organism
        ↓
User takes a photo
        ↓
Vision AI analyzes the image
        ↓
Possible organism identification
        ↓
iNaturalist lookup
        ↓
Scientific & biodiversity information
        ↓
User completes a mission
        ↓
+10 BioPoints
