import tkinter as tk
import cv2
global showScreen
import client
from CONSTANTS import MAIN, YYPORT, ZZPORT, XXPORT, MEETING, AAPORT
from PIL import Image, ImageTk  # 图像控件
import ctrl

def welcome():
    client = init_connection()
    roott = tk.Toplevel()
    # ctrl.root.withdraw()
    # roott = tk.Toplevel()

    roott.geometry("800x500")
    photo = tk.PhotoImage(file="pics/bg2(1).png")
    bg_label = tk.Label(roott, image=photo, justify=tk.LEFT, compound=tk.CENTER)
    create_bt = tk.Button(roott, text="Create\n a\n meeting",
                          activebackground='pink', activeforeground='black', fg='white', bg='red',
                          font=('Helvetica', '10'),
                          width=20, height=5, padx=10, pady=3, relief='raised', anchor='center',
                          command=lambda: create(client))
    join_bt = tk.Button(roott, text="Join\n a\n meeting",
                        activebackground='pink', activeforeground='black', fg='white', bg='seagreen',
                        font=('Helvetica', '10'),
                        width=20, height=5, padx=10, pady=3, relief='raised', anchor='center',
                        command=lambda: join(client, roott))
    create_bt.pack()
    create_bt.place(x=310, y=140)
    join_bt.pack()
    join_bt.place(x=310, y=280)
    bg_label.pack()
    bg_label.place(x=0, y=0)
    roott.mainloop()

def create(client):
    meeting_id = client.create_meeting()
    hint = tk.Toplevel()
    hint.geometry("300x190")
    photo = tk.PhotoImage(file="pics/hint.png")
    bg_label = tk.Label(hint, image=photo, justify=tk.LEFT, compound=tk.CENTER)
    text_id = ("The meeting id is \n" + str(meeting_id))
    label = tk.Label(hint, bg='#feffff', fg='black', text=text_id, font=('Times New Roman', 20))
    label.pack()
    label.place(x=55, y=55)
    check = tk.Button(hint, bg='seagreen', text='confirm', command=lambda: hint.destroy())
    check.place(x=120, y=140)
    bg_label.pack()
    bg_label.place(x=0, y=0)
    hint.mainloop()

def join(client, root):
    root.destroy()
    hint = tk.Toplevel()
    hint.geometry("300x190")
    photo = tk.PhotoImage(file="pics/hint.png")
    bg_label = tk.Label(hint, image=photo, justify=tk.LEFT, compound=tk.CENTER)
    text_id = "Please input the meeting id:"
    label = tk.Label(hint, bg='#feffff', fg='black', text=text_id, font=('Times New Roman', 15))
    label.pack()
    label.place(x=55, y=45)
    var = tk.StringVar()
    E1 = tk.Entry(hint, bd=5, show=None, textvariable=var, )
    E1.pack()
    E1.place(x=80, y=95)
    check = tk.Button(hint, bg='seagreen', text='confirm', command=lambda: join_mt(client, E1.get(), hint))
    check.place(x=120, y=140)
    bg_label.pack()
    bg_label.place(x=0, y=0)
    hint.mainloop()

def init_connection():
    import client
    # ip = '10.24.184.6'
    # ip = '127.0.0.1'
    # ip = '192.168.46.24'
    # ip = '10.24.253.245'
    # ip = '192.168.96.61'
    # ip = '10.15.178.231'
    ip = '10.24.81.213'
    address = {
        'xx': (ip, XXPORT),
        'yy': (ip, YYPORT),
        'zz': (ip, ZZPORT),
        'aa': (ip, AAPORT),
    }
    client = client.Client(address)
    return client

