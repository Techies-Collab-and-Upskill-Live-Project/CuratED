# CuratED Brand Colors Implementation

This document describes the brand color implementation for the CuratED educational platform.

## Brand Color Palette

The following colors define the visual identity of CuratED and should be used consistently across the application:

### Primary Colors
- **Main Color**: `#008073` (Teal) - Primary brand color for key UI elements
- **Sub Color**: `#FFB81E` (Orange/Yellow) - Secondary accent color for highlights and interactions

### Text Colors
- **Part Header**: `#B4931F` (Gold) - For section headers and important text elements
- **Part Text**: `#2D1500` (Dark Brown) - Main body text color
- **Header Text**: `#0F4C78` (Dark Blue) - Primary headers and titles
- **Grey Text**: `#8A8A8A` (Gray) - Secondary text, footnotes, and less important content

### Background Colors
- **Card Text Background**: `#FEF4EA` (Light Cream) - Background for cards and content areas
- **Card Text Color**: `#2D1500` (Dark Brown) - Text color for content on light backgrounds
- **White**: `#ffff` (Pure White) - Pure white backgrounds

### Special Colors
- **Event Card**: `rgba(255, 184, 30, 0.775)` - Semi-transparent orange for event cards and overlays
- **Part Head Text**: `#B4931F` (Gold) - Alternative to part header color
- **Placeholder Color**: `#B2B2B2` (Light Gray) - Input placeholders and disabled text

## Current Implementation

### Email Templates
The brand colors have been implemented in the following email templates:
- `templates/email/auth/verify_email.html` - Email verification template
- `templates/email/auth/password_reset.html` - Password reset template

### Key Changes Made:
1. **Background color**: Changed from `#F9E3DE` to `#FEF4EA` (light cream)
2. **Primary accent**: Changed from `#E2725B` to `#008073` (teal)
3. **Text color**: Changed from `#222` to `#2D1500` (dark brown)
4. **Header color**: Changed from old primary to `#0F4C78` (dark blue)
5. **Secondary text**: Changed from `#888` to `#8A8A8A` (updated gray)
6. **Highlight color**: Changed to `#B4931F` (gold)
7. **Button hover**: Changed from `#ff9900` to `#FFB81E` (brand orange)

### Color Constants
A color constants file has been created at `backend/brand_colors.py` containing:
- Individual color constants for each brand color
- A `BRAND_COLORS` dictionary for easy access to colors by context
- Documentation for each color's intended use

## Usage Guidelines

### For Developers
1. **Always use the brand colors** defined in `backend/brand_colors.py`
2. **Import colors** from the constants file rather than hardcoding hex values
3. **Maintain consistency** across all user-facing elements
4. **Test email templates** to ensure proper color rendering across email clients

### Color Context Mapping
- **Primary actions**: Use `#008073` (main color)
- **Secondary actions**: Use `#FFB81E` (sub color)
- **Text content**: Use `#2D1500` (part text color)
- **Headers**: Use `#0F4C78` (header text color)
- **Backgrounds**: Use `#FEF4EA` (card text background)
- **Accents**: Use `#B4931F` (part header color)

## Testing
The implementation has been tested to ensure:
- ✅ All old colors have been replaced
- ✅ New brand colors are properly applied
- ✅ Email templates render correctly
- ✅ Color consistency is maintained

Run the test script to verify the implementation:
```bash
python /tmp/test_brand_colors.py
```

## Future Considerations
- **Frontend Implementation**: When a frontend is added, ensure these same colors are used
- **CSS Variables**: Consider implementing CSS custom properties for browser-based interfaces
- **Accessibility**: Ensure color combinations meet WCAG accessibility guidelines
- **Dark Mode**: Consider defining a dark mode color palette based on these brand colors

## Migration Summary
This update replaced the previous orange/peach color scheme with the new teal/gold/cream brand palette while maintaining the same visual hierarchy and user experience.