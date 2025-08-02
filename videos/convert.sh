#!/bin/bash

# Initialize counter
count=1

# Output directory (recommended to keep converted files separate)
output_dir="converted_videos_no_audio" # Changed output directory name for clarity
mkdir -p "$output_dir"

# Define accepted video extensions
video_extensions=("mp4" "avi" "mov" "mkv" "webm" "flv" "wmv")

echo "Starting video conversion (no audio) and deletion process..."
echo "Converted files will be saved to: $output_dir"
echo "Original files will be deleted AFTER successful conversion."
echo "Press Ctrl+C to stop at any time. BE CAREFUL!"
echo ""

# Loop through all files in the current directory
for f in *; do
    # Skip if it's the script itself or a directory
    if [[ "$f" == "$(basename "$0")" ]] || [[ -d "$f" ]]; then
        continue
    fi

    # Get the file extension in lowercase
    extension="${f##*.}"
    extension_lower=$(echo "$extension" | tr '[:upper:]' '[:lower:]')

    # Check if the extension is in our list of video extensions
    is_video=false
    for ext in "${video_extensions[@]}"; do
        if [[ "$extension_lower" == "$ext" ]]; then
            is_video=true
            break
        fi
    done

    if [[ "$is_video" == true ]]; then
        formatted_count=$(printf "%03d" "$count")
        output_name="${output_dir}/video${formatted_count}.mp4"

        echo "---"
        echo "Converting '$f' to '$output_name' (removing audio)..."

        # Perform the conversion with -an to remove audio
        # The '&&' ensures that 'rm' only runs if ffmpeg exits successfully (return code 0)
        ffmpeg -i "$f" -crf 18 -an "$output_name" && \
        echo "Conversion successful for '$f'. Deleting original..." && \
        rm "$f" && \
        echo "Original '$f' deleted." || \
        echo "Error converting or deleting '$f'. Original file NOT deleted."

        ((count++))
    else
        echo "Skipping non-video file: '$f'"
    fi
done

echo "---"
echo "Conversion (no audio) and deletion process complete!"