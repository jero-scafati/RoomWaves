# 🎨 CSS Organization Guide - RoomWaves

This guide explains the CSS architecture and best practices for the RoomWaves project.

## 📁 File Structure

```
frontend/src/assets/
├── main.css           # Global styles & imports
├── design-tokens.css  # Design system tokens (colors, spacing, typography)
└── utilities.css      # Utility classes for common patterns
```

## 🎯 Architecture Overview

### 1. **Design Tokens** (`design-tokens.css`)
Centralized design system with CSS variables for:
- **Colors**: Primary, success, error, neutrals
- **Spacing**: Consistent 8px-based scale
- **Typography**: Font sizes, weights, line heights
- **Border Radius**: Standardized corner radii
- **Shadows**: Shadow scale for elevation
- **Transitions**: Consistent animation durations

### 2. **Utility Classes** (`utilities.css`)
Common patterns for rapid development:
- Layout utilities (flex, grid)
- Spacing utilities (padding, margin, gap)
- Text utilities (alignment, size, weight)
- Animation utilities
- Card/surface components

### 3. **Component Styles** (Scoped in `.vue` files)
Component-specific styles using `<style scoped>`.

---

## 🚀 Usage Guidelines

### ✅ DO: Use Design Tokens

```css
/* ✅ GOOD - Use design tokens */
.my-component {
  background-color: var(--color-surface);
  padding: var(--space-lg);
  border-radius: var(--radius-lg);
  color: var(--color-text-primary);
}

/* ❌ BAD - Hardcoded values */
.my-component {
  background-color: #1a1a1a;
  padding: 24px;
  border-radius: 8px;
  color: #e0e0e0;
}
```

### ✅ DO: Organize CSS with Comments

```css
<style scoped>
/* ============================================================================
   LAYOUT
   ============================================================================ */
.container {
  /* styles */
}

/* ============================================================================
   TYPOGRAPHY
   ============================================================================ */
.title {
  /* styles */
}

/* ============================================================================
   INTERACTIVE ELEMENTS
   ============================================================================ */
.button {
  /* styles */
}

/* ============================================================================
   RESPONSIVE DESIGN
   ============================================================================ */
@media (max-width: 768px) {
  /* mobile styles */
}
</style>
```

### ✅ DO: Use Utility Classes for Common Patterns

```vue
<template>
  <!-- ✅ Use utilities for simple layouts -->
  <div class="flex flex-between gap-md">
    <span>Label</span>
    <button>Action</button>
  </div>
</template>
```

### ❌ DON'T: Duplicate Common Styles

```css
/* ❌ BAD - Duplicated across components */
@keyframes fadeIn { /* ... */ }

/* ✅ GOOD - Already in design-tokens.css */
.my-component {
  animation: fadeIn var(--transition-slow);
}
```

---

## 📊 Design Token Reference

### Colors

