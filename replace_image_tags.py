#!/usr/bin/env python3
import os
import re

def replace_image_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 Image 标签，支持 src 属性使用引号或大括号的形式
    image_pattern = re.compile(r'''
        <Image\b
        (?:
            [\s\S]*?
            src=(?:['"])?({?[^'"}\s>]+}?)(?:['"])?
            [\s\S]*?
        )
        />
    ''', re.VERBOSE)

    def replacement(match):
        # 从匹配到的整个 Image 标签中提取 src 和 alt 属性
        tag_content = match.group(0)
        src = match.group(1).strip()

        # 提取 alt 属性
        alt_match = re.search(r'alt=(?:[\'"{])?([^\'"}\s>]*)(?:[\'"})]?)', tag_content)
        alt = alt_match.group(1).strip() if alt_match else ''

        # 移除 src 和 alt 可能包含的大括号
        path = src.strip('{}')
        alt = alt.strip('{}')

        if alt:
            return f'{{{{ image(path="{path}", alt="{alt}") }}}}'
        else:
            return f'{{{{ image(path="{path}") }}}}'

    new_content = image_pattern.sub(replacement, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully replaced Image tags in: {file_path}")
    else:
        print(f"No Image tags found in: {file_path}")

def main():
    posts_dir = '/home/xfy/Developer/blog/content/posts'

    for filename in os.listdir(posts_dir):
        if filename.endswith('.mdx') or filename.endswith('.md'):
            file_path = os.path.join(posts_dir, filename)
            replace_image_tags(file_path)

if __name__ == "__main__":
    main()
