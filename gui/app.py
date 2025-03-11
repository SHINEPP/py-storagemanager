import os
import threading
import tkinter
from tkinter import ttk, filedialog, messagebox

from adb import Adb
from utils import resize_image

SDCARD_PATH = '/sdcard'


class ApplicationUI:

    def __init__(self):
        self.window = tkinter.Tk()
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.width = round(self.screen_width * 0.4)
        self.height = round(self.screen_height * 0.6)
        self.last_save_dir = ''
        self.adb = Adb()
        self._load_icons()
        self._setup_window()
        self._setup_menu()
        self._setup_content()

    def _load_icons(self):
        self.folder_icon = resize_image(path=r'img/folder.png', width=16, height=16)
        self.file_icon = resize_image(path=r'img/file.png', width=16, height=16)

    def _setup_window(self):
        self.window.title('手机文件管理')
        x = int((self.screen_width - self.width) / 2)
        y = int((self.screen_height - self.height) / 2)
        self.window.geometry('%sx%s+%s+%s' % (self.width, self.height, x, y))

    def _setup_menu(self):
        self.menu = tkinter.Menu(self.window)
        self.window.config(menu=self.menu)

        about = tkinter.Menu(self.menu, tearoff=0)
        about.add_command(label='版本: V1.0')
        about.add_command(label='作者: zhouzhenliang')
        self.menu.add_cascade(label='关于', menu=about)

    def _setup_content(self):
        paned_window = tkinter.PanedWindow(self.window, showhandle=False, orient=tkinter.HORIZONTAL)
        paned_window.pack(expand=1, fill=tkinter.BOTH)

        self.left_frame = tkinter.Frame(paned_window)
        paned_window.add(self.left_frame)

        # tree view
        columns = ('Date', 'Size')
        self.tree = ttk.Treeview(self.left_frame, columns=columns, selectmode='extended', show='tree headings')
        self.tree.column('#0', minwidth=200, anchor=tkinter.W)
        self.tree.column('#1', width=60, anchor=tkinter.W)
        self.tree.column('#2', width=20, anchor=tkinter.E)
        self.tree.heading('#0', text='Name', anchor=tkinter.W)
        self.tree.heading('#1', text='Date', anchor=tkinter.W)
        self.tree.heading('#2', text='Size', anchor=tkinter.W)

        style = ttk.Style(self.window)
        style.configure('Treeview', rowheight=24)

        # 监听展开或关闭事件
        self.tree.bind('<<TreeviewOpen>>', self.on_tree_view_opened)
        self.tree.bind('<<TreeviewClose>>', self.on_tree_view_closed)
        self.tree.bind('<Button-2>', self.on_tree_view_selection)

        path = SDCARD_PATH
        self.insert_tree_view('', path, is_open=True)
        self.tree.pack(expand=1, fill=tkinter.BOTH)

        # 多线程加载
        t = threading.Thread(target=self.load_tree_view, args=(path,))
        t.start()

    def load_tree_view(self, path: str):
        isdir = self.adb.isdir(path)
        if not isdir:
            return

        new_paths = []
        for name in self.adb.listdir(path):
            new_path = os.path.join(path, name)
            self.insert_tree_view(path, new_path)
            new_paths.append(new_path)

        for new_path in new_paths:
            if not self.adb.isdir(new_path):
                continue
            for name2 in self.adb.listdir(new_path):
                new_path2 = os.path.join(new_path, name2)
                self.insert_tree_view(new_path, new_path2)

    def insert_tree_view(self, parent: str, path: str, is_open: bool = False):
        if self.tree.exists(path):
            return
        _, name = os.path.split(path)
        isdir = self.adb.isdir(path)
        if isdir:
            icon = self.folder_icon
        else:
            icon = self.file_icon
        date_tex = ''  # datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M')
        size_text = ''  # byte2string(os.path.getsize(path))
        values = (date_tex, size_text)
        self.tree.insert(parent, tkinter.END, iid=path, text=f'  {name}', image=icon, open=is_open, values=values)

    def on_tree_view_opened(self, _):
        tree_view = self.tree.selection()
        print(f'on_tree_view_opened(), tree_view = {tree_view}')
        path = tree_view[0]
        t = threading.Thread(target=self.load_tree_view, args=(path,))
        t.start()

    def on_tree_view_closed(self, _):
        tree_view = self.tree.selection()
        print(f'on_tree_view_closed(), tree_view = {tree_view}')

    def on_tree_view_selection(self, _):
        print(f'on_tree_view_selection()')
        tree_view = self.tree.selection()
        print(f'on_tree_view_selection(), tree_view = {tree_view}')
        if len(tree_view) == 0:
            messagebox.showinfo("提示", "未选择任何文件")
            return
        save_path = self.choice_save_dir()
        if len(save_path) == 0:
            return

        items = []
        for path in tree_view:
            lines = self.adb.pull(path, save_path)
            for line in lines:
                items.append(line)
        messagebox.showinfo("提示", '\r\n'.join(items))

    def choice_save_dir(self) -> str:
        path = filedialog.askdirectory(title=u'选择保存目录', initialdir=self.last_save_dir)
        if len(path) > 0:
            self.last_save_dir = path
        return path

    def show(self):
        self.window.mainloop()


if __name__ == '__main__':
    app = ApplicationUI()
    app.show()
