#!/usr/bin/env python3
"""
Generate TTS audio + VTT subtitle (with timestamps) for 5hows chapters.
Uses edge-tts --write-subtitles to get accurate per-sentence timestamps.

Usage:
  python3 generate_audio.py <input.md> <output.mp3> [voice]

Output:
  <output.mp3>   — audio file
  <output.vtt>   — WebVTT subtitle with timestamps (for reading highlight)
  <output.txt>   — clean speech text (for review)
"""

import asyncio
import re
import sys
import os
import subprocess
import tempfile
import edge_tts


def md_to_speech_text(md_content: str) -> str:
    """Convert markdown to clean speech text, preserving paragraph structure."""
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

    # Handle headings - keep text, add sentence break
    md_content = re.sub(r'^#{1,6}\s+(.+)$', r'\1。', md_content, flags=re.MULTILINE)

    # Handle bold/italic
    md_content = re.sub(r'\*\*([^*]+)\*\*', r'\1', md_content)
    md_content = re.sub(r'\*([^*]+)\*', r'\1', md_content)
    md_content = re.sub(r'==([^=]+)==', r'\1', md_content)

    # Handle horizontal rules
    md_content = re.sub(r'^---$', '。', md_content, flags=re.MULTILINE)

    # Handle blockquotes
    md_content = re.sub(r'^>\s*', '', md_content, flags=re.MULTILINE)

    # Handle list items
    md_content = re.sub(r'^[-*]\s+', '', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^\d+\.\s+', '', md_content, flags=re.MULTILINE)

    # Handle numbered sub-items like a. b. c.
    md_content = re.sub(r'^([a-z])\.\s+', r'\1，', md_content, flags=re.MULTILINE)

    # Math/special symbols
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

    # Remove formatting artifacts
    md_content = re.sub(r'^\s*[○■●]\s*', '', md_content, flags=re.MULTILINE)

    # Remove table of contents section
    md_content = re.sub(r'目录.*?(?=\n\s*\n)', '', md_content, flags=re.DOTALL)

    md_content = md_content.strip()
    return md_content


def srt_to_ms(ts: str) -> int:
    """Convert SRT timestamp (HH:MM:SS,mmm) to milliseconds."""
    ts = ts.strip().replace(',', '.')
    parts = ts.split(':')
    h, m = int(parts[0]), int(parts[1])
    s_parts = parts[2].split('.')
    s, ms = int(s_parts[0]), int(s_parts[1]) if len(s_parts) > 1 else 0
    return (h * 3600 + m * 60 + s) * 1000 + ms


def ms_to_vtt_ts(ms: int) -> str:
    """Convert milliseconds to WebVTT timestamp (HH:MM:SS.mmm)."""
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def srt_to_vtt(srt_content: str) -> str:
    """Convert SRT subtitle content to WebVTT format."""
    lines = srt_content.strip().split('\n')
    vtt_lines = ['WEBVTT', '']
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Skip sequence numbers
        if re.match(r'^\d+$', line):
            i += 1
            continue
        # Timestamp line
        if '-->' in line:
            vtt_lines.append(line.replace(',', '.'))
            i += 1
            continue
        vtt_lines.append(line)
        i += 1
    return '\n'.join(vtt_lines)


async def generate_chunk(text: str, mp3_path: str, vtt_path: str, voice: str):
    """Generate a single chunk with both mp3 and subtitles (SRT→VTT)."""
    communicate = edge_tts.Communicate(text, voice=voice, rate='+0%')
    sub_maker = edge_tts.SubMaker()

    with open(mp3_path, 'wb') as audio_file:
        async for chunk in communicate.stream():
            if chunk['type'] == 'audio':
                audio_file.write(chunk['data'])
            elif chunk['type'] in ('WordBoundary', 'SentenceBoundary'):
                sub_maker.feed(chunk)

    # get_srt() returns SRT format, convert to VTT
    srt_content = sub_maker.get_srt()
    vtt_content = srt_to_vtt(srt_content)
    with open(vtt_path, 'w', encoding='utf-8') as vtt_file:
        vtt_file.write(vtt_content)


def merge_vtt_files(vtt_files: list, mp3_files: list, out_vtt: str):
    """Merge multiple VTT files, adjusting timestamps based on cumulative audio duration."""
    # Get duration of each mp3 chunk
    durations = []
    for mp3 in mp3_files:
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=noprint_wrappers=1:nokey=1', mp3],
                capture_output=True, text=True
            )
            dur = float(result.stdout.strip())
        except Exception:
            # Fallback: estimate from file size (edge-tts produces ~32kbps MP3)
            size = os.path.getsize(mp3)
            dur = size * 8 / 32000
        durations.append(dur)

    def parse_vtt_ts(ts: str) -> int:
        """Convert VTT timestamp HH:MM:SS.mmm to milliseconds."""
        parts = ts.strip().split(':')
        if len(parts) == 3:
            h, m, s = parts
        else:
            h = '0'
            m, s = parts
        sec, ms_str = s.split('.')
        return (int(h) * 3600 + int(m) * 60 + int(sec)) * 1000 + int(ms_str[:3].ljust(3, '0'))

    all_cues = []
    offset_ms = 0
    for i, vtt_path in enumerate(vtt_files):
        with open(vtt_path, encoding='utf-8') as f:
            content = f.read()
        cue_pattern = re.compile(
            r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})\s*\n(.*?)(?=\n\n|\Z)',
            re.DOTALL
        )
        for m in cue_pattern.finditer(content):
            start_ms = parse_vtt_ts(m.group(1)) + offset_ms
            end_ms = parse_vtt_ts(m.group(2)) + offset_ms
            text = m.group(3).strip()
            all_cues.append((start_ms, end_ms, text))
        offset_ms += int(durations[i] * 1000)

    with open(out_vtt, 'w', encoding='utf-8') as f:
        f.write('WEBVTT\n\n')
        for idx, (start, end, text) in enumerate(all_cues):
            f.write(f"{idx + 1}\n{ms_to_vtt_ts(start)} --> {ms_to_vtt_ts(end)}\n{text}\n\n")


