# YatriSetu Design System Reference

Quick reference guide for the YatriSetu design system.

---

## 🎨 Color Palette

### Background Colors
```css
--bg-primary: #0a0e27      /* Main background */
--bg-secondary: #141b2d    /* Sidebar, cards */
--bg-tertiary: #1f2937     /* Inputs, hover states */
--bg-card: #1a2332         /* Card backgrounds */
```

### Accent Colors
```css
--accent-primary: #6366f1   /* Indigo - Primary actions */
--accent-secondary: #8b5cf6 /* Purple - Secondary actions */
--accent-tertiary: #ec4899  /* Pink - Highlights */
```

### Text Colors
```css
--text-primary: #f8fafc     /* Headings, important text */
--text-secondary: #cbd5e1   /* Body text */
--text-muted: #94a3b8       /* Labels, captions */
--text-dim: #64748b         /* Placeholders, disabled */
```

### Status Colors
```css
--success-color: #10b981    /* Success states */
--success-light: #34d399    /* Success hover */
--danger-color: #ef4444     /* Error states */
--danger-light: #f87171     /* Error hover */
--warning-color: #f59e0b    /* Warning states */
--warning-light: #fbbf24    /* Warning hover */
--info-color: #06b6d4       /* Info states */
--info-light: #22d3ee       /* Info hover */
```

---

## 📝 Typography

### Font Families
```css
/* Headings */
font-family: 'Poppins', 'Inter', sans-serif;

/* Body Text */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Code/Data */
font-family: 'Courier New', monospace;
```

### Font Sizes
```css
h1 { font-size: 2.5rem; }    /* 40px */
h2 { font-size: 2rem; }      /* 32px */
h3 { font-size: 1.5rem; }    /* 24px */
h4 { font-size: 1.25rem; }   /* 20px */
h5 { font-size: 1.125rem; }  /* 18px */
h6 { font-size: 1rem; }      /* 16px */
body { font-size: 0.9375rem; } /* 15px */
small { font-size: 0.875rem; } /* 14px */
```

### Font Weights
```css
300 - Light
400 - Regular
500 - Medium
600 - Semibold
700 - Bold
800 - Extrabold
900 - Black
```

---

## 📏 Spacing

### Padding/Margin Scale
```css
4px   - xs
8px   - sm
12px  - md
16px  - lg
20px  - xl
24px  - 2xl
32px  - 3xl
40px  - 4xl
```

### Border Radius
```css
8px  - Small (badges, tags)
10px - Medium (buttons, inputs)
12px - Large (cards, panels)
14px - XL (metrics, insights)
16px - 2XL (major cards)
18px - 3XL (hero cards)
```

---

## 🎯 Components

### Buttons
```html
<!-- Primary Button -->
<button class="btn btn-primary">
    <i class="fas fa-icon"></i> Button Text
</button>

<!-- Secondary Button -->
<button class="btn btn-secondary">
    <i class="fas fa-icon"></i> Button Text
</button>

<!-- Small Button -->
<button class="btn btn-sm btn-primary">
    Small Button
</button>
```

### Stat Cards
```html
<div class="stat-card">
    <div class="stat-icon">
        <i class="fas fa-icon"></i>
    </div>
    <div class="stat-value">1,234</div>
    <div class="stat-label">Label Text</div>
    <div class="stat-change positive">
        <i class="fas fa-arrow-up"></i> +12.3%
    </div>
</div>
```

### Badges
```html
<span class="badge badge-success">Success</span>
<span class="badge badge-danger">Danger</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-info">Info</span>
```

### Table Card
```html
<div class="table-card">
    <div class="table-card-header">
        <h3>Table Title</h3>
        <button class="btn btn-secondary">Action</button>
    </div>
    <table class="table">
        <!-- Table content -->
    </table>
</div>
```

### Insight Metrics
```html
<div class="insight-metric">
    <div class="metric-icon" style="background: gradient;">
        <i class="fas fa-icon"></i>
    </div>
    <div class="metric-data">
        <div class="metric-value">1,234</div>
        <div class="metric-label">Metric Name</div>
    </div>
</div>
```

---

## 🎨 Gradients

### Primary Gradient
```css
background: linear-gradient(135deg, #6366f1, #8b5cf6);
```

### Success Gradient
```css
background: linear-gradient(135deg, #10b981, #34d399);
```