def meeting(client):
    global showScreen
    root = tk.Toplevel()
    root.geometry("947x137")
    showScreen = tk.Toplevel(root)
    photo = tk.PhotoImage(file="pics/bg3.png")
    bg_label = tk.Label(root, image=photo, justify=tk.LEFT, compound=tk.CENTER)
    share_sc = tk.Button(root, text="Share screen", fg='white', bg='pink',
                         width=15, height=4, padx=10, pady=2, relief='raised', anchor='center',
                         command=lambda: func_share_screen(share_sc, client))
    ctrl_sc = tk.Button(root, text="Control other's screen", fg='white', bg='pink',
                        width=15, height=4, padx=10, pady=2, relief='raised', anchor='center',
                        command=lambda: func_ctrl_screen(ctrl_sc, client))
    ctrl_msc = tk.Button(root, text="Control my screen", fg='white', bg='pink',
                         width=15, height=4, padx=10, pady=2, relief='raised', anchor='center',
                         command=lambda: func_control_my(ctrl_msc, client))
    share_vd = tk.Button(root, text="Share video", fg='white', bg='pink',
                         width=15, height=4, padx=10, pady=2, relief='raised', anchor='center',
                         command=lambda: func_share_vd(share_vd, client))
    share_ad = tk.Button(root, text="Share audio", fg='white', bg='pink',
                         width=15, height=4, padx=10, pady=2, relief='raised', anchor='center',
                         command=lambda: func_share_ad(share_ad, client))
    leave = tk.Button(root, text="Leave a meeting", fg='white', bg='lightblue',
                      width=15, height=4, padx=10, pady=2, relief='raised', anchor='center',
                      command=lambda: func_leaving_mt(root, leave, client))
    close = tk.Button(root, text="Close a meeting", fg='white', bg='lightblue',
                      width=15, height=4, padx=10, pady=2, relief='raised', anchor='center',
                      command=lambda: func_close_mt(close, client, root))
    share_sc.pack()
    ctrl_sc.pack()
    ctrl_msc.pack()
    share_vd.pack()
    share_ad.pack()
    leave.pack()
    close.pack()
    share_sc.place(x=20, y=20)
    ctrl_sc.place(x=150, y=20)
    ctrl_msc.place(x=280, y=20)
    share_vd.place(x=410, y=20)
    share_ad.place(x=540, y=20)
    leave.place(x=670, y=20)
    close.place(x=800, y=20)
    bg_label.pack()
    bg_label.place(x=0, y=0)

    mb = tk.Menubutton(root, text="show members", relief="raised", bg='seagreen')
    filemenu = tk.Menu(mb, tearoff=False)
    filemenu.add_command(label="show", command=lambda:func_show_members(filemenu, mb, client))
    filemenu.add_separator()
    mb.config(menu=filemenu)
    mb.pack()
    mb.place(x=0, y=110)

    root.mainloop()

def join_mt(client, sid, hint):
    # hint.destroy()
    ok = client.join_meeting(sid)
    if not ok:
        hint = tk.Toplevel()
        hint.geometry("300x190")
        photo = tk.PhotoImage(file="pics/hint.png")
        bg_label = tk.Label(hint, image=photo, justify=tk.LEFT, compound=tk.CENTER)
        text_id = ("Wrong meeting id!!")
        label = tk.Label(hint, bg='#feffff', fg='black', text=text_id, font=('Times New Roman', 20))
        label.pack()
        label.place(x=55, y=55)
        check = tk.Button(hint, bg='seagreen', text='confirm', command=lambda: hint.destroy())
        check.place(x=120, y=140)
        bg_label.pack()
        bg_label.place(x=0, y=0)
        hint.mainloop()
    else:
        meeting(client)

def func_share_vd(share_vd, client):
    if share_vd['background'] =='pink':
        share_vd.config(bg = 'red')
    elif share_vd['background'] =='red':
        share_vd.config(bg = 'pink')
    top = tk.Toplevel()
    top.title('ME')
    top.geometry('600x400')
    image_width = 600
    image_height = 400
    canvas = tk.Canvas(top, bg="white", width=image_width, height=image_height)  # 绘制画布
    canvas.place(x=0, y=0)
    client.share_video()
    while client.video_sockets.cap.isOpened():
        pic = tkImage(client)
        canvas.create_image(0, 0, anchor='nw', image=pic)
        top.update()
        top.after(1)
    top.destroy()

    # cv2_to_tk(client, root, v1, v2)

def tkImage(client):
    cap = client.video_sockets.cap
    ref, frame = cap.read()
    frame = cv2.flip(frame, 1)  # 摄像头翻转
    cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    pilImage = Image.fromarray(cvimage)
    pilImage = pilImage.resize((600, 400), Image.ANTIALIAS)
    tkImage = ImageTk.PhotoImage(image=pilImage)
    return tkImage

def func_share_ad(share_ad, client):
    if share_ad['background'] =='pink':
        share_ad.config(bg = 'red')
    elif share_ad['background'] =='red':
        share_ad.config(bg = 'pink')
    client.share_audio()

def func_leaving_mt(root, leave, client):
    root.destroy()
    if leave['background'] =='lightblue':
        leave.config(bg = 'red')
    elif leave['background'] =='red':
        leave.config(bg = 'lightblue')
    client.leaving_meeting()

def func_share_screen(share_sc, client):
    if share_sc['background'] == 'pink':
        share_sc.config(bg ='red')
    elif share_sc['background'] =='red':
        share_sc.config(bg = 'pink')
    client.share_screen()

