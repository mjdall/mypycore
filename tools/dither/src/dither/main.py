import argparse
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from PIL import Image
import numpy as np
import tempfile
import subprocess
import os

console = Console()

def dither_image(image, num_colors, dither_strength):
    # Convert image to RGB mode
    image = image.convert("RGB")
    
    # Quantize the image with dithering
    image_dithered = image.quantize(colors=num_colors, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    
    # Convert back to RGB
    image_dithered = image_dithered.convert("RGB")
    
    # Apply additional dithering effect
    img_array = np.array(image_dithered)
    noise = np.random.randint(0, 256, img_array.shape, dtype=np.uint8) * (dither_strength / 100)
    img_array = np.clip(img_array.astype(np.int16) + noise - 128, 0, 255).astype(np.uint8)
    
    return Image.fromarray(img_array)

def process_video(input_path, output_path, num_colors, dither_strength):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract frames
        subprocess.run(["ffmpeg", "-i", input_path, f"{temp_dir}/frame_%04d.png"])
        
        # Process frames
        frames = sorted(os.listdir(temp_dir))
        for frame in console.track(frames, description="Processing frames"):
            img = Image.open(os.path.join(temp_dir, frame))
            dithered = dither_image(img, num_colors, dither_strength)
            dithered.save(os.path.join(temp_dir, frame))
        
        # Combine frames back into video
        subprocess.run(["ffmpeg", "-i", f"{temp_dir}/frame_%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", output_path])

def display_image(image):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        image.save(temp_file.name)
        console.print(f"[bold green]Displaying processed image:[/bold green]")
        console.print(f"file://{temp_file.name}")

def main():
    parser = argparse.ArgumentParser(description="Apply dither effects to images and videos")
    parser.add_argument("input_path", help="Path to the input image or video file")
    parser.add_argument("--colors", type=int, default=8, help="Number of colors to use in the dithered image")
    parser.add_argument("--strength", type=int, default=50, help="Dither strength (0-100)")
    parser.add_argument("--output", help="Path to save the output file")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    args = parser.parse_args()

    console.print(f"[bold]Processing: {args.input_path}[/bold]")
    
    # Determine if input is image or video
    is_video = args.input_path.lower().endswith((".mp4", ".gif"))
    
    if is_video:
        img = Image.open(args.input_path)
        img.thumbnail((80, 80))  # Resize for preview
    else:
        img = Image.open(args.input_path)
    
    num_colors = args.colors
    dither_strength = args.strength
    
    if args.interactive:
        while True:
            if is_video:
                console.print("[bold yellow]Video preview (first frame):[/bold yellow]")
            processed = dither_image(img, num_colors, dither_strength)
            display_image(processed)
            
            command = Prompt.ask("[bold cyan]Enter command[/bold cyan] (adjust_colors, adjust_dither, save, quit)")
            
            if command == "adjust_colors":
                num_colors = IntPrompt.ask("Enter number of colors", default=num_colors)
            elif command == "adjust_dither":
                dither_strength = IntPrompt.ask("Enter dither strength (0-100)", default=dither_strength)
            elif command == "save":
                output_path = Prompt.ask("Enter output path", default=args.output or f"output{os.path.splitext(args.input_path)[1]}")
                save_output(args.input_path, output_path, is_video, num_colors, dither_strength, processed)
                break
            elif command == "quit":
                break
            else:
                console.print("[bold red]Invalid command. Try again.[/bold red]")
    else:
        output_path = args.output or f"output{os.path.splitext(args.input_path)[1]}"
        processed = dither_image(img, num_colors, dither_strength)
        save_output(args.input_path, output_path, is_video, num_colors, dither_strength, processed)

def save_output(input_path, output_path, is_video, num_colors, dither_strength, processed_image):
    if is_video:
        console.print("[bold green]Processing video... This may take a while.[/bold green]")
        process_video(input_path, output_path, num_colors, dither_strength)
    else:
        processed_image.save(output_path)
    console.print(f"[bold green]Saved to: {output_path}[/bold green]")

if __name__ == "__main__":
    main()