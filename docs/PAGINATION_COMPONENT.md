# Pagination Component Documentation

## Overview
The pagination component provides a user-friendly way to navigate through large datasets in table views across the YatriSetu admin panel.

## Features

### 1. Pagination Info
Displays current viewing range:
```
Showing 1-10 of 50 bookings
```

### 2. Smart Page Numbers
- Shows up to 5 page numbers at a time
- Uses ellipsis (...) for large page ranges
- Always shows first and last page
- Centers current page when possible

### 3. Navigation Controls
- Previous button (◀)
- Next button (▶)
- Direct page number links
- Disabled state for first/last pages

## Visual Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Showing 11-20 of 50 bookings    [◀] [1] ... [3] [4] [5] ... [10] [▶]  │
└─────────────────────────────────────────────────────────────┘
```

## Usage

### HTML Structure
```html
<div class="pagination-modern" id="pagination"></div>
```

### JavaScript Implementation
```javascript
function updatePagination(totalItems) {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const pagination = document.getElementById('pagination');
    
    // Calculate display range
    const startItem = (currentPage - 1) * itemsPerPage + 1;
    const endItem = Math.min(currentPage * itemsPerPage, totalItems);
    
    // Generate HTML with info and controls
    let paginationHTML = `
        <div class="pagination-info">
            Showing ${startItem}-${endItem} of ${totalItems} items
        </div>
        <ul class="pagination">
            <!-- Previous button -->
            <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="changePage(${currentPage - 1})">
                    <i class="fas fa-chevron-left"></i>
                </a>
            </li>
            
            <!-- Page numbers -->
            <!-- ... -->
            
            <!-- Next button -->
            <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="changePage(${currentPage + 1})">
                    <i class="fas fa-chevron-right"></i>
                </a>
            </li>
        </ul>
    `;
    
    pagination.innerHTML = paginationHTML;
}
```

## CSS Classes

### Container
- `.pagination-modern` - Main container with flexbox layout

### Info Text
- `.pagination-info` - Displays "Showing X-Y of Z items"

### Pagination List
- `.pagination` - Unordered list container
- `.page-item` - List item for each control
- `.page-link` - Clickable link/button

### States
- `.page-item.active` - Current page (highlighted)
- `.page-item.disabled` - Disabled controls (grayed out)

## Styling

### Colors
- Default: Light gray background (#f9fafb)
- Hover: Slightly darker with border highlight
- Active: Primary accent color (blue)
- Disabled: Muted with reduced opacity

### Dimensions
- Button size: 36px × 36px
- Border radius: 8px
- Gap between buttons: 6px

### Transitions
- All state changes: 0.2s ease
- Hover effect: Slight upward movement (-1px)

## Examples

### Example 1: Few Pages (≤5)
```
Showing 1-10 of 30 items    [◀] [1] [2] [3] [▶]
```

### Example 2: Many Pages with Ellipsis
```
Showing 21-30 of 100 items    [◀] [1] ... [3] [4] [5] ... [10] [▶]
```

### Example 3: First Page
```
Showing 1-10 of 50 items    [◀] [1] [2] [3] [4] [5] [▶]
                            (disabled)
```

### Example 4: Last Page
```
Showing 41-50 of 50 items    [◀] [1] ... [3] [4] [5] [▶]
                                                    (disabled)
```

## Configuration

### Items Per Page
```javascript
const itemsPerPage = 10; // Adjust as needed
```

### Max Visible Pages
```javascript
const maxVisiblePages = 5; // Number of page buttons to show
```

## Accessibility

- Uses semantic HTML (`<nav>`, `<ul>`, `<li>`)
- Includes `aria-label` attributes
- Keyboard navigable
- Clear visual feedback for all states

## Browser Support

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Responsive

## Pages Using Pagination

1. **Bookings** (`/admin/bookings`) - ✅ Fixed
2. **Users** (`/admin/users`) - ✅ Working
3. **Routes** (`/admin/routes`) - May need update
4. **Payments** (`/admin/payments`) - May need update
5. **Buses** (`/admin/buses`) - May need update

## Troubleshooting

### Pagination Not Showing
- Check if `totalItems > itemsPerPage`
- Verify element ID matches: `id="pagination"`
- Check browser console for errors

### Incorrect Page Count
- Verify `itemsPerPage` constant
- Check `totalItems` calculation
- Ensure `Math.ceil()` is used for total pages

### Styling Issues
- Verify base.html includes pagination CSS
- Check for CSS conflicts
- Inspect element in browser DevTools

## Future Enhancements

- [ ] Add "Go to page" input field
- [ ] Add items per page selector (10, 25, 50, 100)
- [ ] Add keyboard shortcuts (←/→ for prev/next)
- [ ] Add URL parameter support for deep linking
- [ ] Add animation for page transitions
