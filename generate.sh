#!/bin/bash

# Configuration
VIDEO_DIR="videos"
AUDIO_DIR="audios"
OUTRO_FILE="outro.mp4"
OUTPUT_DIR="outputs"
LOG_FILE="ffmpeg.log"
TARGET_RES="1080:1920"  # Vertical resolution
FADE_DURATION=0.5         # 0.5-second fade duration
HW_ACCEL_DEVICE="/dev/dri/renderD128"  # VAAPI device

# Create directories
mkdir -p "$VIDEO_DIR" "$AUDIO_DIR" "$OUTPUT_DIR"

# Clear previous log file
> "$LOG_FILE"

# Find all media files
video_files=()
while IFS= read -r -d $'\0'; do
    video_files+=("$REPLY")
done < <(find "$VIDEO_DIR" -type f \( -iname "*.mp4" -o -iname "*.mov" -o -iname "*.avi" -o -iname "*.mkv" \) -print0)

audio_files=()
while IFS= read -r -d $'\0'; do
    audio_files+=("$REPLY")
done < <(find "$AUDIO_DIR" -type f \( -iname "*.mp3" -o -iname "*.wav" -o -iname "*.ogg" \) -print0)

# Process all combinations
for video in "${video_files[@]}"; do
    for audio in "${audio_files[@]}"; do
        # Get base names for output file
        video_base=$(basename "${video%.*}")
        audio_base=$(basename "${audio%.*}")
        output_file="$OUTPUT_DIR/'${audio_base}'${video_base}.mp4"
        
        # Skip if already processed
        if [[ -f "$output_file" ]]; then
            echo "Skipping existing: $output_file"
            continue
        fi
        
        echo "Processing: $video_base + $audio_base"
        
        # Get durations
        video_duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$video")
        audio_duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$audio")
        
        # Calculate min duration
        min_duration=$(awk -v vd="$video_duration" -v ad="$audio_duration" \
            'BEGIN {print (vd < ad) ? vd : ad}')
        echo "Using duration: $min_duration seconds"
        
        # Calculate fade start time
        fade_start=$(echo "scale=5; $min_duration - $FADE_DURATION" | bc)
        
        # Hardware-accelerated processing with corrected filter chain
        ffmpeg -y \
            -hwaccel vaapi -hwaccel_device "$HW_ACCEL_DEVICE" -hwaccel_output_format vaapi -i "$video" \
            -i "$audio" \
            -hwaccel vaapi -hwaccel_device "$HW_ACCEL_DEVICE" -hwaccel_output_format vaapi -i "$OUTRO_FILE" \
            -filter_complex \
                "[0:v]trim=0:$min_duration,setpts=PTS-STARTPTS,hwdownload,format=nv12,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=60[mainv];
                 [mainv]fade=t=out:st=$fade_start:d=$FADE_DURATION:color=black[mainv_fade];
                 [1:a]atrim=0:$min_duration,asetpts=PTS-STARTPTS,aresample=44100[maina];
                 [2:v]hwdownload,format=nv12[outrov];
                 [2:a]aresample=44100[outro_a];
                 [mainv_fade][maina][outrov][outro_a]concat=n=2:v=1:a=1[vout_cpu][aout];
                 [vout_cpu]format=nv12,hwupload[outv]" \
            -c:v hevc_vaapi \
            -c:a aac -b:a 192k \
            -map "[outv]" \
            -map "[aout]" \
            "$output_file" \
            2>> "$LOG_FILE"
        
        # Check result
        if [[ $? -eq 0 ]]; then
            echo "Created: $output_file"
        else
            echo "Error processing $video_base + $audio_base. Check $LOG_FILE"
        fi
    done
done

# Cleanup
rm -rf "$TEMP_DIR"