#!/usr/bin/env python3
"""
Website Content Manager - Updates website from Google Sheets CSV
Reads content from published Google Sheets and regenerates the website HTML
"""

import csv
import urllib.request
import json
import os
import re
from typing import Dict, List, Any
from urllib.parse import urlparse, parse_qs

def read_csv_from_url(url: str) -> List[Dict[str, str]]:
    """Read CSV data from a URL and return as list of dictionaries"""
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
            reader = csv.DictReader(content.splitlines())
            return list(reader)
    except Exception as e:
        print(f"Error reading CSV from {url}: {e}")
        return []

def load_config() -> Dict[str, str]:
    """Load CSV URLs from config file"""
    try:
        with open('sheet_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: sheet_config.json not found!")
        print("Please create sheet_config.json with your Google Sheets CSV URLs")
        exit(1)

def extract_gdrive_file_id(url: str) -> str:
    """Extract Google Drive file ID from various URL formats"""
    if not url or not isinstance(url, str):
        return None

    # Match various Google Drive URL formats
    patterns = [
        r'/d/([a-zA-Z0-9_-]+)',  # /d/FILE_ID format
        r'id=([a-zA-Z0-9_-]+)',   # id=FILE_ID format
        r'/file/d/([a-zA-Z0-9_-]+)',  # /file/d/FILE_ID format
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None

def download_image_from_gdrive(gdrive_url: str, local_filename: str) -> bool:
    """Download an image from Google Drive and save to images/ folder"""
    # Extract file ID
    file_id = extract_gdrive_file_id(gdrive_url)
    if not file_id:
        print(f"  ⚠️  Could not extract file ID from: {gdrive_url}")
        return False

    # Create download URL
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # Ensure images directory exists
    os.makedirs('images', exist_ok=True)

    # Full path for the image
    filepath = os.path.join('images', local_filename)

    try:
        print(f"  📥 Downloading {local_filename}...")
        urllib.request.urlretrieve(download_url, filepath)
        print(f"  ✅ Saved to {filepath}")
        return True
    except Exception as e:
        print(f"  ❌ Error downloading {local_filename}: {e}")
        return False

def is_gdrive_url(url: str) -> bool:
    """Check if URL is a Google Drive URL"""
    if not url or not isinstance(url, str):
        return False
    return 'drive.google.com' in url or 'googleusercontent.com' in url

def process_image_url(url: str, default_filename: str) -> str:
    """
    Process image URL - download from Google Drive if needed, return local path

    Args:
        url: The image URL (Google Drive or local path)
        default_filename: Filename to use if downloading from Google Drive

    Returns:
        Local path to use in HTML (e.g., 'images/logo.png')
    """
    if not url:
        return ''

    # If it's already a local path, return as-is
    if url.startswith('images/'):
        return url

    # If it's a Google Drive URL, download it
    if is_gdrive_url(url):
        if download_image_from_gdrive(url, default_filename):
            return f'images/{default_filename}'
        else:
            # Return empty or original URL as fallback
            return ''

    # Otherwise, assume it's a valid external URL
    return url

def parse_general_info(data: List[Dict]) -> Dict[str, str]:
    """Parse general site information"""
    info = {}
    for row in data:
        if row.get('field') and row.get('value'):
            info[row['field']] = row['value']
    return info

def parse_hero(data: List[Dict]) -> Dict[str, str]:
    """Parse hero section data"""
    hero = {}
    for row in data:
        if row.get('field') and row.get('value'):
            hero[row['field']] = row['value']
    return hero

def parse_about(data: List[Dict]) -> Dict[str, Any]:
    """Parse about section data"""
    about = {
        'title': '',
        'paragraphs': [],
        'stats': []
    }
    for row in data:
        field = row.get('field', '')
        value = row.get('value', '')
        if field == 'title':
            about['title'] = value
        elif field.startswith('paragraph'):
            about['paragraphs'].append(value)
        elif field.endswith('_number'):
            stat_key = field.replace('_number', '')
            stat = next((s for s in about['stats'] if s['key'] == stat_key), None)
            if not stat:
                stat = {'key': stat_key, 'number': value, 'label': ''}
                about['stats'].append(stat)
            else:
                stat['number'] = value
        elif field.endswith('_label'):
            stat_key = field.replace('_label', '')
            stat = next((s for s in about['stats'] if s['key'] == stat_key), None)
            if not stat:
                stat = {'key': stat_key, 'number': '', 'label': value}
                about['stats'].append(stat)
            else:
                stat['label'] = value
    return about

def parse_core_values(data: List[Dict]) -> List[Dict[str, str]]:
    """Parse core values data"""
    values = []
    for row in data:
        if row.get('icon') and row.get('title'):
            values.append({
                'icon': row.get('icon', '🎯'),
                'title': row.get('title', ''),
                'description': row.get('description', ''),
                'gradient': row.get('gradient', 'from-blue-500 to-cyan-500')
            })
    return values

def parse_services(data: List[Dict]) -> List[Dict[str, str]]:
    """Parse services overview data"""
    services = []
    for row in data:
        if row.get('name'):
            services.append({
                'name': row.get('name', ''),
                'link_id': row.get('link_id', ''),
                'gradient': row.get('gradient', 'from-blue-500 to-cyan-500')
            })
    return services

def parse_service_details(data: List[Dict]) -> List[Dict[str, Any]]:
    """Parse detailed service pages data"""
    details = []
    for row in data:
        if row.get('service_id'):
            # Parse bullet points (separated by | character)
            bullets = row.get('key_services', '').split('|') if row.get('key_services') else []
            bullets = [b.strip() for b in bullets if b.strip()]

            details.append({
                'service_id': row.get('service_id', ''),
                'title': row.get('title', ''),
                'intro': row.get('intro', ''),
                'bullets_title': row.get('bullets_title', 'Key Services Include:'),
                'bullets': bullets,
                'closing': row.get('closing', ''),
                'bg_image': row.get('bg_image', ''),
                'image_position': row.get('image_position', 'right')  # left or right
            })
    return details

def parse_contact(data: List[Dict]) -> Dict[str, str]:
    """Parse contact section data"""
    contact = {}
    for row in data:
        if row.get('field') and row.get('value'):
            contact[row['field']] = row['value']
    return contact

def generate_html(general: Dict, hero: Dict, about: Dict, values: List,
                 services: List, service_details: List, contact: Dict) -> str:
    """Generate complete HTML from data"""

    # Generate stats HTML
    stats_html = '\n'.join([
        f'''                    <div class="text-center">
                        <div class="text-4xl font-bold text-blue-400 mb-2">{stat['number']}</div>
                        <div class="text-gray-400">{stat['label']}</div>
                    </div>'''
        for stat in about.get('stats', [])
    ])

    # Generate core values HTML
    values_html = '\n'.join([
        f'''                <!-- Core Value {i+1} -->
                <div class="group relative p-8 rounded-lg shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden bg-gradient-to-br {value['gradient']} hover:scale-105 fade-in{' animation-delay-' + str((i+1)*200) if i > 0 else ''}">
                    <div class="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 transition-opacity"></div>
                    <div class="text-white text-5xl mb-4 relative z-10">{value['icon']}</div>
                    <h3 class="text-2xl font-bold mb-4 text-white relative z-10">{value['title']}</h3>
                    <p class="text-white text-opacity-90 relative z-10">
                        {value['description']}
                    </p>
                </div>'''
        for i, value in enumerate(values)
    ])

    # Generate services overview HTML
    services_html = '\n'.join([
        f'''                <!-- Service {i+1} -->
                <a href="#{service['link_id']}" class="group relative p-8 rounded-lg shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer overflow-hidden bg-gradient-to-br {service['gradient']} hover:scale-105 fade-in{' animation-delay-' + str((i+1)*200) if i > 0 else ''}">
                    <div class="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 transition-opacity"></div>
                    <h3 class="text-2xl font-bold text-center text-white relative z-10">{service['name']}</h3>
                </a>'''
        for i, service in enumerate(services)
    ])

    # Generate service detail sections HTML
    service_details_html = '\n'.join([
        generate_service_detail_section(detail, i)
        for i, detail in enumerate(service_details)
    ])

    # Generate about paragraphs
    about_paragraphs = '\n'.join([
        f'''                <p class="text-lg text-gray-300 mb-6">
                    {para}
                </p>'''
        for para in about.get('paragraphs', [])
    ])

    html = f'''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{general.get('site_title', 'TriStar')}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Fade-in animation */
        .fade-in {{
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.8s ease-out, transform 0.8s ease-out;
        }}

        .fade-in.show {{
            opacity: 1;
            transform: translateY(0);
        }}

        /* Animation delays */
        .animation-delay-200 {{
            animation-delay: 0.2s;
        }}

        .animation-delay-400 {{
            animation-delay: 0.4s;
        }}

        .animation-delay-600 {{
            animation-delay: 0.6s;
        }}

        .animation-delay-2000 {{
            animation-delay: 2s;
        }}

        .animation-delay-4000 {{
            animation-delay: 4s;
        }}

        /* Blob animation */
        @keyframes blob {{
            0%, 100% {{
                transform: translate(0, 0) scale(1);
            }}
            25% {{
                transform: translate(100px, -50px) scale(1.2);
            }}
            50% {{
                transform: translate(-100px, 100px) scale(0.8);
            }}
            75% {{
                transform: translate(50px, 50px) scale(1.1);
            }}
        }}

        .animate-blob {{
            animation: blob 10s ease-in-out infinite;
        }}
    </style>
</head>
<body class="bg-gray-900">
    <!-- Navigation -->
    <nav class="fixed w-full bg-gray-900 bg-opacity-95 backdrop-blur-sm shadow-lg border-b border-gray-800 z-50">
        <div class="container mx-auto px-6 py-4">
            <div class="flex justify-between items-center">
                <!-- Logo with text -->
                <a href="#home" class="flex items-center">
                    <img src="{general.get('logo_url', 'images/logo.png')}" alt="{general.get('company_name', 'TriStar')} Logo" class="h-10 w-auto mr-4">
                    <span class="text-4xl font-bold text-[#D81400]">{general.get('company_name', 'TRI STAR')}</span>
                </a>
                <div class="hidden md:flex space-x-8">
                    <a href="#home" class="text-gray-300 hover:text-white transition">Home</a>
                    <a href="#about" class="text-gray-300 hover:text-white transition">About</a>
                    <a href="#services" class="text-gray-300 hover:text-white transition">Services</a>
                    <a href="#contact" class="text-gray-300 hover:text-white transition">Contact</a>
                </div>
                <!-- Mobile menu button -->
                <button id="mobile-menu-button" class="md:hidden text-gray-300">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>
            </div>
            <!-- Mobile menu -->
            <div id="mobile-menu" class="hidden md:hidden mt-4 space-y-2">
                <a href="#home" class="block text-gray-300 hover:text-white transition">Home</a>
                <a href="#about" class="block text-gray-300 hover:text-white transition">About</a>
                <a href="#services" class="block text-gray-300 hover:text-white transition">Services</a>
                <a href="#contact" class="block text-gray-300 hover:text-white transition">Contact</a>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600 text-white pt-20">
        <div class="container mx-auto px-6 text-center">
            <h1 class="text-5xl md:text-6xl font-bold mb-6">{hero.get('title', 'Welcome to TriStar')}</h1>
            <p class="text-xl md:text-2xl mb-8 text-blue-100">{hero.get('subtitle', 'Building foundations for success')}</p>
            <a href="#about" class="inline-block bg-white text-blue-600 px-8 py-3 rounded-full font-semibold hover:bg-blue-50 transition">
                {hero.get('button_text', 'Learn More')}
            </a>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="min-h-screen flex items-center py-20 bg-gray-800">
        <div class="container mx-auto px-6">
            <h2 class="text-4xl font-bold text-center mb-12 text-white">{about.get('title', 'About Us')}</h2>
            <div class="max-w-3xl mx-auto">
{about_paragraphs}
                <div class="grid md:grid-cols-{len(about.get('stats', []))} gap-8 mt-12">
{stats_html}
                </div>
            </div>
        </div>
    </section>

    <!-- Core Values Section -->
    <section id="core-values" class="min-h-screen flex items-center py-20 bg-gray-900 relative overflow-hidden">
        <!-- Decorative elements -->
        <div class="absolute top-0 left-0 w-96 h-96 bg-purple-600 rounded-full mix-blend-lighten filter blur-2xl opacity-20 animate-blob"></div>
        <div class="absolute bottom-0 right-0 w-96 h-96 bg-pink-600 rounded-full mix-blend-lighten filter blur-2xl opacity-20 animate-blob animation-delay-4000"></div>

        <div class="container mx-auto px-6 relative z-10">
            <h2 class="text-4xl font-bold text-center mb-12 text-white fade-in">Our Core Values</h2>
            <div class="grid md:grid-cols-{len(values)} gap-8 max-w-5xl mx-auto">
{values_html}
            </div>
        </div>

        <!-- Wave divider at bottom -->
        <div class="absolute bottom-0 left-0 right-0">
            <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M0 120L60 105C120 90 240 60 360 45C480 30 600 30 720 37.5C840 45 960 60 1080 67.5C1200 75 1320 75 1380 75L1440 75V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0V120Z" fill="#1f2937"/>
            </svg>
        </div>
    </section>

    <!-- Services Section -->
    <section id="services" class="min-h-screen flex items-center py-20 bg-gray-800 relative overflow-hidden">
        <!-- Decorative elements -->
        <div class="absolute top-0 right-0 w-96 h-96 bg-blue-600 rounded-full mix-blend-lighten filter blur-2xl opacity-20 animate-blob"></div>
        <div class="absolute bottom-0 left-0 w-96 h-96 bg-purple-600 rounded-full mix-blend-lighten filter blur-2xl opacity-20 animate-blob animation-delay-2000"></div>

        <div class="container mx-auto px-6 relative z-10">
            <h2 class="text-4xl font-bold text-center mb-12 text-white fade-in">Our Services</h2>
            <div class="grid md:grid-cols-{len(services)} gap-8 max-w-5xl mx-auto">
{services_html}
            </div>
        </div>

        <!-- Wave divider at bottom -->
        <div class="absolute bottom-0 left-0 right-0">
            <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M0 120L60 105C120 90 240 60 360 45C480 30 600 30 720 37.5C840 45 960 60 1080 67.5C1200 75 1320 75 1380 75L1440 75V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0V120Z" fill="#000000"/>
            </svg>
        </div>
    </section>

{service_details_html}

    <!-- Contact Section -->
    <section id="contact" class="min-h-screen flex items-center py-20 bg-gray-900">
        <div class="container mx-auto px-6">
            <h2 class="text-4xl font-bold text-center mb-12 text-white">{contact.get('title', 'Get In Touch')}</h2>
            <div class="max-w-2xl mx-auto">
                <form class="space-y-6">
                    <div>
                        <label class="block text-gray-300 mb-2 font-semibold">{contact.get('name_label', 'Name')}</label>
                        <input type="text" class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 text-white placeholder-gray-500" placeholder="{contact.get('name_placeholder', 'Your name')}">
                    </div>
                    <div>
                        <label class="block text-gray-300 mb-2 font-semibold">{contact.get('email_label', 'Email')}</label>
                        <input type="email" class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 text-white placeholder-gray-500" placeholder="{contact.get('email_placeholder', 'your@email.com')}">
                    </div>
                    <div>
                        <label class="block text-gray-300 mb-2 font-semibold">{contact.get('message_label', 'Message')}</label>
                        <textarea rows="5" class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 text-white placeholder-gray-500" placeholder="{contact.get('message_placeholder', 'Your message')}"></textarea>
                    </div>
                    <button type="submit" class="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition">
                        {contact.get('button_text', 'Send Message')}
                    </button>
                </form>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-black text-gray-400 py-8 border-t border-gray-800">
        <div class="container mx-auto px-6 text-center">
            <p>{general.get('footer_text', '© 2025 TriStar. All rights reserved.')}</p>
        </div>
    </footer>

    <!-- Mobile menu toggle script -->
    <script>
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');

        mobileMenuButton.addEventListener('click', () => {{
            mobileMenu.classList.toggle('hidden');
        }});

        // Close mobile menu when clicking a link
        const mobileLinks = mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {{
            link.addEventListener('click', () => {{
                mobileMenu.classList.add('hidden');
            }});
        }});

        // Scroll animations with fade in and out
        const observerOptions = {{
            threshold: 0.15,
            rootMargin: '0px 0px -50px 0px'
        }};

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('show');
                }} else {{
                    entry.target.classList.remove('show');
                }}
            }});
        }}, observerOptions);

        // Observe all fade-in elements
        document.addEventListener('DOMContentLoaded', () => {{
            const fadeElements = document.querySelectorAll('.fade-in');
            fadeElements.forEach(el => observer.observe(el));
        }});
    </script>
</body>
</html>
'''
    return html

def text_to_paragraphs(text: str, css_class: str = "text-lg text-gray-200 mb-6") -> str:
    """
    Convert text with line breaks or separators into multiple HTML paragraphs

    Supports:
    - Double pipe separator: ||
    - Newline characters: \n
    - Multiple consecutive newlines
    """
    if not text:
        return ''

    # Split by double pipe separator OR by double newlines
    # First try double pipe
    if '||' in text:
        paragraphs = [p.strip() for p in text.split('||') if p.strip()]
    else:
        # Split by newlines and group consecutive text
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        # If no double newlines, try single newlines
        if len(paragraphs) <= 1:
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
            # If still just one paragraph, keep it as is
            if len(paragraphs) <= 1:
                paragraphs = [text.strip()]

    # Generate HTML for each paragraph
    paragraphs_html = '\n'.join([
        f'                    <p class="{css_class}">\n                        {para}\n                    </p>'
        for para in paragraphs if para
    ])

    return paragraphs_html

def generate_service_detail_section(detail: Dict, index: int) -> str:
    """Generate HTML for a service detail section"""

    # Determine image position and gradient direction
    if detail['image_position'] == 'left':
        mask_gradient = "linear-gradient(to right, rgba(0,0,0,1) 0%, rgba(0,0,0,0.8) 50%, rgba(0,0,0,0) 100%)"
        grid_order = '''                <!-- Empty space for image on the left -->
                <div class="hidden md:block"></div>
                <!-- Text content on the right -->'''
    else:  # right
        mask_gradient = "linear-gradient(to left, rgba(0,0,0,1) 0%, rgba(0,0,0,0.8) 50%, rgba(0,0,0,0) 100%)"
        grid_order = '''                <!-- Text content on the left -->'''

    # Generate bullet points
    bullets_html = '\n'.join([
        f'                        <li>{bullet}</li>'
        for bullet in detail['bullets']
    ])

    # Convert intro and closing text to paragraphs
    intro_html = text_to_paragraphs(detail.get('intro', ''))
    closing_html = text_to_paragraphs(detail.get('closing', ''))

    section = f'''
    <!-- {detail['title']} Detail Section -->
    <section id="{detail['service_id']}" class="min-h-screen flex items-center py-20 bg-black relative overflow-hidden">
        <!-- Background image -->
        <div class="absolute inset-0 bg-cover bg-center" style="background-image: url('{detail['bg_image']}'); -webkit-mask-image: {mask_gradient}; mask-image: {mask_gradient};"></div>

        <div class="container mx-auto px-6 relative z-10">
            <div class="grid md:grid-cols-2 gap-12 items-center">
{grid_order}
                <div class="text-white">
                    <h2 class="text-4xl md:text-5xl font-bold mb-8">{detail['title']}</h2>
{intro_html}
                    <h3 class="text-2xl font-bold mb-4">{detail['bullets_title']}</h3>
                    <ul class="list-disc list-inside space-y-2 text-gray-200 mb-6">
{bullets_html}
                    </ul>
{closing_html}
                </div>'''

    # Add closing div for image position
    if detail['image_position'] == 'right':
        section += '''
                <!-- Empty space for image on the right -->
                <div class="hidden md:block"></div>'''

    section += '''
            </div>
        </div>
    </section>'''

    return section

def process_all_images(general: Dict, service_details: List) -> None:
    """
    Download all Google Drive images to local images/ folder

    Modifies the data structures in-place to use local paths
    """
    print("🖼️  Processing images...")

    # Process logo
    if 'logo_url' in general and is_gdrive_url(general['logo_url']):
        print("  Processing logo...")
        general['logo_url'] = process_image_url(general['logo_url'], 'logo.png')

    # Process service detail background images
    for i, detail in enumerate(service_details):
        if 'bg_image' in detail and is_gdrive_url(detail['bg_image']):
            # Create a filename based on service_id
            filename = f"{detail.get('service_id', f'service-{i}')}-bg.jpg"
            print(f"  Processing {detail.get('title', 'service')} background...")
            detail['bg_image'] = process_image_url(detail['bg_image'], filename)

    print("✅ Image processing complete")

def main():
    """Main function to update website from Google Sheets"""
    print("🚀 Starting website update from Google Sheets...")

    # Load configuration
    config = load_config()
    print("✅ Loaded configuration")

    # Read all CSV data
    print("📊 Reading data from Google Sheets...")
    general_data = read_csv_from_url(config.get('general_csv_url', ''))
    hero_data = read_csv_from_url(config.get('hero_csv_url', ''))
    about_data = read_csv_from_url(config.get('about_csv_url', ''))
    values_data = read_csv_from_url(config.get('values_csv_url', ''))
    services_data = read_csv_from_url(config.get('services_csv_url', ''))
    service_details_data = read_csv_from_url(config.get('service_details_csv_url', ''))
    contact_data = read_csv_from_url(config.get('contact_csv_url', ''))

    # Parse data
    print("🔍 Parsing data...")
    general = parse_general_info(general_data)
    hero = parse_hero(hero_data)
    about = parse_about(about_data)
    values = parse_core_values(values_data)
    services = parse_services(services_data)
    service_details = parse_service_details(service_details_data)
    contact = parse_contact(contact_data)

    print(f"  - General info: {len(general)} fields")
    print(f"  - Hero section: {len(hero)} fields")
    print(f"  - About section: {len(about.get('paragraphs', []))} paragraphs, {len(about.get('stats', []))} stats")
    print(f"  - Core values: {len(values)} values")
    print(f"  - Services: {len(services)} services")
    print(f"  - Service details: {len(service_details)} detailed pages")
    print(f"  - Contact info: {len(contact)} fields")

    # Process and download images
    process_all_images(general, service_details)

    # Generate HTML
    print("🔨 Generating HTML...")
    html = generate_html(general, hero, about, values, services, service_details, contact)

    # Write to file
    print("💾 Writing to index.html...")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("✨ Website updated successfully!")
    print("🌐 Your website has been regenerated from Google Sheets data")

if __name__ == "__main__":
    main()
