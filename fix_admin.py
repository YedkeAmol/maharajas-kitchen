import re

with open('templates/admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    'bg-surface-900': 'bg-white',
    'bg-surface-800': 'bg-gray-50',
    'border-surface-700': 'border-gray-200',
    'hover:bg-surface-700': 'hover:bg-gray-100',
    'text-gray-100': 'text-text',
    'text-gray-300': 'text-text',
    'text-gray-400': 'text-muted',
    'text-brand-500': 'text-primary',
    'bg-brand-500': 'bg-primary',
    'border-brand-500': 'border-primary',
    'text-brand-400': 'text-primary',
    'hover:bg-brand-600': 'hover:bg-[#c94d0a]',
    'text-surface-900': 'text-white'
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed admin.html")
