# Google Sheets Template Structure

This document shows the exact structure your Google Sheets should have for the website content manager.

## 📋 Overview

Your Google Sheet should have **7 tabs** (sheets):
1. General
2. Hero
3. About
4. CoreValues
5. Services
6. ServiceDetails
7. Contact

Each tab will be published as a separate CSV URL.

---

## 📄 Tab 1: General

**Tab name:** `General`

This tab contains basic site information.

### Structure:

| field | value |
|-------|-------|
| company_name | TRI STAR |
| company_name_color | #D81400 |
| company_name_size | 2.25rem |
| company_name_style | normal |
| company_name_font | Arial |
| nav_home | Home |
| nav_about | About |
| nav_services | Services |
| nav_contact | Contact |
| nav_color | #D1D5DB |
| nav_size | 1rem |
| nav_font | Arial |
| site_title | TriStar - Your Website |
| logo_url | https://drive.google.com/uc?export=view&id=YOUR_FILE_ID |
| footer_text | © 2025 TriStar. All rights reserved. |

### Instructions:
1. Column A header: `field`
2. Column B header: `value`
3. Add rows for each field
4. For logo_url, use Google Drive image URL (see image instructions below)

---

## 🎯 Tab 2: Hero

**Tab name:** `Hero`

This tab contains the hero/landing section content.

### Structure:

| field | value |
|-------|-------|
| title | Welcome to TriStar |
| subtitle | Building foundations for success through expert geotechnical solutions |
| button_text | Learn More |

### Instructions:
1. Column A header: `field`
2. Column B header: `value`
3. Three rows for title, subtitle, and button text

---

## 📖 Tab 3: About

**Tab name:** `About`

This tab contains the About Us section.

### Structure:

| field | value |
|-------|-------|
| title | About Us |
| paragraph1 | Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. |
| paragraph2 | Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. |
| stat1_number | 100+ |
| stat1_label | Projects |
| stat2_number | 50+ |
| stat2_label | Clients |
| stat3_number | 5+ |
| stat3_label | Years |

### Instructions:
1. Column A header: `field`
2. Column B header: `value`
3. You can add more paragraphs (paragraph3, paragraph4, etc.)
4. You can add more stats (stat4_number, stat4_label, etc.)

---

## 💎 Tab 4: CoreValues

**Tab name:** `CoreValues`

This tab contains your company's core values.

### Structure:

| icon | title | description | color |
|------|-------|-------------|-------|
| 🎯 | Excellence | We strive for excellence in everything we do, delivering quality that exceeds expectations. | #10B981 |
| 🤝 | Integrity | We operate with honesty and transparency, building trust with every interaction. | #6366F1 |
| 💡 | Innovation | We embrace creativity and forward-thinking solutions to solve complex challenges. | #F59E0B |

### Instructions:
1. Column A: `icon` (emoji - use Windows key + . or Cmd + Ctrl + Space on Mac)
2. Column B: `title`
3. Column C: `description`
4. Column D: `color` (hex color code, e.g. `#3B82F6`)

### To add more values:
Just add more rows! The website will automatically display all values.

---

## 🛠️ Tab 5: Services

**Tab name:** `Services`

This tab contains the services overview cards.

### Structure:

| name | link_id | color | description |
|------|---------|-------|-------------|
| Geotechnical Drilling | geotechnical-drilling | #3B82F6 | Expert drilling services for site investigation and subsurface exploration. |
| Geotechnical Testing | geotechnical-testing | #A855F7 | Comprehensive laboratory and field testing of soil and rock samples. |
| Construction Material Testing | construction-material-testing | #F97316 | Quality assurance testing for concrete, asphalt, and other construction materials. |

### Instructions:
1. Column A: `name` (Service display name)
2. Column B: `link_id` (URL-friendly ID, lowercase, use hyphens)
3. Column C: `gradient` (Color gradient)
4. Column D: `description` (Short description shown on the service card — optional)

### To add more services:
Just add more rows! The website will automatically create new service cards.

⚠️ **Important:** The `link_id` must match the `service_id` in the ServiceDetails tab!

---

## 📝 Tab 6: ServiceDetails

**Tab name:** `ServiceDetails`

This tab contains detailed service pages.

### Structure:

| service_id | content | bg_image | image_position |
|------------|---------|----------|----------------|
| geotechnical-drilling | (markdown content — see below) | https://drive.google.com/uc?export=view&id=YOUR_FILE_ID | right |

### Instructions:
1. `service_id` - Must match the `link_id` from Services tab
2. `content` - Free-form markdown text (use Alt+Enter for new lines in the cell). Use `#` or `##` at the top for the section title.
4. `bg_image` - Google Drive image URL for background
5. `image_position` - Either `left` or `right` (which side the image appears)

