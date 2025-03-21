from PIL import Image, ImageDraw

def create_icon():
    # Create a 256x256 image with a transparent background
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a modern, minimalist icon
    # Background circle
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=(41, 128, 185, 255))  # Blue color
    
    # Code brackets
    bracket_width = 40
    bracket_height = 120
    x = size//2
    y = size//2
    
    # Left bracket
    draw.rectangle([x-bracket_width//2, y-bracket_height//2,
                   x-bracket_width//4, y+bracket_height//2],
                  fill=(255, 255, 255, 255))
    
    # Right bracket
    draw.rectangle([x+bracket_width//4, y-bracket_height//2,
                   x+bracket_width//2, y+bracket_height//2],
                  fill=(255, 255, 255, 255))
    
    # Save the icon
    image.save('app_icon.ico', format='ICO')
    print("Icon created successfully!")

if __name__ == "__main__":
    create_icon() 