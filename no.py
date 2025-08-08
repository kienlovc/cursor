import os
import shutil
import subprocess
import re
import tempfile
from colorama import Fore, Style, init

# Khởi tạo colorama
init()

# Emoji hiển thị
EMOJI = {
    "PROCESS": "🔄",
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "FOLDER": "📁",
    "FILE": "📄",
    "STOP": "🛑",
    "CHECK": "✔️"
}

class WindowsAutoUpdateDisabler:
    def __init__(self):
        local_app = os.getenv("LOCALAPPDATA", "")
        self.updater_path = os.path.join(local_app, "cursor-updater")
        self.update_yml_path = os.path.join(local_app, "Programs", "Cursor", "resources", "app", "update.yml")
        self.product_json_path = os.path.join(local_app, "Programs", "Cursor", "resources", "app", "product.json")

    def kill_processes(self):
        """Tắt tiến trình Cursor"""
        print(f"{Fore.CYAN}{EMOJI['PROCESS']} Đang dừng tiến trình Cursor...{Style.RESET_ALL}")
        subprocess.run(['taskkill', '/F', '/IM', 'Cursor.exe', '/T'], capture_output=True)
        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Đã dừng Cursor{Style.RESET_ALL}")
        return True

    def remove_updater_directory(self):
        """Xóa thư mục updater"""
        if os.path.exists(self.updater_path):
            try:
                if os.path.isdir(self.updater_path):
                    shutil.rmtree(self.updater_path)
                else:
                    os.remove(self.updater_path)
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Đã xóa updater{Style.RESET_ALL}")
            except PermissionError:
                print(f"{Fore.YELLOW}{EMOJI['INFO']} Không thể xóa updater (bị khóa), bỏ qua{Style.RESET_ALL}")
        return True

    def clear_update_yml(self):
        """Xóa nội dung update.yml"""
        if os.path.exists(self.update_yml_path):
            try:
                with open(self.update_yml_path, 'w') as f:
                    f.write('')
                os.system(f'attrib +r "{self.update_yml_path}"')  # khóa file
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} update.yml đã được xóa & khóa{Style.RESET_ALL}")
            except PermissionError:
                print(f"{Fore.YELLOW}{EMOJI['INFO']} update.yml bị khóa, bỏ qua{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}{EMOJI['INFO']} Không tìm thấy update.yml{Style.RESET_ALL}")
        return True

    def create_block_file(self):
        """Tạo file giả updater để chặn"""
        try:
            os.makedirs(os.path.dirname(self.updater_path), exist_ok=True)
            open(self.updater_path, 'w').close()
            os.system(f'attrib +r "{self.updater_path}"')  # khóa file
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Đã tạo file chặn updater{Style.RESET_ALL}")
        except PermissionError:
            print(f"{Fore.YELLOW}{EMOJI['INFO']} File updater bị khóa, bỏ qua{Style.RESET_ALL}")
        return True

    def remove_update_url(self):
        """Xóa URL update trong product.json"""
        if not os.path.exists(self.product_json_path):
            print(f"{Fore.YELLOW}{EMOJI['INFO']} Không tìm thấy product.json{Style.RESET_ALL}")
            return True
        
        try:
            with open(self.product_json_path, "r", encoding="utf-8") as f:
                content = f.read()

            patterns = [
                r"https://api2.cursor.sh/aiserver.v1.AuthService/DownloadUpdate",
                r"https://api2.cursor.sh/updates",
                r"http://cursorapi.com/updates"
            ]
            for p in patterns:
                content = re.sub(p, "", content)

            shutil.copy2(self.product_json_path, self.product_json_path + ".old")
            with open(self.product_json_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            os.system(f'attrib +r "{self.product_json_path}"')  # khóa file
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Đã xóa URL update trong product.json{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Lỗi sửa product.json: {e}{Style.RESET_ALL}")
            return False

    def disable_auto_update(self):
        print(f"{Fore.CYAN}{EMOJI['STOP']} Bắt đầu chặn cập nhật tự động Cursor (Windows){Style.RESET_ALL}")
        self.kill_processes()
        self.remove_updater_directory()
        self.clear_update_yml()
        self.create_block_file()
        self.remove_update_url()
        print(f"{Fore.GREEN}{EMOJI['CHECK']} Hoàn tất! Auto-update đã bị vô hiệu hóa{Style.RESET_ALL}")

if __name__ == "__main__":
    tool = WindowsAutoUpdateDisabler()
    tool.disable_auto_update()
    input(f"{EMOJI['INFO']} Nhấn Enter để thoát...")