def func_ctrl_screen(ctrl_sc, client):
    if ctrl_sc['background'] =='pink':
        ctrl_sc.config(bg = 'red')
    elif ctrl_sc['background'] =='red':
        ctrl_sc.config(bg = 'pink')
    request_ctrlsc(client)

def request_ctrlsc(client):
    hint = tk.Toplevel()
    hint.geometry("300x190")
    photo = tk.PhotoImage(file="pics/hint.png")
    bg_label = tk.Label(hint, image=photo, justify=tk.LEFT, compound=tk.CENTER)
    text_id = "Please input the control ip: "
    label = tk.Label(hint, bg='#feffff', fg='black', text=text_id, font=('Times New Roman', 15))
    label.pack()
    label.place(x=55, y=45)
    var = tk.StringVar()
    E1 = tk.Entry(hint, bd=5, show=None, textvariable=var, )
    E1.pack()
    E1.place(x=80, y=95)
    # TODO:
    check = tk.Button(hint, bg='seagreen', text='confirm', command=lambda: confirm_request(client, E1.get()))
    check.place(x=120, y=140)
    bg_label.pack()
    bg_label.place(x=0, y=0)
    hint.mainloop()

def confirm_request(client, ip):
    print(ip)
    client.msg_sockets.send_msg('ip' + ip)
    # wait = tk.Toplevel()
    # wait.geometry("300x190")
    # photo = tk.PhotoImage(file="pics/hint.png")
    # bg_label = tk.Label(wait, image=photo, justify=tk.LEFT, compound=tk.CENTER)
    # text_id = "Waiting for \nbecontroller's reply..."
    # label = tk.Label(wait, bg='#feffff', fg='black', text=text_id, font=('Times New Roman', 15))
    # label.pack()
    # label.place(x=55, y=45)
    # check = tk.Button(wait, bg='seagreen', text='confirm', command=lambda: client.control_others())
    # check.place(x=120, y=140)
    # bg_label.pack()
    # bg_label.place(x=0, y=0)
    # wait.mainloop()
    client.control_others()

def func_show_members(filemenu, mb, client):
    hint = tk.Toplevel()
    hint.geometry("300x190")
    hint.configure(bg='seagreen')
    member_list = client.show_members()
    members = member_list.split(',')
    label = {}
    for i in members:
        label[i] = tk.Label(hint, bg='seagreen', fg='white', text=i, font=('Times New Roman', 15))
        # print(label.get(i))
        label.get(i).pack()
    check = tk.Button(hint, bg='seagreen', fg ='white', text='confirm', command=lambda: hint.destroy())
    check.place(x=120, y=140)
    hint.mainloop()

def func_control_my(button, client):
    if button['background'] =='pink':
        button.config(bg = "red")
    elif button['background'] =='red':
        button.config(bg = 'pink')
    hint = tk.Toplevel()
    hint.geometry("300x190")
    photo = tk.PhotoImage(file="pics/hint.png")
    bg_label = tk.Label(hint, image=photo, justify=tk.LEFT, compound=tk.CENTER)
    text_id = "Accept? (yes or no)"
    label = tk.Label(hint, bg='#feffff', fg='black', text=text_id, font=('Times New Roman', 15))
    label.pack()
    label.place(x=63, y=45)
    var = tk.StringVar()
    E1 = tk.Entry(hint, bd=5, show=None, textvariable=var, )
    E1.pack()
    E1.place(x=80, y=95)
    check = tk.Button(hint, bg='seagreen', text='confirm', command=lambda:temp_ctrl_my(client, E1.get()))
    check.place(x=120, y=140)
    bg_label.pack()
    bg_label.place(x=0, y=0)
    hint.mainloop()

def temp_ctrl_my(client, str):
    client.msg_sockets.send_accept(str)
    # wait = tk.Toplevel()
    # wait.geometry("300x190")
    # photo = tk.PhotoImage(file="pics/hint.png")
    # bg_label = tk.Label(wait, image=photo, justify=tk.LEFT, compound=tk.CENTER)
    # text_id = "Waiting for \ncontroller's reply..."
    # label = tk.Label(wait, bg='#feffff', fg='black', text=text_id, font=('Times New Roman', 15))
    # label.pack()
    # label.place(x=55, y=45)
    # check = tk.Button(wait, bg='seagreen', text='confirm', command=lambda:client.control_my())
    # check.place(x=120, y=140)
    # bg_label.pack()
    # bg_label.place(x=0, y=0)
    # wait.mainloop()
    client.control_my()

def func_close_mt(button, client, root):
    root.destroy()
    if button['background'] =='lightblue':
        button.config(bg = "red")
    elif button['background'] =='red':
        button.config(bg = 'lightblue')
    client.closing_meeting()

if __name__ == "__main__":
    welcome()