### Warning Gradient
```css
background: linear-gradient(135deg, #f59e0b, #fbbf24);
```

### Danger Gradient
```css
background: linear-gradient(135deg, #ef4444, #f87171);
```

### Info Gradient
```css
background: linear-gradient(135deg, #06b6d4, #22d3ee);
```

---

## 🌟 Shadows

```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

---

## 🎭 Animations

### Hover Effects
```css
/* Card Lift */
transform: translateY(-6px);
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

/* Button Lift */
transform: translateY(-2px);

/* Sidebar Item Slide */
transform: translateX(4px);
```

### Transitions
```css
/* Standard */
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

/* Fast */
transition: all 0.2s ease;

/* Slow */
transition: all 0.5s ease;
```

---

## 📱 Responsive Breakpoints

```css
/* Mobile */
@media (max-width: 768px) { }

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) { }

/* Desktop */
@media (min-width: 1025px) { }
```

---

## 🎯 Usage Examples

### Page Header
```html
<div class="page-header">
    <div>
        <h2>Page Title</h2>
        <p>Page description</p>
    </div>
    <div class="header-actions">
        <button class="btn btn-secondary">
            <i class="fas fa-sync-alt"></i> Refresh
        </button>
        <button class="btn btn-primary">
            <i class="fas fa-plus"></i> Add New
        </button>
    </div>
</div>
```

### Sidebar Navigation
```html
<nav>
    <div class="nav-section-title">Section Title</div>
    <a class="nav-link active" href="/page">
        <i class="fas fa-icon"></i>
        <span>Page Name</span>
    </a>
</nav>
```

### Form Input
```html
<div class="mb-3">
    <label class="form-label">Label</label>
    <input type="text" class="form-control" placeholder="Placeholder">
</div>
```

---

## 🎨 Icon Guidelines

### Icon Library
Font Awesome 6.4.0

### Icon Sizes
```css
Small: 14px
Medium: 16px
Large: 18px
XL: 20px
2XL: 24px
3XL: 32px
```

### Common Icons
```html
<i class="fas fa-home"></i>        <!-- Dashboard -->
<i class="fas fa-robot"></i>       <!-- Chatbot -->
<i class="fas fa-bus"></i>         <!-- Buses -->
<i class="fas fa-route"></i>       <!-- Routes -->
<i class="fas fa-users"></i>       <!-- Users -->
<i class="fas fa-ticket-alt"></i>  <!-- Bookings -->
<i class="fas fa-wallet"></i>      <!-- Payments -->
<i class="fas fa-chart-line"></i>  <!-- Analytics -->
```

---

## ✅ Best Practices

### Do's
✅ Use CSS variables for colors
✅ Use Poppins for headings
✅ Use Inter for body text
✅ Add hover states to interactive elements
✅ Use gradients for primary actions
✅ Maintain consistent spacing
✅ Use semantic HTML
✅ Add ARIA labels

### Don'ts
❌ Don't use inline styles
❌ Don't mix font families randomly
❌ Don't use too many colors
❌ Don't forget hover states
❌ Don't use low contrast text
❌ Don't skip responsive design
❌ Don't ignore accessibility

---

## 🚀 Quick Start

### 1. Include Base Template
```html
{% extends "base.html" %}
```

### 2. Add Page Title
```html
{% block title %}Page Title - YatriSetu{% endblock %}
```

### 3. Add Custom CSS (Optional)
```html
{% block extra_css %}
<style>
    /* Custom styles */
</style>
{% endblock %}
```

### 4. Add Content
```html
{% block content %}
<!-- Sidebar -->
<div class="sidebar">
    <!-- Navigation -->
</div>

<!-- Main Content -->
<div class="main-content">
    <!-- Page content -->
</div>
{% endblock %}
```

### 5. Add Custom JS (Optional)
```html
{% block extra_js %}
<script>
    // Custom JavaScript
</script>
{% endblock %}
```

---

## 📚 Resources

### Fonts
- [Google Fonts - Inter](https://fonts.google.com/specimen/Inter)
- [Google Fonts - Poppins](https://fonts.google.com/specimen/Poppins)

### Icons
- [Font Awesome](https://fontawesome.com/icons)

### Colors
- [Tailwind Colors](https://tailwindcss.com/docs/customizing-colors)

### Gradients
- [UI Gradients](https://uigradients.com/)

---

**Last Updated:** February 22, 2026
**Version:** 2.0
