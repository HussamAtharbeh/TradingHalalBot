# Halal Trading Academy - Design Guidelines

## Design Approach

**Reference-Based Hybrid**: Combine Binance's dark crypto trading aesthetic + gaming platform visual richness (Steam, Epic Games) + Linear's typography clarity. The platform balances serious financial education with gamification elements.

## Core Design Elements

### A. Typography

**Primary Font**: Inter (via Google Fonts)
- **Hero/Headings**: Black (900), 2xl-5xl, tight tracking (-0.02em)
- **Subheadings**: Bold (700), xl-2xl
- **Body**: Medium (500), sm-base
- **Labels/Meta**: Bold (700), xs-sm, uppercase, wide tracking (0.3em)
- **Numbers/Stats**: Mono variant, Black (900) for emphasis

### B. Layout System

**Spacing**: Tailwind units of 2, 4, 6, 8, 10, 12 for tight layouts; 16, 20, 24, 32 for generous sections
**Containers**: max-w-7xl centered with px-6 py-10
**Grid**: 3-column desktop (lg:grid-cols-3), 2-column tablet, single mobile
**Border Radius**: Extreme roundness - 2xl (1rem) for small elements, 3xl (1.5rem) for cards, full for pills

### C. Component Library

**Cards**: 
- Background: #161a1e or #1e2329
- Border: 1px solid white/5%
- Padding: p-12 (generous internal spacing)
- Shadow: shadow-2xl
- Hover: Subtle scale (1.02) or border color shifts

**Navigation Tabs**:
- Container: bg-white/5 with p-1.5, rounded-full
- Active: bg-game-gold (#f0b90b) with shadow-2xl
- Inactive: text-gray-400, hover to white

**Stat Pills/Badges**:
- Background: Dark container (#1e2329)
- Gold accent circles for icons/actions
- Two-line format: label (tiny, gray-500) + value (large, white, mono)

**Buttons**:
- Primary: bg-game-gold, text-black, font-black
- When on images: backdrop-blur-2xl bg-black/40 border-white/20
- States: hover:scale-105, no complex hover backgrounds

**Progress Bars**:
- Track: bg-black/40 with border-white/5
- Fill: Gradient from gold to yellow-600 with glow shadow
- Text overlay: Centered, tiny uppercase

**Headers**:
- Sticky with backdrop-blur-2xl
- Height: h-24
- Two-tier info display: brand + navigation + user stats

### D. Visual Treatments

**Glassmorphism**: bg-white/5 backdrop-blur-2xl for overlays and navigation
**Gradients**: Gold gradients (from-game-gold to-yellow-600) for emphasis elements
**Shadows**: Colored shadows (shadow-yellow-500/30) for gold elements, shadow-2xl for depth
**Borders**: Consistent white/5-10% opacity throughout
**Icons**: Emoji-based for playful personality (📈🎮💎👨‍🏫), 2xl-5xl sizing

### E. Imagery Strategy

**Hero Images**: No traditional hero section - gaming dashboard approach with immediate content
**Stock/Product Cards**: Use Unsplash for trainer photos, picsum.photos for placeholder game images
**Avatars**: UI-avatars API with dark backgrounds and gold text
**Decorative Elements**: Large emoji backgrounds at 50%+ opacity as section accents

**Image Placement**:
- Trainer cards: Medium rounded rectangles (400x400)
- Game lobby: Wide landscape cards (800x450)
- Profile avatars: Rounded-2xl with gold borders for VIP users
- No large hero image - content-first approach

### F. Animations

**Minimal & Purposeful**:
- fade-in (0.4s) for view transitions
- scale-in (0.3s) for modals/cards
- Hover scales: 1.05 for interactive elements
- Progress bar fills: 1000ms duration
- No decorative scroll animations

## Special Patterns

**VIP Differentiation**: Gold border-2 + shadow-yellow-500/40 on avatars and sections
**Stats Display**: Grid of dark cards with emoji icons, mono numbers, and tiny labels
**Toast Notifications**: Positioned top-right, color-coded (gold for money, green for success)
**Onboarding**: Full-screen overlay with step progression
**Game Entry**: Modal overlays that replace main content with close buttons

## Accessibility

- Consistent WCAG AA contrast (white on dark, gold on dark both pass)
- All interactive elements min 44px touch target
- Clear focus states with outline-game-gold
- Screen reader labels on icon-only buttons

## Key Constraints

- Never use pure white - always off-white (#f5f5f5) or white with opacity
- Maintain dark-first aesthetic - no light mode elements
- Keep gold as sole accent color - no secondary brand colors
- Borders always subtle (white/5-10%) except for VIP gold accents
- Text shadows forbidden - rely on backgrounds for legibility