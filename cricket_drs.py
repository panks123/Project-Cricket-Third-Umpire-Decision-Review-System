import tkinter as tk
import PIL.Image
import PIL.ImageTk
import cv2
from functools import partial
import threading
import imutils
import time

try:
    stream=cv2.VideoCapture("clip_.mp4")
except Exception as e:
    pass

flag=True


def play(speed):
    global flag
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    try:
        grabbed, frame = stream.read()
        frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0, 0, image=frame, anchor=tk.NW)
        if flag:
            canvas.create_text(160,45,fill="red3",font="Times 30 italic bold",text="Decision Pending")
        flag=not flag
    except Exception as e:
        pass


def pending(decision):
    # 1. Display decision pending image
    frame=cv2.cvtColor(cv2.imread("pending.png"),cv2.COLOR_BGR2RGB)
    frame=imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)  # In case the image is not re-sized (650x366)
    frame=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0,0,image=frame,anchor=tk.NW)

    # 2. Wait for 1 second
    time.sleep(2)

    # 3. Display Sponsor Image
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)  # In case the image is not re-sized (650x366)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)

    # 4. Wait for 1.5 second
    time.sleep(1.5)

    # 5. Display out/not out image
    if decision=="out":
        decisionImg="out.png"
    else:
        decisionImg="notout.png"

    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)  # In case the image is not re-sized (650x366)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)
    # 6. Wait for 5 second
    time.sleep(5)

    # Display the home image again
    frame = cv2.cvtColor(cv2.imread("home.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)  # In case the image is not re-sized (650x366)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tk.NW)


def out():
    thread=threading.Thread(target=pending,args=("out",))
    thread.daemon=1
    thread.start()


def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()


# width and height of the main sreen
SET_WIDTH=650
SET_HEIGHT=366

window=tk.Tk()
window.title("Third Umpire Decision Review Kit")
window.wm_iconbitmap("drs.ico")

cv_img=cv2.cvtColor(cv2.imread("home.png"),cv2.COLOR_BGR2RGB)
canvas=tk.Canvas(window,width=SET_WIDTH,height=SET_HEIGHT)
photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas=canvas.create_image(0,0,anchor=tk.NW,image=photo)
canvas.pack()

# Buttons to manage playback()
btn=tk.Button(window,text="Load clip",width=50,bg="cyan",command=partial(play,-100))
btn.pack(pady=3)

btn=tk.Button(window,text="<<<<Previous (fast)",width=50,bg="cyan",command=partial(play,-25))
btn.pack(pady=3)

btn=tk.Button(window,text="<<Previous (slow)",width=50,bg="cyan",command=partial(play,-2))
btn.pack(pady=3)

btn=tk.Button(window,text="Next (fast)>>>>",width=50,bg="cyan",command=partial(play,25))
btn.pack(pady=3)

btn=tk.Button(window,text="Next (slow)>>",width=50,bg="cyan",command=partial(play,2))
btn.pack(pady=3)

btn=tk.Button(window,text="Give Out",width=50,bg="cyan",command=out)
btn.pack(pady=3)

btn=tk.Button(window,text="Give Not Out",width=50,bg="cyan",command=not_out)
btn.pack(pady=3)

statusBar=tk.Label(window,text=u"\u00a9"+"Pankaj Kumar 2020",relief=tk.SUNKEN,anchor=tk.W,bg="cyan",padx=20)
statusBar.pack(side=tk.BOTTOM,fill=tk.X)
window.mainloop()

