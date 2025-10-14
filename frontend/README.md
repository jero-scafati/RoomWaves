# RoomWaves Frontend

Vue.js web interface for acoustic analysis.

## Setup

```bash
npm install
```

## Run

```bash
npm run dev
```

App available at `http://localhost:5173`

## Build

```bash
npm run build
```

## Docker

```bash
docker build -t roomwaves-frontend .
docker run -p 80:80 roomwaves-frontend
```

## Tech Stack

- Vue 3
- ECharts (visualization)
- Vite (build tool)
