from tkinter import StringVar
from tkinter.ttk import *
from ttkthemes import ThemedTk
import time
import os
from PIL import Image, ImageTk
from tkinter.filedialog import SaveAs
from getpass import getuser
from os.path import join

home = '/home/' + getuser()
localp = join(home, '.local', 'share')

root = ThemedTk(theme='arc')

root.geometry('463x500')
root.resizable(False,False)
root.title('Сканнер нахуй')

f = Frame(width=100)
f.grid(row=1,column=0,sticky='n, e, s, w')
try:
	ff = ImageTk.PhotoImage(Image.open(localp + 'scanthumb.png').resize((363,500),Image.ANTIALIAS))
except:
	os.system('scanimage >~/.local/share/scanthumb.png --format=png --speed=yes')
	ff = ImageTk.PhotoImage(Image.open(localp + 'scanthumb.png').resize((363,500),Image.ANTIALIAS))
img = Label(image=ff)
img.image=ff
img.grid(row=1,column=1)

def upd(self, who):
	who['text'] = round(self['value'])
def preview(imgd, buttons):
	buttons[2]['state'] = 'disabled'
	buttons[3]['state'] = 'disabled'
	os.system('scanimage >~/.local/share/scanthumb.png --format=png --speed=yes')
	ff = ImageTk.PhotoImage(Image.open(localp + 'scanthumb.png').resize((363,500),Image.ANTIALIAS))
	imgd.destroy()
	img = Label(image=ff, width=50)
	img.image=ff
	img.grid(row=1,column=1)
	buttons[2]['state'] = 'normal'
	buttons[3]['state'] = 'normal'
def scan(args):
	args[2]['state'] = 'disabled'
	args[3]['state'] = 'disabled'
	lb = Label(f, text='Working...')
	lb.pack(side='bottom')
	if args[1] == 0: args[1] = 75
	root.after(2, time.sleep(0.1))
	resultpath = SaveAs(defaultextension='.'+args[0], initialfile='scan', filetypes=['PNG picture {.png}', 'JPEG picture {.jpg}'], title='Путь сканирования').show()
	lb['text'] = 'Working...'
	if not resultpath:
		lb['text'] = 'Done'
		args[2]['state'] = 'normal'
		args[3]['state'] = 'normal'
		root.after(3000, lb.destroy)
		return
	
	os.system('scanimage >"{}" --resolution {}dpi --format={}'.format(resultpath, args[1], args[0]))
	lb['text'] = 'Done'
	args[2]['state'] = 'normal'
	args[3]['state'] = 'normal'
	root.after(3000, lb.destroy)

l = Label(f,text='75')
dpi = Scale(f, from_=75, to=600)
lisd_arg = StringVar()
lisd = Combobox(f, values=('png', 'jpg'), textvariable=lisd_arg)
get = Button(f, text='Сканировать')
pre = Button(f, text='Предпросмотр')


dpi['command'] = lambda x: upd(dpi, l)
get['command'] = lambda: scan([lisd_arg.get(), round(dpi['value']), get, pre])
pre['command'] = lambda: root.after(0,preview(img, ['', '', pre, get]))



get.pack()
pre.pack()
dpi.pack()
l.pack()
lisd.pack()




root.mainloop()
