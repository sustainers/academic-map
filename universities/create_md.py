import sys
import re

def slugify(s):
    # Convert to lowercase, remove non-alphanumeric characters, and replace spaces with hyphens
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def main():
    if len(sys.argv) < 2:
        print("Error: University name not provided.")
        sys.exit(1)

    university = sys.argv[1]
    slug = slugify(university)

    with open(f"{slug}.md", "w") as file:
        file.write(f"# {university}\n")

if __name__ == "__main__":
    main()