### Writing content with Markdown:

Use **Alt+Enter** (Windows) or **Ctrl+Enter** (Mac) to add new lines inside a Google Sheets cell.

```
## Key Services Include

Our drilling services cover a wide range of project types.

- Standard Penetration Testing (SPT)
- Cone Penetration Testing (CPT)
- Soil and rock core sampling
    - Shallow cores
    - Deep rock coring
- Monitoring well installation

Our experienced team ensures accurate data collection on every project.
```

**Supported syntax:**
- `## Heading` — section heading
- `### Sub-heading` — smaller heading
- `- item` — bullet point
- `    - item` — nested bullet (4 spaces indent)
- `**bold**` — bold text
- `*italic*` — italic text
- Blank line — paragraph break

### To add more services:
Add a new row with a new `service_id`. Make sure to also add it to the Services tab!

---

## 📧 Tab 7: Contact

**Tab name:** `Contact`

This tab contains contact form labels and placeholders.

### Structure:

| field | value |
|-------|-------|
| title | Get In Touch |
| name_label | Name |
| name_placeholder | Your name |
| email_label | Email |
| email_placeholder | your@email.com |
| message_label | Message |
| message_placeholder | Your message |
| button_text | Send Message |

### Instructions:
1. Column A header: `field`
2. Column B header: `value`
3. Customize labels and placeholders as needed

---

## 🖼️ How to Use Google Drive Images

### Step 1: Upload Image to Google Drive
1. Go to Google Drive
2. Upload your image file

### Step 2: Share the Image
1. Right-click the image → "Share"
2. Click "Change to anyone with the link"
3. Make sure it's set to "Viewer"
4. Click "Copy link"

### Step 3: Convert the Link
You'll get a link like:
```
https://drive.google.com/file/d/1AbCdEfGhIjKlMnOpQrStUvWxYz123456/view?usp=sharing
```

**Extract the FILE_ID** (the long string between `/d/` and `/view`):
```
1AbCdEfGhIjKlMnOpQrStUvWxYz123456
```

**Convert to direct image URL:**
```
https://drive.google.com/uc?export=view&id=1AbCdEfGhIjKlMnOpQrStUvWxYz123456
```

### Option: Use a Formula (Advanced)
You can add a helper column with this formula to auto-convert:

In column C (assuming Google Drive link is in B2):
```
=IF(B2="","","https://drive.google.com/uc?export=view&id=" & REGEXEXTRACT(B2,"[-\w]{25,}"))
```

Then copy the result from column C to use in your sheet!

---

## 🎨 Gradient Color Reference

Here are some pre-tested gradient combinations you can use:

| Gradient Class | Colors | Use For |
|----------------|--------|---------|
| `from-blue-500 to-cyan-500` | Blue to Cyan | Technology, Trust |
| `from-purple-500 to-pink-500` | Purple to Pink | Creativity, Innovation |
| `from-orange-500 to-red-500` | Orange to Red | Energy, Action |
| `from-emerald-500 to-teal-500` | Green to Teal | Growth, Success |
| `from-indigo-500 to-blue-500` | Indigo to Blue | Professional, Calm |
| `from-amber-500 to-yellow-500` | Amber to Yellow | Optimism, Clarity |
| `from-rose-500 to-pink-500` | Rose to Pink | Warmth, Care |
| `from-cyan-500 to-blue-500` | Cyan to Blue | Fresh, Modern |

---

## ✅ Checklist: Setting Up Your Google Sheet

- [ ] Create a new Google Sheet
- [ ] Create 7 tabs with exact names: General, Hero, About, CoreValues, Services, ServiceDetails, Contact
- [ ] Add column headers as specified for each tab
- [ ] Fill in your content
- [ ] Upload images to Google Drive and get shareable links
- [ ] Convert Google Drive links to direct URLs
- [ ] Test that all links work (paste in browser)
- [ ] Share the sheet with your team members (give them edit access)
- [ ] Publish each tab as CSV (see main README for instructions)

---

## 💡 Tips

1. **Keep backups**: Google Sheets has version history (File → Version history)
2. **Test changes**: You can manually run the GitHub Action to test
3. **Images**: Use high-quality images (at least 1920x1080 for backgrounds)
4. **Text length**: Keep titles concise, descriptions can be longer
5. **Special characters**: Avoid using `|` character except in key_services field
6. **Emojis**: You can use emojis in any text field! 🎉

---

## ❓ Need Help?

If something isn't working:
1. Check that column headers match exactly (case-sensitive)
2. Make sure there are no empty rows between data
3. Verify Google Drive images are shared publicly
4. Check the GitHub Action logs for error messages
