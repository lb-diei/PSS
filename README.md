# 🪄 Photo Sorter

**Smart Image Organizer - Sort by Date, Size, and Remove Duplicates**



## What It Does

| Before (Messy) | After (Organized) |
|----------------|-------------------|
| photos/        | organized_by_date/ |
| photo1.jpg     | 2026/01/20260115_103022.jpg |
| screenshot.png | organized_by_size/small/screenshot.png |
| vacation.jpg   | 2025/12/20251220_150430.jpg |


## Features

- Sort by Date - Organize photos by year/month folders
- Sort by Size - Separate screenshots from high-res photos
- Remove Duplicates - Find and delete identical images
- Safe Operation - Copy mode by default, no data loss


## Quick Start

```bash
# Install dependencies
pip install pillow

# Organize photos by date
python image_organizer.py photos/ --by-date

# Organize by size (small/medium/large)
python image_organizer.py photos/ --by-size

# Find duplicates
python image_organizer.py photos/ --find-dupes

# Remove duplicates (keeps first found)
python image_organizer.py photos/ --remove-dupes
```


## Command Options

| Option | Description |
|--------|------------|
| --by-date | Sort into year/month folders |
| --by-size | Sort into small/medium/large folders |
| --find-dupes | Show duplicate files |
| --remove-dupes | Delete duplicate files |
| --keep first/last | Which duplicate to keep |


## Size Categories

| Category | Resolution | Description |
|----------|-----------|-------------|
| Small | < 0.5MP | Screenshots, icons, thumbnails |
| Medium | 0.5-2MP | Standard photos, web images |
| Large | > 2MP | High-res photos, originals |


## Examples

Organize by Date:

| Original | Organized To |
|----------|-------------|
| photo1.jpg | 2026/01/20260115_103022.jpg |
| vacation.jpg | 2025/12/20251220_150430.jpg |
| screenshot.png | 2026/02/20260210_093000.png |

Organize by Size:

| Original | Category | Organized To |
|----------|---------|--------------|
| icon.png | small | small/icon.png |
| photo.jpg | medium | medium/photo.jpg |
| wedding.jpg | large | large/wedding.jpg |

Find Duplicates:

| Hash Match | Files Found |
|------------|------------|
| abc123... | photo.jpg, photo_copy.jpg |
| def456... | screenshot.png, screenshot_backup.png |


## Requirements

| Item | Version |
|------|---------|
| Python | 3.6+ |
| Pillow | Latest |


## Installation

```bash
# Clone this repository
git clone https://github.com/lb-diei/lb02.git

# Install dependencies
cd lb02
pip install -r requirements.txt
```


## Usage

```bash
# Basic usage
python image_organizer.py /path/to/photos/

# Organize by date
python image_organizer.py /path/to/photos/ --by-date

# Organize by size
python image_organizer.py /path/to/photos/ --by-size

# Find duplicates
python image_organizer.py /path/to/photos/ --find-dupes

# Remove duplicates (keeps first)
python image_organizer.py /path/to/photos/ --remove-dupes

# Remove duplicates (keeps last modified)
python image_organizer.py /path/to/photos/ --remove-dupes --keep last
```


## Important Notes

1. Original files are preserved (copy mode)
2. Duplicates are permanently deleted
3. EXIF data is used for date if available
4. Falls back to file modification time


## Technical Details

| Feature | Implementation |
|---------|---------------|
| Date Detection | PIL/Pillow EXIF reading |
| Size Detection | Image dimensions |
| Duplicate Detection | MD5 file hashing |
| File Operations | Python shutil |


## Changelog

### v1.0.0 (2025~2026)
- Initial release
- Date-based organization
- Size-based organization
- Duplicate detection and removal


## Contributing

Issues and Pull Requests welcome!


## License

MIT License - Free to use and modify


## Author

Created with Claude Code
