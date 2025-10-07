# Color System Guide - RoomWaves

## Overview

The RoomWaves application now uses a centralized color system based on CSS custom properties (variables). This ensures consistency across the entire application and makes it easy to maintain and update the design.

## Color Palette

All colors are defined in `/src/assets/design-tokens.css` and can be accessed using CSS variables.

### Background Colors

```css
--color-background: #050e14          /* Main background */
--color-background-secondary: #040b10 /* Footer and secondary sections */
--color-surface: #181A1B             /* Cards, dropdowns, selectors */
--color-surface-elevated: #1f2123    /* Elevated surfaces */
--color-surface-hover: #252729       /* Hover states */
```

### Text Colors

```css
--color-text-primary: #FFFFC2    /* Main text (cream/yellow) */
--color-text-secondary: #A5A5A6  /* Secondary text (gray) */
--color-text-tertiary: #808082   /* Tertiary text (darker gray) */
--color-text-disabled: #6a6a6a   /* Disabled text */
```

### Primary Colors

```css
--color-primary: #2F0988          /* Buttons, links, primary actions */
--color-primary-hover: #4510b8    /* Hover state */
--color-primary-light: #5a1de0    /* Light variant */
```

### Semantic Colors

```css
--color-success: #71d687
--color-error: #c05656
--color-warning: #ad720a
--color-info: #0f758f
```

## Using Colors in Components

### ✅ Correct Usage (Use CSS Variables)

```css
.my-component {
  background-color: var(--color-background);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.my-button {
  background-color: var(--color-primary);
  color: var(--color-text-primary);
}
```

### ❌ Incorrect Usage (Don't Hardcode Colors)

```css
/* DON'T DO THIS */
.my-component {
  background-color: #050e14;
  color: #FFFFC2;
}
```

## Glassmorphism Effect

The navbar uses a glassmorphism effect for a modern, transparent look. You can apply this effect using the predefined variables:

```css
.glass-element {
  background: var(--glass-background);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
}
```

Or use the utility class:

```html
<div class="glass">
  <!-- Content -->
</div>
```

## Typography

### Font Family

The application uses **Arvo** font (a bold serif font) as the primary typeface:

```css
font-family: var(--font-family-base);
```

### Font Weights

```css
--font-weight-normal: 400
--font-weight-medium: 500
--font-weight-semibold: 600
--font-weight-bold: 700
```

### Font Sizes

```css
--font-size-xs: 0.75rem    /* 12px */
--font-size-sm: 0.875rem   /* 14px */
--font-size-base: 1rem     /* 16px */
--font-size-lg: 1.125rem   /* 18px */
--font-size-xl: 1.25rem    /* 20px */
--font-size-2xl: 1.5rem    /* 24px */
--font-size-3xl: 2rem      /* 32px */
--font-size-4xl: 2.5rem    /* 40px */
```

## Utility Classes

The application provides utility classes in `/src/assets/utilities.css` for common patterns:

### Buttons

```html
<!-- Primary button -->
<button class="btn btn-primary">Submit</button>

<!-- Secondary button -->
<button class="btn btn-secondary">Cancel</button>
```

### Form Controls

```html
<!-- Input field -->
<input type="text" class="form-control" placeholder="Enter text">

<!-- Select dropdown -->
<select class="form-control">
  <option>Option 1</option>
</select>
```

### Cards

```html
<!-- Basic card -->
<div class="card">
  Content here
</div>

<!-- Elevated card -->
<div class="card-elevated">
  Content here
</div>
```

### Text Colors

```html
<p class="text-primary">Primary text</p>
<p class="text-secondary">Secondary text</p>
<p class="text-tertiary">Tertiary text</p>
<p class="text-success">Success message</p>
<p class="text-error">Error message</p>
```

### Badges

```html
<span class="badge badge-primary">New</span>
<span class="badge badge-success">Success</span>
<span class="badge badge-error">Error</span>
```

### Alerts

```html
<div class="alert alert-success">
  Operation completed successfully!
</div>

<div class="alert alert-error">
  An error occurred.
</div>
```

### Gradients

```html
<!-- Background gradient -->
<div class="gradient-primary">
  Content with gradient background
</div>

<!-- Text gradient -->
<h1 class="text-gradient-primary">
  Gradient text
</h1>
```

## Spacing System

The application uses an 8px-based spacing scale:

```css
--space-xs: 0.25rem   /* 4px */
--space-sm: 0.5rem    /* 8px */
--space-md: 1rem      /* 16px */
--space-lg: 1.5rem    /* 24px */
--space-xl: 2rem      /* 32px */
--space-2xl: 3rem     /* 48px */
--space-3xl: 4rem     /* 64px */
```

### Usage Example

```css
.my-component {
  padding: var(--space-md);
  margin-bottom: var(--space-lg);
  gap: var(--space-sm);
}
```

## Border Radius

```css
--radius-sm: 4px
--radius-md: 6px
--radius-lg: 8px
--radius-xl: 12px
--radius-full: 9999px
```

## Transitions

```css
--transition-fast: 150ms ease
--transition-base: 200ms ease
--transition-slow: 300ms ease
```

### Usage Example

```css
.my-button {
  transition: all var(--transition-base);
}
```

## Shadows

```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3)
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.3)
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.4)
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.4)
--shadow-glow: 0 0 20px rgba(47, 9, 136, 0.3)
```

## Migration Guide

When updating existing components to use the new color system:

1. **Replace hardcoded colors with CSS variables**
   ```css
   /* Before */
   color: #e0e0e0;
   
   /* After */
   color: var(--color-text-primary);
   ```

2. **Use utility classes where appropriate**
   ```html
   <!-- Before -->
   <p style="color: #b0b0b0; font-size: 14px;">Text</p>
   
   <!-- After -->
   <p class="text-secondary text-sm">Text</p>
   ```

3. **Replace hardcoded spacing with variables**
   ```css
   /* Before */
   padding: 16px;
   margin: 24px;
   
   /* After */
   padding: var(--space-md);
   margin: var(--space-lg);
   ```

4. **Use form-control class for inputs**
   ```html
   <!-- Before -->
   <input style="background: #2a2a2a; color: #e0e0e0; border: 1px solid #3a3a3a;">
   
   <!-- After -->
   <input class="form-control">
   ```

## Best Practices

1. **Always use CSS variables** - Never hardcode color values in your components
2. **Use utility classes** - For common patterns like buttons, forms, and text colors
3. **Maintain consistency** - Follow the established design tokens for spacing, sizing, and colors
4. **Test in dark mode** - All colors are optimized for dark backgrounds
5. **Use semantic colors** - Use success/error/warning colors for appropriate contexts

## Examples

### Creating a Custom Component

```vue
<template>
  <div class="custom-card">
    <h3 class="card-title">Title</h3>
    <p class="card-description">Description text</p>
    <button class="btn btn-primary">Action</button>
  </div>
</template>

<style scoped>
.custom-card {
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  transition: all var(--transition-base);
}

.custom-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-lg);
}

.card-title {
  color: var(--color-text-primary);
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--space-sm);
}

.card-description {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  margin-bottom: var(--space-md);
}
</style>
```

## Questions or Issues?

If you need additional colors or design tokens, add them to `/src/assets/design-tokens.css` and document them here.