#### Primary Colors
- `--color-primary` (#3b82f6) - Main brand color
- `--color-primary-hover` (#2563eb) - Hover state
- `--color-primary-light` (#60a5fa) - Light variant

#### Semantic Colors
- `--color-success` (#10b981) - Success states
- `--color-error` (#ef4444) - Error states
- `--color-warning` (#f59e0b) - Warning states

#### Neutral Colors
- `--color-background` (#0f0f0f) - Page background
- `--color-surface` (#1a1a1a) - Cards, containers
- `--color-surface-elevated` (#242424) - Elevated surfaces
- `--color-text-primary` (#e0e0e0) - Primary text
- `--color-text-secondary` (#b0b0b0) - Secondary text

### Spacing Scale (8px base)

```css
--space-xs: 0.25rem;  /* 4px */
--space-sm: 0.5rem;   /* 8px */
--space-md: 1rem;     /* 16px */
--space-lg: 1.5rem;   /* 24px */
--space-xl: 2rem;     /* 32px */
--space-2xl: 3rem;    /* 48px */
--space-3xl: 4rem;    /* 64px */
```

**Usage:**
```css
padding: var(--space-md);        /* 16px all sides */
gap: var(--space-lg);            /* 24px gap */
margin-bottom: var(--space-xl);  /* 32px bottom margin */
```

### Typography

#### Font Sizes
```css
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */
--font-size-lg: 1.125rem;   /* 18px */
--font-size-xl: 1.25rem;    /* 20px */
--font-size-2xl: 1.5rem;    /* 24px */
--font-size-3xl: 2rem;      /* 32px */
--font-size-4xl: 2.5rem;    /* 40px */
```

#### Font Weights
```css
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

---

## 🎭 Common Patterns

### Cards/Containers

```css
/* Basic card */
.card {
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
}

/* Elevated card */
.card-elevated {
  background-color: var(--color-surface-elevated);
  box-shadow: var(--shadow-md);
}
```

### Buttons

```css
/* Primary button */
.btn-primary {
  background-color: var(--color-primary);
  color: white;
  padding: var(--space-sm) var(--space-lg);
  border-radius: var(--radius-md);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-base);
}

.btn-primary:hover {
  background-color: var(--color-primary-hover);
  transform: translateY(-2px);
}
```

### Form Elements

```css
select,
input {
  background-color: var(--color-surface-elevated);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  padding: var(--space-sm) var(--space-md);
  transition: border-color var(--transition-base);
}

select:focus,
input:focus {
  outline: none;
  border-color: var(--color-primary);
}
```

---

## 📱 Responsive Design

### Breakpoint Guidelines

```css
/* Mobile-first approach */

/* Base styles (mobile) */
.element {
  font-size: var(--font-size-sm);
  padding: var(--space-sm);
}

/* Tablet and up (768px+) */
@media (min-width: 768px) {
  .element {
    font-size: var(--font-size-base);
    padding: var(--space-md);
  }
}

/* Desktop and up (1024px+) */
@media (min-width: 1024px) {
  .element {
    font-size: var(--font-size-lg);
    padding: var(--space-lg);
  }
}
```

### Standard Breakpoints
- **Mobile**: < 480px
- **Tablet**: 480px - 767px
- **Desktop**: 768px - 1023px
- **Large Desktop**: 1024px+

---

## 🔄 Migration Strategy

### Gradually Replace Hardcoded Values

**Before:**
```css
.button {
  background-color: #3b82f6;
  padding: 10px 24px;
  border-radius: 8px;
  color: #e0e0e0;
}
```

**After:**
```css
.button {
  background-color: var(--color-primary);
  padding: var(--space-sm) var(--space-lg);
  border-radius: var(--radius-lg);
  color: var(--color-text-primary);
}
```

---

## 🛠️ Component Style Template

Use this template for new components:

```vue
<template>
  <div class="my-component">
    <!-- template -->
  </div>
</template>

<style scoped>
/* ============================================================================
   LAYOUT
   ============================================================================ */


/* ============================================================================
   TYPOGRAPHY
   ============================================================================ */


/* ============================================================================
   INTERACTIVE ELEMENTS
   ============================================================================ */


/* ============================================================================
   STATES
   ============================================================================ */


/* ============================================================================
   RESPONSIVE DESIGN
   ============================================================================ */
@media (max-width: 768px) {
  
}
</style>
```

---

## 🎓 Best Practices Summary

1. **Always use design tokens** instead of hardcoded values
2. **Organize CSS** with clear section comments
3. **Use utility classes** for simple, common patterns
4. **Follow the spacing scale** (no arbitrary values)
5. **Use consistent transitions** from design tokens
6. **Write mobile-first** responsive styles
7. **Keep animations** centralized in design-tokens.css
8. **Document** complex CSS with comments

---

## 🔍 Troubleshooting

### Colors look different after migration
Make sure you're using the correct token name. Check `design-tokens.css` for the full color palette.

### Styles not applying
1. Check if the token exists in `design-tokens.css`
2. Make sure `main.css` is imported in `main.js`
3. Verify the CSS variable syntax: `var(--token-name)`

### Need a new design token?
Add it to `design-tokens.css` following the existing naming convention.

---

## 📚 Additional Resources

- [MDN: CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [CSS Architecture Best Practices](https://www.sitepoint.com/bem-smacss-advice-from-developers/)
- [Vue.js Style Guide](https://vuejs.org/style-guide/)
