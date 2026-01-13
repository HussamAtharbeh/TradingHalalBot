# Halal Trading Academy (TradeQuest)

## Overview
A gamified educational platform for Sharia-compliant trading featuring market simulators, expert trainers, trading challenges, and a premium store. The platform uses a dark crypto/gaming aesthetic inspired by Binance with gold (#f0b90b) accents.

## Project Architecture

### Frontend (React + TypeScript + Vite)
- **App.tsx**: Main application with routing between views, onboarding flow, and game screens
- **Components**:
  - `Header.tsx`: Navigation with tabs and user balance pill
  - `Onboarding.tsx`: Multi-step introduction flow
  - `Home.tsx`: Dashboard with progress, ads banner, and games lobby
  - `StockList.tsx`: Halal stocks with expandable compliance info
  - `Academy.tsx`: Trainer profiles with booking modals
  - `GamesLobby.tsx`: Game cards for simulators and challenges
  - `Store.tsx`: Coin packs and VIP subscriptions
  - `Profile.tsx`: User stats and achievements
  - `TradingSimulator.tsx`: Real-time price simulation game
  - `ScenarioChallenge.tsx`: Quiz-style trading challenges
  - `ToastNotification.tsx`: Toast feedback system

### Backend (Express + TypeScript)
- **server/routes.ts**: RESTful API endpoints with Zod validation
- **server/storage.ts**: In-memory storage for MVP (data resets on restart)

### Shared Types (shared/schema.ts)
- UserProfile, HalalStock, Trainer, GameItem, CoinPack, VipSubscription, TradingScenario
- All models have Zod schemas for validation

## Key Features
- **Onboarding**: 4-step introduction to platform features
- **Stock List**: 28 Jordanian halal stocks with compliance details (debt ratio, interest income, activity)
  - Categories: Banking, Insurance, Utilities, Mining, Education, Telecom, Transport, Real Estate, Industrial, Healthcare, Food, Energy
  - All stocks connected to the Trading Simulator
- **Trading Simulator**: Live price simulation with buy/sell positions and P&L tracking
- **Trading Challenges**: Quiz-style scenarios that teach market analysis
- **Shedda Card Game**: Jawaker-style card battle game teaching trading concepts step-by-step
  - 22 trading cards across 5 tiers (all unlocked from start)
  - Educational lobby with 5-step learning guide
- **Academy**: 3 expert trainers with booking and WhatsApp integration
- **Store**: Coin packs and VIP memberships
- **Profile**: Level progression, XP system, achievements

## Design System
- **Theme**: Dark-first with gold (#f0b90b) as primary accent
- **Font**: Inter (system fallback)
- **Border Radius**: Extreme rounding (2xl, 3xl)
- **Effects**: Glassmorphism, gold glow on VIP elements
- See `design_guidelines.md` for complete styling rules

## API Endpoints
- `GET /api/user/:id` - Get user profile
- `PATCH /api/user/:id` - Update user profile
- `POST /api/user/:id/balance` - Update balance
- `POST /api/user/:id/xp` - Add XP
- `GET /api/stocks` - List halal stocks
- `GET /api/trainers` - List trainers
- `GET /api/games` - List games
- `GET /api/store/coins` - List coin packs
- `GET /api/store/vip` - List VIP subscriptions
- `GET /api/scenarios` - List trading scenarios

## Running the Project
```bash
npm run dev
```
Server runs on port 5000 (Express + Vite).

## Data Persistence
MVP uses in-memory storage. Data resets on server restart. For production, connect to PostgreSQL using the existing Drizzle ORM setup.

## Recent Changes
- January 2026: Initial MVP with complete gamified trading education platform
- Implemented all core features: trading simulator, challenges, stocks, trainers, store
- Dark gaming theme with gold accents following design_guidelines.md
- Updated stock list to 28 Jordanian halal stocks (Jordan Islamic Bank, Safwa Islamic Bank, Arab Potash, etc.)
- All stocks now connected to Trading Simulator with Lucide icons instead of emojis
- Enhanced Shedda game with step-by-step learning guide and all 22 cards unlocked
