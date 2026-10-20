from pathlib import Path
from resume_parser import parse_resume

file_path = input("Enter the full path of your resume: ").strip().strip('"')
path = Path(file_path)

if not path.exists():
    print("ERROR: File not found.")
else:
    print("File:", path.name)
    print("Extension:", path.suffix.lower())
    print("Size:", path.stat().st_size, "bytes")

    try:
        text = parse_resume(str(path))
        print("Extracted characters:", len(text))
        print("\nExtracted text preview:\n")
        print(text[:1500])
    except Exception as error:
        print("ERROR TYPE:", type(error).__name__)
        print("ERROR MESSAGE:", error)