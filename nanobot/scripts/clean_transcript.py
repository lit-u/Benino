import re
import sys

def parse_time(time_str):
    # 00:00:00,160
    h, m, s = time_str.replace(',', '.').split(':')
    return float(h) * 3600 + float(m) * 60 + float(s)

def clean_srt(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.strip().split('\n\n')
    
    unique_lines = []
    
    for block in blocks:
        lines = block.split('\n')
        if len(lines) < 3:
            continue
            
        # Parse timestamp
        # 00:00:00,160 --> 00:00:02,629
        time_line = lines[1]
        try:
            start_str, end_str = time_line.split(' --> ')
            start = parse_time(start_str)
            end = parse_time(end_str)
            duration = end - start
        except:
            continue

        if duration < 0.2: # Ignore very short artifacts
            continue
            
        text = " ".join(lines[2:])
        text = text.replace('\n', ' ').strip()
        
        if not text:
            continue
            
        unique_lines.append(text)

    # Smart Deduplication
    # YouTube auto-captions often do:
    # A
    # A B
    # A B C
    # B C D
    # ...
    # We want to reconstruct the stream.
    
    # Simple algorithm:
    # If line starts with previous line, replace previous.
    # If line is contained in previous, skip (unless it adds something? rarely).
    # This is tricky with rolling window captions.
    
    # Better: Longest Common Subsequence or just string overlap.
    # Given the sample:
    # 1. "Last week, Anthropic released an 80page"
    # 3. "Last week, Anthropic released an 80page document that talks about Aristotle."
    # 5. "document that talks about Aristotle. Now, why are they quoting Aristotle? Why"
    
    # 1 is prefix of 3. Keep 3.
    # 3 contains "document that talks about Aristotle."
    # 5 starts with "document that talks about Aristotle."
    
    # Algorithm:
    # processed_text = ""
    # current_line = line[i]
    # overlap = find_overlap(processed_text, current_line)
    # append current_line[overlap:]
    
    final_text = ""
    
    for line in unique_lines:
        # Clean up tags like <c> if any (not in this SRT but possible)
        line = re.sub(r'<[^>]+>', '', line)
        
        if not final_text:
            final_text = line
            continue
            
        # Check for overlap with the end of final_text
        # We check trailing N chars of final_text vs leading N chars of line
        
        # Optimization: Check only last 50 chars
        search_window = final_text[-100:] if len(final_text) > 100 else final_text
        
        overlap_len = 0
        # Brute force overlap check (simple logic)
        for i in range(len(search_window)):
            suffix = search_window[i:]
            if line.startswith(suffix):
                overlap_len = len(suffix)
                break
        
        to_append = line[overlap_len:]
        if to_append:
            # Add a space if needed
            if final_text and not final_text.endswith(' ') and not to_append.startswith(' '):
                 if not to_append.startswith(',') and not to_append.startswith('.'):
                     final_text += " "
            final_text += to_append
            
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_text)

if __name__ == "__main__":
    clean_srt(r"d:\_PAL\benino\workspace\oldboy\temp\transcript_raw_4.en.srt", r"d:\_PAL\benino\workspace\oldboy\temp\clean_transcript_4.txt")
