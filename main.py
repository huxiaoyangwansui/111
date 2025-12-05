import tkinter as tk
from PIL import Image, ImageTk
import sys
import os

def resource_path(relative_path):
    """获取文件的绝对路径，支持PyInstaller打包"""
    try:
        # PyInstaller创建临时文件夹的路径
        base_path = sys._MEIPASS
    except Exception:
        # 正常运行时的路径
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class FullscreenImageApp:
    def __init__(self, root, image_path):
        self.root = root
        self.image_path = image_path
        
        # 配置窗口属性
        self.setup_window()
        
        # 加载并显示图片
        self.load_image()
        
        # 绑定事件
        self.bind_events()
    
    def setup_window(self):
        # 置顶显示
        self.root.attributes('-topmost', True)
        
        # 去掉窗口边框和标题栏
        self.root.overrideredirect(True)
        
        # 获取屏幕尺寸并设置为全屏
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        # 设置窗口背景色为黑色
        self.root.configure(bg='black')
    
    def load_image(self):
        # 加载图片
        self.original_image = Image.open(self.image_path)
        
        # 创建标签用于显示图片
        self.image_label = tk.Label(self.root, bg='black')
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # 调整图片大小并显示
        self.resize_image()
    
    def resize_image(self):
        # 获取当前窗口尺寸
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # 调整图片大小以适应窗口，保持比例
        resized_image = self.original_image.resize(
            (window_width, window_height), 
            Image.LANCZOS
        )
        
        # 创建ImageTk对象
        self.tk_image = ImageTk.PhotoImage(resized_image)
        
        # 更新标签图片
        self.image_label.config(image=self.tk_image)
        self.image_label.image = self.tk_image  # 保持引用，防止被垃圾回收
    
    def bind_events(self):
        # 防止窗口关闭
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # 禁用Alt+F4
        self.root.bind("<Alt-F4>", lambda e: "break")
        
        # 禁用Ctrl+W
        self.root.bind("<Control-w>", lambda e: "break")
        
        # 禁用Esc键
        self.root.bind("<Escape>", lambda e: "break")
        
        # 窗口大小变化时重新调整图片
        self.root.bind("<Configure>", lambda e: self.resize_image())

if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    
    # 获取图片路径
    image_path = resource_path("windows.png")
    
    # 检查图片文件是否存在
    if not os.path.exists(image_path):
        print(f"错误：图片文件 '{image_path}' 不存在！")
        sys.exit(1)
    
    # 创建应用实例
    app = FullscreenImageApp(root, image_path)
    
    # 运行主循环
    root.mainloop()
