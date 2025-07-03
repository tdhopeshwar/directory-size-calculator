# ------------------ CLASS DEFINITIONS ------------------

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size  # in KB

    def __repr__(self):
        return f"📄 {self.name} - {self.size}KB"


class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.subdirectories = {}
        self.parent = None
        self.cached_size = None  # cache the total size

    def add_file(self, file):
        self.files.append(file)
        self.invalidate_cache()

    def add_subdirectory(self, directory):
        self.subdirectories[directory.name] = directory
        directory.parent = self
        self.invalidate_cache()

    def invalidate_cache(self):
        self.cached_size = None
        if self.parent:
            self.parent.invalidate_cache()

    def get_size(self):
        if self.cached_size is not None:
            return self.cached_size  #  use cached value if available

        total = sum(file.size for file in self.files)
        for subdir in self.subdirectories.values():
            total += subdir.get_size()

        self.cached_size = total  #  store result in cache
        return total

    def list_contents(self):
        print(f"\n📁 Listing contents of '{self.name}':")
        for file in self.files:
            print(f"   📄 {file.name} - {file.size}KB")
        for subdir_name in self.subdirectories:
            print(f"   📁 {subdir_name}/")
        print()



# ------------------  DIRECTORY STRUCTURE ------------------

# Create root directory
root = Directory("root")

# Create resumes folder
resumes = Directory("resumes")
root.add_subdirectory(resumes)

# Add files to resumes
resumes.add_file(File("Tanisha_Resume_Jan.pdf", 250))
resumes.add_file(File("Tanisha_Resume_June.pdf", 275))

# Add nested folder inside resumes
old_versions = Directory("old_versions")
resumes.add_subdirectory(old_versions)

# Add file in nested folder
old_versions.add_file(File("Tanisha_Resume_2024.pdf", 180))

# Create another folder
projects = Directory("projects")
root.add_subdirectory(projects)

projects.add_file(File("capgemini_assignment.txt", 100))
projects.add_file(File("python_project.zip", 450))


# ------------------ COMMAND LOOP ------------------

if __name__ == "__main__":
    print("📂 Welcome to the Directory Size Calculator!")
    print("Type 'help' to see the list of commands.\n")

    current_dir = root

    def change_directory(current, folder_name):
        if folder_name == "..":
            return current.parent if current.parent else current
        elif folder_name in current.subdirectories:
            return current.subdirectories[folder_name]
        else:
            print("❌ Directory not found.")
            return current

    while True:
        cmd = input(f"[{current_dir.name}] >> ").strip()

        if cmd == "ls":
            current_dir.list_contents()
        elif cmd.startswith("cd "):
            folder = cmd[3:]
            current_dir = change_directory(current_dir, folder)
        elif cmd == "cd ..":
            current_dir = change_directory(current_dir, "..")
        elif cmd.startswith("size"):
            parts = cmd.split()
            if len(parts) == 1:
                print(f"📏 Total size of '{current_dir.name}' and subfolders: {current_dir.get_size()} KB\n")
            else:
                target_name = parts[1]
                if target_name in current_dir.subdirectories:
                    folder = current_dir.subdirectories[target_name]
                    print(f"📏 Total size of '{folder.name}' and subfolders: {folder.get_size()} KB\n")
                else:
                    print(f"❌ Folder '{target_name}' not found in current directory.\n")
        elif cmd == "help":
            print("""
Available commands:
  ls           - List files and folders
  cd <name>    - Change to subdirectory
  cd ..        - Go to parent directory
  size         - Show total size of current directory
  size <dir>   - Show total size of a subfolder
  help         - Show this help message
  exit         - Exit the program
""")
        elif cmd == "exit":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❓ Unknown command. Type 'help' to see available options.")
