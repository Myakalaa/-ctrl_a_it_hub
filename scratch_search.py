content = open(r'C:\Users\amyak\Desktop\CTRL A IT HUB\static\css\main.css', 'r', encoding='utf-8').read()
for line_idx, line in enumerate(content.splitlines()):
    if '.course-card' in line:
        print(f'{line_idx+1}: {line.strip()}')
