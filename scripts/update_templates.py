import os

def update_template_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Replace the old staticfiles tag with static
                updated_content = content.replace('{% load staticfiles %}', '{% load static %}')
                
                # Write the updated content back to the file
                with open(file_path, 'w') as f:
                    f.write(updated_content)
                print(f"Updated {file_path}")

if __name__ == "__main__":
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    update_template_files(templates_dir)
