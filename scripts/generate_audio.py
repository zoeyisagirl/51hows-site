#!/usr/bin/env python3
"""Generate TTS audio for 5hows chapters using edge-tts."""

import asyncio
import re
import sys
import os
import edge_tts

def md_to_speech_text(md_content: str) -> str:
    """Convert markdown to clean speech text."""
    # Remove frontmatter
    if md_content.startswith('---'):
        parts = md_content.split('---', 2)
        md_content = parts[2] if len(parts) > 2 else md_content

    # Remove image syntax
    md_content = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', md_content)
    
    # Remove links but keep text
    md_content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', md_content)
    
    # Remove HTML tags but keep inner text
    md_content = re.sub(r'<span[^>]*>', '', md_content)
    md_content = re.sub(r'</span>', '', md_content)
    md_content = re.sub(r'<br\s*/?>', '，', md_content)
    md_content = re.sub(r'<[^>]+>', '', md_content)
    
    # Handle headings - add a pause
    md_content = re.sub(r'^#{1,6}\s+(.+)$', r'\1。', md_content, flags=re.MULTILINE)
    
    # Handle bold/italic
    md_content = re.sub(r'\*\*([^*]+)\*\*', r'\1', md_content)
    md_content = re.sub(r'\*([^*]+)\*', r'\1', md_content)
    md_content = re.sub(r'==([^=]+)==', r'\1', md_content)
    
    # Handle horizontal rules - add pause
    md_content = re.sub(r'^---$', '。', md_content, flags=re.MULTILINE)
    
    # Handle blockquotes - just keep text
    md_content = re.sub(r'^>\s*', '', md_content, flags=re.MULTILINE)
    
    # Handle list items
    md_content = re.sub(r'^[-*]\s+', '', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^\d+\.\s+', '', md_content, flags=re.MULTILINE)
    
    # Handle numbered sub-items like a. b. c.
    md_content = re.sub(r'^([a-z])\.\s+', r'\1，', md_content, flags=re.MULTILINE)
    
    # Clean up special characters that TTS might stumble on
    md_content = md_content.replace('e⁻¹', 'e的负一次方')
    md_content = md_content.replace('e⁻⁴', 'e的负四次方')
    md_content = md_content.replace('(1-e⁻⁴)', '(1减e的负四次方)')
    md_content = md_content.replace('→', '到')
    md_content = md_content.replace('≥', '大于等于')
    md_content = md_content.replace('≤', '小于等于')
    md_content = md_content.replace('≠', '不等于')
    md_content = md_content.replace('≈', '约等于')
    md_content = md_content.replace('∞', '无穷')
    
    # Remove excessive whitespace
    md_content = re.sub(r'\n{3,}', '\n\n', md_content)
    
    # Remove lines that are just formatting artifacts
    md_content = re.sub(r'^\s*○\s*', '', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^\s*■\s*', '', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^\s*●\s*', '', md_content, flags=re.MULTILINE)
    
    # Remove the table of contents section (it's not useful in audio)
    # Find "目录" section and remove until next real heading
    md_content = re.sub(r'目录.*?(?=\n\s*\n)', '', md_content, flags=re.DOTALL)
    
    md_content = md_content.strip()
    return md_content


async def generate_audio(text: str, output_path: str, voice: str = 'zh-CN-YunxiNeural'):
    """Generate audio file from text using edge-tts."""
    # edge-tts has a limit per request, split if needed
    # Max is roughly 5000 characters per chunk
    CHUNK_SIZE = 4500
    
    if len(text) <= CHUNK_SIZE:
        communicate = edge_tts.Communicate(text, voice=voice, rate='+0%')
        await communicate.save(output_path)
    else:
        # Split into chunks and concatenate
        chunks = []
        paragraphs = text.split('\n\n')
        current_chunk = ''
        
        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 > CHUNK_SIZE and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = para
            else:
                current_chunk += '\n\n' + para if current_chunk else para
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        print(f"  Split into {len(chunks)} chunks")
        
        # Generate each chunk
        chunk_files = []
        for i, chunk in enumerate(chunks):
            chunk_path = output_path.replace('.mp3', f'_chunk{i}.mp3')
            print(f"  Generating chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...")
            communicate = edge_tts.Communicate(chunk, voice=voice, rate='+0%')
            await communicate.save(chunk_path)
            chunk_files.append(chunk_path)
        
        # Concatenate using ffmpeg if available, otherwise just use first chunk approach
        if len(chunk_files) == 1:
            os.rename(chunk_files[0], output_path)
        else:
            # Create file list for ffmpeg
            list_path = output_path.replace('.mp3', '_list.txt')
            chunk_dir = os.path.dirname(os.path.abspath(output_path))
            with open(list_path, 'w') as f:
                for cf in chunk_files:
                    # Use absolute paths in the list
                    abs_path = os.path.abspath(cf)
                    f.write(f"file '{abs_path}'\n")
            
            # Try ffmpeg
            import subprocess
            try:
                result = subprocess.run(
                    ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_path, '-c', 'copy', output_path],
                    capture_output=True, text=True
                )
                if result.returncode != 0:
                    raise Exception(result.stderr)
                # Clean up chunks
                for cf in chunk_files:
                    os.remove(cf)
                os.remove(list_path)
            except FileNotFoundError:
                # No ffmpeg, just concatenate mp3 files naively
                print("  Warning: ffmpeg not found, concatenating naively")
                with open(output_path, 'wb') as out:
                    for cf in chunk_files:
                        with open(cf, 'rb') as inp:
                            out.write(inp.read())
                        os.remove(cf)
                try:
                    os.remove(list_path)
                except:
                    pass
    
    file_size = os.path.getsize(output_path)
    print(f"  Audio saved: {output_path} ({file_size/1024/1024:.1f} MB)")


async def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_audio.py <input_md> <output_mp3> [voice]")
        print("Available voices: zh-CN-YunxiNeural (male), zh-CN-XiaoxiaoNeural (female)")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    voice = sys.argv[3] if len(sys.argv) > 3 else 'zh-CN-YunxiNeural'
    
    print(f"Reading: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to speech text
    speech_text = md_to_speech_text(md_content)
    
    chars = len(speech_text)
    est_minutes = chars / 4 / 60
    print(f"Text: {chars} characters, estimated ~{est_minutes:.0f} minutes of audio")
    
    # Save clean text for review
    text_output = output_path.replace('.mp3', '.txt')
    with open(text_output, 'w', encoding='utf-8') as f:
        f.write(speech_text)
    print(f"Clean text saved: {text_output}")
    
    # Generate audio
    await generate_audio(speech_text, output_path, voice)
    print("Done!")


if __name__ == '__main__':
    asyncio.run(main())