async def generate_audio_with_vtt(text: str, output_mp3: str, output_vtt: str, voice: str):
    """Generate audio and VTT, splitting into chunks if needed."""
    CHUNK_SIZE = 4500

    if len(text) <= CHUNK_SIZE:
        print(f"  Generating single chunk ({len(text)} chars)...")
        await generate_chunk(text, output_mp3, output_vtt, voice)
    else:
        # Split into paragraph-based chunks
        paragraphs = text.split('\n\n')
        chunks = []
        current = ''
        for para in paragraphs:
            if len(current) + len(para) + 2 > CHUNK_SIZE and current:
                chunks.append(current.strip())
                current = para
            else:
                current += ('\n\n' + para if current else para)
        if current.strip():
            chunks.append(current.strip())

        print(f"  Split into {len(chunks)} chunks")

        tmp_dir = tempfile.mkdtemp()
        chunk_mp3s = []
        chunk_vtts = []

        for i, chunk in enumerate(chunks):
            cmp3 = os.path.join(tmp_dir, f'chunk{i}.mp3')
            cvtt = os.path.join(tmp_dir, f'chunk{i}.vtt')
            print(f"  Chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...")
            await generate_chunk(chunk, cmp3, cvtt, voice)
            chunk_mp3s.append(cmp3)
            chunk_vtts.append(cvtt)

        # Merge mp3 files
        list_path = os.path.join(tmp_dir, 'list.txt')
        with open(list_path, 'w') as f:
            for p in chunk_mp3s:
                f.write(f"file '{os.path.abspath(p)}'\n")

        result = subprocess.run(
            ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_path, '-c', 'copy', output_mp3],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            # Naive concatenation fallback
            print("  ffmpeg failed, using naive MP3 concatenation")
            with open(output_mp3, 'wb') as out:
                for p in chunk_mp3s:
                    with open(p, 'rb') as inp:
                        out.write(inp.read())

        # Merge VTT files with offset timestamps
        merge_vtt_files(chunk_vtts, chunk_mp3s, output_vtt)

        # Cleanup
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)

    size = os.path.getsize(output_mp3)
    print(f"  Audio: {output_mp3} ({size/1024/1024:.1f} MB)")
    if os.path.exists(output_vtt):
        vtt_size = os.path.getsize(output_vtt)
        print(f"  VTT:   {output_vtt} ({vtt_size/1024:.0f} KB)")
    else:
        print("  WARNING: VTT file not created!")


async def main():
    if len(sys.argv) < 3:
        print("Usage: python3 generate_audio.py <input.md> <output.mp3> [voice]")
        print("Voices: zh-CN-YunxiNeural (male), zh-CN-XiaoxiaoNeural (female)")
        sys.exit(1)

    input_path = sys.argv[1]
    output_mp3 = sys.argv[2]
    output_vtt = output_mp3.replace('.mp3', '.vtt')
    output_txt = output_mp3.replace('.mp3', '.txt')
    voice = sys.argv[3] if len(sys.argv) > 3 else 'zh-CN-YunxiNeural'

    print(f"Reading: {input_path}")
    with open(input_path, encoding='utf-8') as f:
        md = f.read()

    speech_text = md_to_speech_text(md)
    chars = len(speech_text)
    print(f"Text: {chars} characters (~{chars/3.5/60:.0f} min)")

    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(speech_text)
    print(f"Text saved: {output_txt}")

    await generate_audio_with_vtt(speech_text, output_mp3, output_vtt, voice)
    print("Done!")


if __name__ == '__main__':
    asyncio.run(main())
