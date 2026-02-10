#!/usr/bin/env python3
"""
Smart Image Organizer

Sort photos by date, size, and remove duplicates.
"""

import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from PIL import Image
from collections import defaultdict


def get_image_date(image_path):
    """Extract the date taken from image EXIF data or file modification time."""
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if exif:
            for tag, value in exif.items():
                if tag == 36867:  # DateTimeOriginal
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except:
        pass
    # Fallback to file modification time
    return datetime.fromtimestamp(os.path.getmtime(image_path))


def get_image_size(image_path):
    """Get image dimensions."""
    try:
        img = Image.open(image_path)
        return img.size  # (width, height)
    except:
        return (0, 0)


def categorize_by_size(width, height):
    """Categorize image by dimensions."""
    total_pixels = width * height
    if total_pixels < 500000:  # < 0.5MP (screenshots, icons)
        return 'small'
    elif total_pixels < 2000000:  # 0.5-2MP (small photos)
        return 'medium'
    else:  # > 2MP (high-res photos)
        return 'large'


def calculate_file_hash(file_path):
    """Calculate MD5 hash of a file for duplicate detection."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def organize_by_date(source_dir, target_dir='organized_by_date'):
    """Organize images into folders by year/month."""
    source_path = Path(source_dir)
    target_path = source_path / target_dir
    target_path.mkdir(exist_ok=True)
    
    organized = defaultdict(list)
    
    for img_file in source_path.glob('*.*'):
        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']:
            try:
                date = get_image_date(img_file)
                folder = target_path / str(date.year) / f"{date.month:02d}"
                folder.mkdir(parents=True, exist_ok=True)
                
                new_name = f"{date.strftime('%Y%m%d_%H%M%S')}{img_file.suffix}"
                target_file = folder / new_name
                
                counter = 1
                while target_file.exists():
                    new_name = f"{date.strftime('%Y%m%d_%H%M%S')}_{counter}{img_file.suffix}"
                    target_file = folder / new_name
                    counter += 1
                
                shutil.copy2(img_file, target_file)
                organized['date'].append((img_file.name, str(target_file.relative_to(source_path))))
            except Exception as e:
                print(f"Error processing {img_file}: {e}")
    
    return dict(organized)


def organize_by_size(source_dir, target_dir='organized_by_size'):
    """Organize images into folders by size category."""
    source_path = Path(source_dir)
    target_path = source_path / target_dir
    target_path.mkdir(exist_ok=True)
    
    organized = defaultdict(list)
    categories = {'small': target_path / 'small',
                  'medium': target_path / 'medium',
                  'large': target_path / 'large'}
    
    for cat in categories.values():
        cat.mkdir(exist_ok=True)
    
    for img_file in source_path.glob('*.*'):
        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']:
            try:
                width, height = get_image_size(img_file)
                category = categorize_by_size(width, height)
                
                target_file = categories[category] / img_file.name
                counter = 1
                while target_file.exists():
                    new_name = f"{img_file.stem}_{counter}{img_file.suffix}"
                    target_file = categories[category] / new_name
                    counter += 1
                
                shutil.copy2(img_file, target_file)
                organized[category].append((img_file.name, str(target_file.relative_to(source_path))))
            except Exception as e:
                print(f"Error processing {img_file}: {e}")
    
    return dict(organized)


def find_duplicates(source_dir):
    """Find duplicate images using file hash."""
    source_path = Path(source_dir)
    hash_to_files = defaultdict(list)
    
    for img_file in source_path.glob('*.*'):
        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']:
            try:
                file_hash = calculate_file_hash(img_file)
                hash_to_files[file_hash].append(img_file)
            except Exception as e:
                print(f"Error hashing {img_file}: {e}")
    
    duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
    return duplicates


def remove_duplicates(source_dir, keep='first'):
    """Remove duplicate images, keeping the first (or last) one."""
    duplicates = find_duplicates(source_dir)
    removed = []
    
    for hash_val, files in duplicates.items():
        files.sort(key=lambda f: f.stat().st_mtime)
        
        if keep == 'last':
            files_to_remove = files[:-1]
        else:
            files_to_remove = files[1:]
        
        for file in files_to_remove:
            file.unlink()
            removed.append(file.name)
    
    return removed


def main():
    """Main function to demonstrate usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Smart Image Organizer')
    parser.add_argument('source', help='Source directory containing images')
    parser.add_argument('--by-date', action='store_true', help='Organize by date')
    parser.add_argument('--by-size', action='store_true', help='Organize by size')
    parser.add_argument('--find-dupes', action='store_true', help='Find duplicates')
    parser.add_argument('--remove-dupes', action='store_true', help='Remove duplicates')
    parser.add_argument('--keep', choices=['first', 'last'], default='first',
                        help='Which duplicate to keep (default: first)')
    
    args = parser.parse_args()
    
    if args.by_date:
        result = organize_by_date(args.source)
        print("Organized by date:")
        for folder, files in result.get('date', []):
            print(f"  {folder} -> {files}")
    
    elif args.by_size:
        result = organize_by_size(args.source)
        print("Organized by size:")
        for category, files in result.items():
            for orig, new in files:
                print(f"  {category}: {orig} -> {new}")
    
    elif args.find_dupes:
        duplicates = find_duplicates(args.source)
        if duplicates:
            print("Found duplicates:")
            for hash_val, files in duplicates.items():
                print(f"  {len(files)} copies: {[f.name for f in files]}")
        else:
            print("No duplicates found.")
    
    elif args.remove_dupes:
        removed = remove_duplicates(args.source, keep=args.keep)
        if removed:
            print(f"Removed {len(removed)} duplicate(s):")
            for name in removed:
                print(f"  - {name}")
        else:
            print("No duplicates to remove.")


if __name__ == '__main__':
    main()
