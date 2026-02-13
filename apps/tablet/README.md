# Tablet App (Expo)

React Native (Expo + TypeScript) tablet client for the restaurant menu.

## Prerequisites

- Node.js 18+
- Android Studio + Android emulator
- Backend API running at `http://localhost:8000`

## Install

```bash
cd apps/tablet
npm install
```

## Run on Android emulator

```bash
cd apps/tablet
npx expo start
```

Then press `a` in the Expo terminal to open on Android emulator.

## Backend URL configuration

The app uses `src/config/api.ts`:

- Android emulator default: `http://10.0.2.2:8000`
- Physical device: replace with your machine LAN IP (for example `http://192.168.1.20:8000`)

Make sure backend and device/emulator can reach each other on the same network.
