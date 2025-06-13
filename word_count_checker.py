import re

# Read the LaTeX file
with open('latex/report.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove comments
content = re.sub(r'%.*', '', content)

# Remove LaTeX commands and environments that don't count towards word count
# Title page metadata
content = re.sub(r'\\university\{[^}]*\}', '', content)
content = re.sub(r'\\department\{[^}]*\}', '', content)
content = re.sub(r'\\course\{[^}]*\}', '', content)
content = re.sub(r'\\title\{[^}]*\}', '', content)
content = re.sub(r'\\author\{[^}]*\}', '', content)
content = re.sub(r'\\email\{[^}]*\}', '', content)
content = re.sub(r'\\githubusername\{[^}]*\}', '', content)
content = re.sub(r'\\supervisors\{[^}]*\}', '', content)
content = re.sub(r'\\repository\{[^}]*\}', '', content)

# Remove document structure commands
content = re.sub(r'\\documentclass.*', '', content)
content = re.sub(r'\\usepackage.*', '', content)
content = re.sub(r'\\graphicspath.*', '', content)
content = re.sub(r'\\begin\{document\}', '', content)
content = re.sub(r'\\end\{document\}', '', content)
content = re.sub(r'\\maketitlepage', '', content)

# Remove section titles (they don't count)
content = re.sub(r'\\section\*?\{[^}]*\}', '', content)
content = re.sub(r'\\subsection\*?\{[^}]*\}', '', content)

# Remove figure environments and captions
content = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', content, flags=re.DOTALL)

# Remove equations
content = re.sub(r'\\begin\{equation\}.*?\\end\{equation\}', '', content, flags=re.DOTALL)

# Remove bibliography commands
content = re.sub(r'\\bibliographystyle.*', '', content)
content = re.sub(r'\\bibliography.*', '', content)

# Remove other LaTeX commands but keep their content where appropriate
content = re.sub(r'\\textbf\{([^}]*)\}', r'\1', content)
content = re.sub(r'\\cite\{[^}]*\}', '', content)  # Citations don't count
content = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', content)  # Keep content of most commands
content = re.sub(r'\\[a-zA-Z]+', '', content)  # Remove remaining commands

# Remove extra whitespace and count words
content = re.sub(r'\s+', ' ', content).strip()
words = content.split()
word_count = len([word for word in words if word.strip()])

print(f'Estimated word count (excluding non-counting elements): {word_count}')

# Also count figures
with open('latex/report.tex', 'r', encoding='utf-8') as f:
    original_content = f.read()

figure_count = len(re.findall(r'\\begin\{figure\}', original_content))
print(f'Figure count: {figure_count}')

# Check if within limits
if word_count <= 1500:
    print(f'✅ Word count is within limit (≤1500)')
else:
    print(f'❌ Word count exceeds limit by {word_count - 1500} words')

if figure_count <= 5:
    print(f'✅ Figure count is within limit (≤5)')
else:
    print(f'❌ Figure count exceeds limit by {figure_count - 5} figures') 