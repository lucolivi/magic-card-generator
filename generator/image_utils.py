from PIL import Image, ImageDraw, ImageFont

def paste_image(source_image, target_image, x, y, mask):
    target_image = target_image.copy()
    target_image.paste(source_image, (x,y), mask)
    return target_image

def write_text(image, text, font, x, y):
    image = image.copy()
    draw = ImageDraw.Draw(image)
    draw.text((x, y), text, font=font, fill='black')
    return image

def get_text_width(text, font):
    draw = ImageDraw.Draw(Image.new('RGB', (0, 0)))
    return draw.textlength(text, font=font)

def wrap_text(text, font, max_width):
    text_tokens = text.split(" ")

    wrapped_text_lines = [text_tokens[0]]

    for token in text_tokens[1:]:
        line_candidate = wrapped_text_lines[-1] + " " + token

        if get_text_width(line_candidate, font) > max_width:
            wrapped_text_lines.append(token)
        else:
            wrapped_text_lines[-1] = line_candidate

    return wrapped_text_lines

def wrap_multiline_text(text, font, max_width):
    wrapped_text_lines = []

    for t_line in text.split("\n"):
        t_line_wrapped_text = wrap_text(t_line, font, max_width)
        wrapped_text_lines.extend(t_line_wrapped_text)

    return wrapped_text_lines

def write_multiline_text(image, multiline_text, font, x, y):
    image = image.copy()
    draw = ImageDraw.Draw(image)
    draw.multiline_text((x,y), multiline_text, font=font, fill='black', spacing=4)
    return image

def get_multiline_text_height(multiline_text, font):
    draw = ImageDraw.Draw(Image.new('RGB', (0, 0)))
    
    text_bb = draw.multiline_textbbox(
        xy=(0,0), 
        text=multiline_text,
        font=font
    )

    multiline_text_height = text_bb[3] - text_bb[1]

    return multiline_text_height

def get_fitting_text_and_font(text, max_width, max_height, font_file, min_font_size, max_font_size):
    for font_size in range(max_font_size, min_font_size, -1):
        
        font = ImageFont.truetype(font_file, font_size)

        wrapped_text = wrap_multiline_text(text, font, max_width)
        multiline_text = "\n".join(wrapped_text)

        multiline_text_height = get_multiline_text_height(multiline_text, font)

        if multiline_text_height < max_height:
            break
            
    return multiline_text, font

def get_center_y_anchor_offset(height, max_height):
    y_offset = (max_height - height) / 2
    return max(0, y_offset)

def write_text_centered_within_box(image, text, x, y, max_width, max_height, font_file, min_font_size, max_font_size):
    fit_text, fit_font = get_fitting_text_and_font(text, max_width, max_height, font_file, min_font_size, max_font_size)
    text_height = get_multiline_text_height(fit_text, fit_font)
    y_offset = get_center_y_anchor_offset(text_height, max_height)
    return write_multiline_text(image, fit_text, fit_font, x, y + y_offset)

def write_text_centered(image, text, font, x, y, width):
    text_width = get_text_width(text, font)
    
    x_offset = (width - text_width) / 2

    image = write_text(
        image=image, 
        text=text, 
        font=font, 
        x=x + x_offset, y=y
    )

    return image