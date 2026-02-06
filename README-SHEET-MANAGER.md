# 📊 Website Content Manager - Google Sheets Edition

Welcome! This guide will help you manage your TriStar website content using Google Sheets - **no coding required!**

## 🎯 What This Does

- ✏️ **Edit website content** in a familiar Google Sheets interface
- 🖼️ **Manage images** using Google Drive links
- 🤖 **Automatic updates** - changes in the sheet automatically update the website
- 👥 **Team collaboration** - multiple people can edit the sheet
- 🔒 **Private editing** - only people with edit access can change content
- 🌐 **Public viewing** - content is public (but it's on your website anyway!)

## 📋 How It Works

```
1. Edit Google Sheet → 2. Click "Update Website" → 3. Website Updates! 🎉
         ↓                        ↓                         ↓
    (Your team)          (GitHub Action)            (Automatic deploy)
```

---

## 🚀 Initial Setup (One-Time)

### Step 1: Create Your Google Sheet

1. **Make a copy of the template Google Sheet** (link will be provided)
   - OR create a new Google Sheet from scratch using [GOOGLE-SHEETS-TEMPLATE.md](GOOGLE-SHEETS-TEMPLATE.md)

2. **Create 7 tabs** with these exact names:
   - `General`
   - `Hero`
   - `About`
   - `CoreValues`
   - `Services`
   - `ServiceDetails`
   - `Contact`

3. **Fill in your content** following the template structure

### Step 2: Publish Each Tab as CSV

This is the most important step! You need to publish each tab separately.

**For EACH of the 7 tabs**, do this:

1. Open your Google Sheet
2. Click on the tab you want to publish (e.g., "General")
3. Go to **File → Share → Publish to web**
4. In the dropdown:
   - First dropdown: Select the specific tab (e.g., "General")
   - Second dropdown: Select "Comma-separated values (.csv)"
5. Click **Publish**
6. Copy the URL that appears - it will look like:
   ```
   https://docs.google.com/spreadsheets/d/1AbCdEfGhIjKlMnOpQr.../export?format=csv&gid=0
   ```
7. Save this URL - you'll need it for the config file!

8. **Repeat for all 7 tabs!**

📝 **Pro tip:** Keep a note file with all 7 URLs labeled by tab name!

### Step 3: Configure the Website

1. In this GitHub repository, find the file `sheet_config.json.example`

2. Copy it and rename to `sheet_config.json`:
   ```bash
   cp sheet_config.json.example sheet_config.json
   ```

3. Open `sheet_config.json` and replace the URLs with your actual CSV URLs:

   ```json
   {
     "general_csv_url": "YOUR_GENERAL_TAB_CSV_URL_HERE",
     "hero_csv_url": "YOUR_HERO_TAB_CSV_URL_HERE",
     "about_csv_url": "YOUR_ABOUT_TAB_CSV_URL_HERE",
     "values_csv_url": "YOUR_COREVALUES_TAB_CSV_URL_HERE",
     "services_csv_url": "YOUR_SERVICES_TAB_CSV_URL_HERE",
     "service_details_csv_url": "YOUR_SERVICEDETAILS_TAB_CSV_URL_HERE",
     "contact_csv_url": "YOUR_CONTACT_TAB_CSV_URL_HERE"
   }
   ```

4. Save the file

5. Commit and push to GitHub:
   ```bash
   git add sheet_config.json
   git commit -m "Add Google Sheets configuration"
   git push
   ```

### Step 4: Test the Setup

1. Go to your GitHub repository
2. Click on the **"Actions"** tab at the top
3. Click on **"Update Website from Google Sheets"** workflow
4. Click the **"Run workflow"** button (right side)
5. Click the green **"Run workflow"** button in the dropdown
6. Wait about 30 seconds and refresh - you should see a completed run!
7. Check your website to see the updates

---

## ✏️ Daily Usage (For Your Team)

### How to Update the Website

1. **Edit the Google Sheet**
   - Change any text, images, or content
   - Add or remove services
   - Update stats or core values

2. **Trigger the update** (two options):

   **Option A: Manual Update (Recommended)**
   - Go to GitHub → Actions tab
   - Click "Update Website from Google Sheets"
   - Click "Run workflow" button
   - Wait ~30 seconds for completion
   - Check your website!

   **Option B: Automatic Update**
   - The website updates automatically every 6 hours
   - Just edit the sheet and wait
   - No action needed!

3. **Verify changes**
   - Visit your website to see the updates
   - Changes should appear within minutes

### 🖼️ How to Change Images

1. **Upload image to Google Drive**
   - Recommended size: 1920x1080 or larger for backgrounds
   - JPG or PNG format

2. **Share the image**
   - Right-click → Share
   - Set to "Anyone with the link can view"
   - Copy the link

3. **Convert the link**
   - Original link:
     ```
     https://drive.google.com/file/d/1AbCdEfGhIjKlMnOpQr.../view?usp=sharing
     ```
   - Extract the ID (the long string between `/d/` and `/view`)
   - Convert to:
     ```
     https://drive.google.com/uc?export=view&id=1AbCdEfGhIjKlMnOpQr...
     ```

4. **Paste into Google Sheet**
   - Put the converted URL in the appropriate image field
   - Save and trigger website update

📝 **Tip:** See [GOOGLE-SHEETS-TEMPLATE.md](GOOGLE-SHEETS-TEMPLATE.md) for a formula to auto-convert links!

### 🎨 How to Add New Services

1. **Add to Services tab**
   - Add a new row with: name, link_id, gradient
   - Example: `Web Design | web-design | from-blue-500 to-purple-500`

2. **Add to ServiceDetails tab**
   - Add a new row with full service details
   - Use the same `link_id` as above in the `service_id` column
   - Separate bullet points with `|` character

3. **Save and update**
   - The website will automatically create the new service page!

### 📝 How to Edit Core Values

1. **Go to CoreValues tab**
2. **Edit existing rows** or **add new rows**
3. Choose an emoji for the icon (Windows: Win + . | Mac: Cmd + Ctrl + Space)
4. Pick a gradient color (see template for options)
5. Save and update!

---

## 🔧 Advanced Configuration

### Change Update Frequency

Edit `.github/workflows/update-from-sheet.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Current: Every 6 hours
```

**Other options:**
- `'0 * * * *'` - Every hour
- `'0 */2 * * *'` - Every 2 hours
- `'0 */12 * * *'` - Every 12 hours
- `'0 0 * * *'` - Once per day at midnight
- `'0 9,17 * * 1-5'` - 9 AM and 5 PM, Monday-Friday

### Disable Automatic Updates

Remove or comment out the `schedule:` section in the workflow file.

---

## 🐛 Troubleshooting

### "Website didn't update"

**Check:**
1. ✅ Did you trigger the GitHub Action?
   - Go to Actions tab → Click "Update Website from Google Sheets" → "Run workflow"

2. ✅ Is `sheet_config.json` configured?
   - Check that the file exists and has all 7 URLs

3. ✅ Are the CSV URLs correct?
   - Test each URL by pasting in a browser - you should see CSV data

4. ✅ Did the GitHub Action succeed?
   - Go to Actions tab and check for ✅ green checkmark
   - If ❌ red X, click to see error logs

### "Images not showing"

**Check:**
1. ✅ Is the Google Drive image shared publicly?
   - Right-click image → Share → "Anyone with link can view"

2. ✅ Did you convert the URL correctly?
   - Should be: `https://drive.google.com/uc?export=view&id=FILE_ID`
   - NOT: `https://drive.google.com/file/d/FILE_ID/view`

3. ✅ Is the URL in the correct field?
   - Check GOOGLE-SHEETS-TEMPLATE.md for field names

### "New service not appearing"

**Check:**
1. ✅ Did you add it to BOTH tabs?
   - Services tab (for the overview card)
   - ServiceDetails tab (for the detail page)

2. ✅ Does the `link_id` match the `service_id`?
   - They must be exactly the same!
   - Use lowercase and hyphens only

### "GitHub Action failing"

**Check the logs:**
1. Go to Actions tab
2. Click on the failed run
3. Click on "update-website" job
4. Read the error message

**Common errors:**
- `sheet_config.json not found` → Create the config file
- `Error reading CSV` → Check that URLs are correct and publicly accessible
- `KeyError` → Check that column headers match template exactly

### "Permission denied when pushing"

This shouldn't happen with the default GitHub token, but if it does:
1. Go to repository Settings
2. Actions → General
3. Scroll to "Workflow permissions"
4. Select "Read and write permissions"
5. Click Save

---

## 👥 Team Management

### Giving Team Members Edit Access

1. Open your Google Sheet
2. Click "Share" button (top right)
3. Add team member's email
4. Set permission to "Editor"
5. Click "Send"

They can now edit the sheet but **cannot** change publish settings or delete the sheet.

### Roles

| Role | Can Edit Sheet | Can Trigger GitHub Action | Can Change Config |
|------|----------------|---------------------------|-------------------|
| Google Sheet Editor | ✅ | ❌ | ❌ |
| GitHub Collaborator | ❌ | ✅ | ✅ |
| Both | ✅ | ✅ | ✅ |

**Recommended:** Give most team members only Google Sheet edit access. They can edit content, and the website auto-updates every 6 hours.

---

## 📚 Reference Files

- **[GOOGLE-SHEETS-TEMPLATE.md](GOOGLE-SHEETS-TEMPLATE.md)** - Complete template structure with examples
- **sheet_config.json** - Your CSV URLs configuration (you create this)
- **sheet_config.json.example** - Example configuration file
- **update_website.py** - Python script (you don't need to edit this)
- **.github/workflows/update-from-sheet.yml** - GitHub Action workflow

---

## 🎓 Quick Start Checklist

For setup:
- [ ] Create Google Sheet with 7 tabs
- [ ] Fill in content following template
- [ ] Publish each tab as CSV
- [ ] Copy all 7 CSV URLs
- [ ] Create `sheet_config.json` with your URLs
- [ ] Commit and push to GitHub
- [ ] Test by running GitHub Action manually
- [ ] Verify website updated correctly

For daily use:
- [ ] Edit Google Sheet content
- [ ] Go to GitHub Actions
- [ ] Click "Run workflow"
- [ ] Wait 30 seconds
- [ ] Check website for updates!

---

## 💡 Tips & Best Practices

1. **Test changes in a copy first** if making major edits
2. **Use descriptive service names** that customers understand
3. **Keep paragraphs concise** - easier to read on mobile
4. **Use high-quality images** - minimum 1920x1080 for backgrounds
5. **Back up your sheet** - File → Make a copy (monthly)
6. **Version history** - File → Version history → See version history
7. **Coordinate edits** - Use Google Sheets comments to discuss changes
8. **Check mobile view** - Most visitors use phones!

---

## ❓ FAQ

**Q: Can I make the Google Sheet private?**
A: The published CSV is public (read-only), but edit permission stays private. This is fine because the website content is already public anyway.

**Q: How long until changes appear?**
A: Manual trigger: ~30 seconds. Automatic: up to 6 hours (or whatever schedule you set).

**Q: Can I add more than 3 services?**
A: Yes! Just add more rows to the Services and ServiceDetails tabs. The website adapts automatically.

**Q: What if I break something?**
A: Use Google Sheets version history to restore previous content. The website will revert on the next update.

**Q: Do I need to know Python?**
A: No! You only need to edit the Google Sheet. The Python script runs automatically.

**Q: Can I use Excel instead?**
A: No, it must be Google Sheets for the CSV publishing feature to work.

**Q: How much does this cost?**
A: $0! Everything uses free tiers (GitHub Free, Google Sheets, Google Drive).

---

## 🆘 Getting Help

If you're stuck:

1. **Check this README** - most questions are answered here
2. **Check GOOGLE-SHEETS-TEMPLATE.md** - for content structure questions
3. **Check GitHub Action logs** - for technical errors
4. **Google Sheets version history** - to undo changes
5. **Ask your developer friend** - they set this up for you! 😊

---

## 🎉 You're Ready!

That's it! You now have a powerful, codeless website management system. Your team can update the website as easily as editing a spreadsheet.

**Happy editing! 🚀**
