from flask import Flask, render_template, request, send_from_directory
import qrcode
from qrcode.image.pil import PilImage
from PIL import Image, ImageDraw, ImageFont
import os
import colorsys

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def hex_to_rgba(hex_color, alpha=255):
    """Convert hex color to RGBA tuple"""
    rgb = hex_to_rgb(hex_color)
    return rgb + (alpha,)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form inputs
    name = request.form.get('name', 'N/A').strip()
    email = request.form.get('email', 'N/A').strip()
    phone = request.form.get('phone', 'N/A').strip()
    profession = request.form.get('profession', 'N/A').strip()
    address = request.form.get('address', 'N/A').strip()
    linkedin = request.form.get('linkedin', 'N/A').strip()
    
    # Theme and color options
    theme = request.form.get('theme', 'gold')
    accent_color = request.form.get('accent_color', '#FFD700')
    bg_start = request.form.get('bg_start', '#1e1e1e')
    bg_end = request.form.get('bg_end', '#505050')
    
    # Layout options
    card_width = int(request.form.get('card_width', 900))
    card_height = int(request.form.get('card_height', 500))
    layout_style = request.form.get('layout_style', 'standard')
    
    # Typography options
    font_style = request.form.get('font_style', 'montserrat')
    
    # Visual effects options
    show_shadow = request.form.get('show_shadow') == 'on'
    show_glass = request.form.get('show_glass') == 'on'
    show_border = request.form.get('show_border') == 'on'
    show_header = request.form.get('show_header') == 'on'
    show_qr = request.form.get('show_qr') == 'on'
    
    # QR code options
    qr_size = int(request.form.get('qr_size', 110))
    qr_color = request.form.get('qr_color', '#000000')
    qr_bg_color = request.form.get('qr_bg_color', '#FFFFFF')

    # Logo option
    header_logo_option = request.form.get('header_logo_option', 'zc')
    logo_file = request.files.get('logo_file')
    logo_path = None
    if header_logo_option == 'custom' and logo_file and logo_file.filename:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_file.filename)
        logo_file.save(logo_path)

    print("DEBUG: Generating card for", name)

    # Theme color map for new themes
    theme_colors = {
        'magenta_neutrals': {
            'bg': '#EFD6D2', 'text': '#17293A', 'accent': '#BB2649', 'divider': '#CFC7B2'
        },
        'vibrant_energetic': {
            'bg': '#EDEAB1', 'text': '#512C3A', 'accent': '#FF654F', 'divider': '#71ADBA'
        },
        'soft_pastel': {
            'bg': '#f5e2b7', 'text': '#b54f7a', 'accent': '#e2a1c4', 'divider': '#d58bb0'
        },
        'clean_dark': {
            'bg': '#141414', 'text': '#FFFFFF', 'accent': '#FF654F', 'divider': '#282828'
        },
    }
    # Use custom colors if theme is custom, otherwise use preset
    if theme == 'custom':
        accent = hex_to_rgb(accent_color)
        grad_start = hex_to_rgb(bg_start)
        grad_end = hex_to_rgb(bg_end)
        text_color = '#111111'
        divider_color = '#CCCCCC'
        bg_hex = bg_start
    else:
        t = theme_colors[theme]
        accent = hex_to_rgb(t['accent'])
        grad_start = grad_end = hex_to_rgb(t['bg'])
        text_color = t['text']
        divider_color = t['divider']
        bg_hex = t['bg']

    # Font selection
    font_files = {
        'montserrat': {
            'bold': 'Montserrat-Bold.ttf',
            'regular': 'Montserrat-Regular.ttf'
        },
        'roboto': {
            'bold': 'Roboto-Bold.ttf',
            'regular': 'Roboto-Regular.ttf'
        },
        'opensans': {
            'bold': 'OpenSans-Bold.ttf',
            'regular': 'OpenSans-Regular.ttf'
        }
    }
    
    try:
        if font_style in font_files:
            font_name = ImageFont.truetype(font_files[font_style]['bold'], 56)
            font_title = ImageFont.truetype(font_files[font_style]['regular'], 36)
            font_info = ImageFont.truetype(font_files[font_style]['regular'], 26)
        else:
            raise OSError
    except:
        # Try Montserrat as fallback
        try:
            font_name = ImageFont.truetype("Montserrat-Bold.ttf", 56)
            font_title = ImageFont.truetype("Montserrat-Regular.ttf", 36)
            font_info = ImageFont.truetype("Montserrat-Regular.ttf", 26)
        except:
            # Fallback to system default
            font_name = ImageFont.load_default()
            font_title = ImageFont.load_default()
            font_info = ImageFont.load_default()

    # Create gradient background
    bg = Image.new('RGB', (card_width, card_height), color=hex_to_rgb(bg_hex))
    card = bg.copy()
    draw = ImageDraw.Draw(card)

    # Apply layout styles
    if layout_style == 'minimal':
        # Minimal style - cleaner, less effects
        show_shadow = False
        show_glass = False
        show_border = True
        show_header = False
    elif layout_style == 'modern':
        # Modern style - more geometric
        show_shadow = True
        show_glass = True
        show_border = True
        show_header = True
    elif layout_style == 'elegant':
        # Elegant style - sophisticated
        show_shadow = True
        show_glass = True
        show_border = True
        show_header = True

    # Drop shadow
    if show_shadow:
        shadow = Image.new('RGBA', (card_width+24, card_height+24), (0,0,0,0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle([(12,12), (card_width+12, card_height+12)], radius=40, fill=(0,0,0,90))
        card_with_shadow = Image.new('RGBA', shadow.size, (0,0,0,0))
        card_with_shadow.paste(shadow, (0,0))
        card_with_shadow.paste(card, (12,12), mask=None)
        card = card_with_shadow.convert('RGB')
        draw = ImageDraw.Draw(card)
        offset_x, offset_y = 12, 12
    else:
        offset_x, offset_y = 0, 0

    # Glassmorphism overlay
    if show_glass:
        overlay = Image.new('RGBA', (card_width, card_height), (255,255,255,40))
        card.paste(overlay, (offset_x, offset_y), overlay)

    # Header bar and border padding
    bar_pad = 22
    header_height = 54
    if show_header:
        draw.rectangle(
            [
                (offset_x+bar_pad, offset_y+bar_pad),
                (card_width+offset_x-bar_pad, offset_y+bar_pad+header_height)
            ],
            fill=accent
        )
        use_logo = (header_logo_option == 'custom' and logo_path) or (logo_file and logo_file.filename)
        if use_logo and logo_path:
            try:
                logo_img = Image.open(logo_path).convert('RGBA')
                logo_max_height = header_height - 10
                logo_max_width = 60
                logo_img.thumbnail((logo_max_width, logo_max_height), Image.Resampling.LANCZOS)
                logo_x = card_width + offset_x - bar_pad - 10 - logo_img.width
                logo_y = offset_y + bar_pad + (header_height - logo_img.height) // 2
                card.paste(logo_img, (logo_x, logo_y), logo_img)
            except Exception as e:
                draw.text((card_width+offset_x-bar_pad-70, offset_y+bar_pad+8), "ZC", font=font_name, fill=text_color)
        else:
            draw.text((card_width+offset_x-bar_pad-70, offset_y+bar_pad+8), "ZC", font=font_name, fill=text_color)
        content_start_y = offset_y + header_height + bar_pad + 10
    else:
        content_start_y = offset_y + 30

    # Draw border only below the header bar
    if show_border:
        border_top = offset_y + bar_pad + header_height + 8
        try:
            draw.rounded_rectangle(
                [
                    (offset_x+10, border_top),
                    (card_width+offset_x-10, card_height+offset_y-10)
                ],
                radius=18,
                outline=accent, width=4
            )
        except AttributeError:
            draw.rectangle(
                [
                    (offset_x+10, border_top),
                    (card_width+offset_x-10, card_height+offset_y-10)
                ],
                outline=accent, width=4
            )

    # Name and profession
    draw.text((offset_x+60, content_start_y), name.upper(), font=font_name, fill=text_color)
    draw.text((offset_x+60, content_start_y+60), profession, font=font_title, fill=text_color)
    draw.line([(offset_x+60, content_start_y+105), (card_width+offset_x-60, content_start_y+105)], fill=divider_color, width=1)

    # Contact info
    info_y = content_start_y + 130
    info_gap = 44
    draw.text((offset_x+60, info_y), "Email:", font=font_info, fill=text_color)
    draw.text((offset_x+188, info_y), email, font=font_info, fill=text_color)
    draw.text((offset_x+60, info_y+info_gap), "Phone:", font=font_info, fill=text_color)
    draw.text((offset_x+188, info_y+info_gap), phone, font=font_info, fill=text_color)
    draw.text((offset_x+60, info_y+2*info_gap), "Address:", font=font_info, fill=text_color)
    draw.text((offset_x+188, info_y+2*info_gap), address, font=font_info, fill=text_color)

    # LinkedIn label and QR code
    if show_qr:
        qr_x = card_width+offset_x-qr_size-60
        qr_y = card_height+offset_y-qr_size-60
        # Use boldest font, but smaller size
        try:
            label_font = ImageFont.truetype(font_files.get(font_style, font_files['montserrat'])['bold'], 18)
        except:
            label_font = ImageFont.load_default()
        label_text = "LinkedIn"
        label_bbox = draw.textbbox((0, 0), label_text, font=label_font)
        label_width = label_bbox[2] - label_bbox[0]
        label_height = label_bbox[3] - label_bbox[1]
        label_x = qr_x + (qr_size - label_width) // 2
        label_y = qr_y - label_height - 8
        draw.text((label_x, label_y), label_text, font=label_font, fill="#000000")
        
        qr = qrcode.QRCode(box_size=3, border=1)
        qr.add_data(linkedin)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color=qr_color, back_color=qr_bg_color)
        if not isinstance(qr_img, Image.Image):
            qr_img = qr_img.get_image()
        qr_img = qr_img.convert('RGB')
        qr_img = qr_img.resize((qr_size, qr_size))
        card.paste(qr_img, (qr_x, qr_y))

    # Save image
    if not os.path.exists("static"):
        os.makedirs("static")
    card.save("static/card.png")

    # --- Generate back of card with vCard QR code and enhanced design ---
    # Gradient background
    back = Image.new('RGB', (card_width, card_height), color=hex_to_rgb(bg_hex))
    for y in range(card_height):
        ratio = y / card_height
        r1, g1, b1 = hex_to_rgb(bg_hex)
        r2, g2, b2 = (255,255,255)
        r = int(r1 * (1-ratio) + r2 * ratio)
        g = int(g1 * (1-ratio) + g2 * ratio)
        b = int(b1 * (1-ratio) + b2 * ratio)
        for x in range(card_width):
            back.putpixel((x, y), (r, g, b))
    back_draw = ImageDraw.Draw(back)
    # Header bar (same as front)
    if show_header:
        back_draw.rectangle(
            [
                (offset_x+bar_pad, offset_y+bar_pad),
                (card_width+offset_x-bar_pad, offset_y+bar_pad+header_height)
            ],
            fill=accent
        )
        logo_pad = bar_pad + 18
        if use_logo and logo_path:
            try:
                logo_img = Image.open(logo_path).convert('RGBA')
                logo_max_height = header_height - 10
                logo_max_width = 60
                logo_img.thumbnail((logo_max_width, logo_max_height), Image.Resampling.LANCZOS)
                logo_x = card_width + offset_x - logo_pad - logo_img.width
                logo_y = offset_y + bar_pad + (header_height - logo_img.height) // 2
                back.paste(logo_img, (logo_x, logo_y), logo_img)
            except Exception as e:
                back_draw.text((card_width+offset_x-logo_pad-70, offset_y+bar_pad+8), "ZC", font=font_name, fill=text_color)
        else:
            back_draw.text((card_width+offset_x-logo_pad-70, offset_y+bar_pad+8), "ZC", font=font_name, fill=text_color)
    # Border (start further below header, more padding)
    border_pad = 30
    border_top = offset_y + bar_pad + header_height + border_pad
    border_left = offset_x + border_pad
    border_right = card_width + offset_x - border_pad
    border_bottom = card_height + offset_y - border_pad
    if show_border:
        try:
            back_draw.rounded_rectangle(
                [
                    (border_left, border_top),
                    (border_right, border_bottom)
                ],
                radius=24,
                outline=accent, width=4
            )
        except AttributeError:
            back_draw.rectangle(
                [
                    (border_left, border_top),
                    (border_right, border_bottom)
                ],
                outline=accent, width=4
            )
    # --- Improved vertical spacing for QR, logo, label, tagline ---
    vcard = f"""BEGIN:VCARD\nVERSION:3.0\nN:{name};;;;\nFN:{name}\nTITLE:{profession}\nEMAIL:{email}\nTEL:{phone}\nADR;TYPE=work:;;{address};;;;\nEND:VCARD"""
    vcard_qr = qrcode.QRCode(box_size=3, border=2)
    vcard_qr.add_data(vcard)
    vcard_qr.make(fit=True)
    vcard_img = vcard_qr.make_image(fill_color="black", back_color="white")
    if not isinstance(vcard_img, Image.Image):
        vcard_img = vcard_img.get_image()
    vcard_img = vcard_img.convert('RGB')
    qr_w, qr_h = vcard_img.size
    # Layout constants
    vertical_margin = 10
    logo_to_qr_gap = 18
    qr_to_label_gap = 22
    label_to_tagline_gap = 36
    # Calculate available content area (inside border)
    content_top = border_top + vertical_margin
    content_bottom = border_bottom - vertical_margin
    content_height = content_bottom - content_top
    # Logo above QR (centered, well below header)
    logo_above_qr_y = content_top
    # QR code position
    qr_y = logo_above_qr_y + 60 + logo_to_qr_gap
    qr_x = (card_width - qr_w) // 2
    # Label position
    label_text = "Scan to save contact"
    try:
        label_font = ImageFont.truetype(font_files.get(font_style, font_files['montserrat'])['bold'], 22)
    except:
        label_font = ImageFont.load_default()
    label_bbox = back_draw.textbbox((0, 0), label_text, font=label_font)
    label_width = label_bbox[2] - label_bbox[0]
    label_x = (card_width - label_width) // 2
    label_y = qr_y + qr_h + qr_to_label_gap
    # Tagline position
    tagline = "Zness Card | Digital Identity"
    try:
        tagline_font = ImageFont.truetype(font_files.get(font_style, font_files['montserrat'])['regular'], 18)
    except:
        tagline_font = ImageFont.load_default()
    tagline_bbox = back_draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    tagline_x = (card_width - tagline_width) // 2
    tagline_y = label_y + label_to_tagline_gap
    # Draw white rounded rectangle with shadow behind QR (inside border)
    rect_pad = 18
    rect_x0 = qr_x - rect_pad
    rect_y0 = qr_y - rect_pad
    rect_x1 = qr_x + qr_w + rect_pad
    rect_y1 = qr_y + qr_h + rect_pad
    shadow_offset = 7
    back_draw.rounded_rectangle(
        [(rect_x0+shadow_offset, rect_y0+shadow_offset), (rect_x1+shadow_offset, rect_y1+shadow_offset)],
        radius=20, fill="#00000033"
    )
    back_draw.rounded_rectangle(
        [(rect_x0, rect_y0), (rect_x1, rect_y1)],
        radius=20, fill="#FFFFFF"
    )
    # Logo above QR (centered)
    if use_logo and logo_path:
        try:
            logo_img2 = Image.open(logo_path).convert('RGBA')
            logo_img2.thumbnail((60, 60), Image.Resampling.LANCZOS)
            logo_above_qr_x = (card_width - logo_img2.width) // 2
            back.paste(logo_img2, (logo_above_qr_x, logo_above_qr_y), logo_img2)
        except Exception as e:
            back_draw.text((card_width//2-30, logo_above_qr_y+10), "ZC", font=font_name, fill=accent)
    else:
        back_draw.text((card_width//2-30, logo_above_qr_y+10), "ZC", font=font_name, fill=accent)
    # Paste QR
    back.paste(vcard_img, (qr_x, qr_y))
    # Add label under QR
    back_draw.text((label_x, label_y), label_text, font=label_font, fill=accent)
    # Tagline at bottom
    back_draw.text((tagline_x, tagline_y), tagline, font=tagline_font, fill="#444444")
    back.save('static/card_back.png')

    return render_template("cards.html", name=name)

if __name__ == '_main_':
    app.run(debug=True)