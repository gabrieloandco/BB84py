from Tkinter import *

#1
#root = Tkinter.Tk()
#theLabel = Tkinter.Label(root, text="This is too easy")
#theLabel.pack()
#root.mainloop()

#2
#root = Tk()

#topFrame = Frame(root)
#topFrame.pack()
#bottomFrame = Frame(root)
#bottomFrame.pack(side=BTTOM)

#button1 = Button(topFrame, text="Button 1", fg="red")
#button2 = Button(topFrame, text="Button 2", fg="blue")
#button3 = Button(topFrame, text="Button 3", fg="green")
#button4 = Button(bottomFrame, text="Button4", fg="purple")

#button1.pack(side=LEFT)
#button2.pack(side=RIGHT)
#button3.pack(side=RIGHT)
#button4.pack(side=BOTTOM)

#root.mainloop()

#3
#root = Tk()

#one = Label(root, text="One", bg="red",fg="white")
#one.pack()
#two = Label(root, text="Two", bg="green", fg="black")
#two.pack(fill=X)
#three = Label(root, text="Three", bg="blue", fg="white")
#three.pack(side=LEFT,fill=Y)

#root.mainloop()

#4

#root = Tk()

#label_1 = Label(root, text="Name")
#label_2 = Label(root, text="Password")
#entry_1 = Entry(root)
#entry_2 = Entry(root)
#label_1.grid(row=0)
#label_2.grid(row=1)
#entry_1.grid(row=0,column=1)
#entry_2.grid(row=1,column=1)

#root.mainloop()

#5
#root = Tk()

#label_1 = Label(root, text="Name")
#label_2 = Label(root, text="Password")
#entry_1 = Entry(root)
#entry_2 = Entry(root)

#label_1.grid(row=0, sticky=E)
#label_2.grid(row=1, sticky=E)

#entry_1.grid(row=0, column=1)
#entry_2.grid(row=1, column=1)

#c = Checkbutton(root, text= "Keep me logged in")
#c.grid(columnspan=2)

#root.mainloop()

#6
#root = Tk()

#def printName(event):
    #print("Hello Fuckers")

#button_1 = Button(root, text="Print my name")
#button_1.bind("<Button-1>", printName)
#button_1.pack()

#root.mainloop()

#7
#root = Tk()

#def leftClick(event):
#    print("Left")

#def middleClick(event):
#    print("Middle")

#def rightClick(event):
#    print("Right")

#frame = Frame(root, width=300, height=250)
#frame.bind("<Button-1>",leftClick)
#frame.bind("<Button-2>", middleClick)
#frame.bind("<Button-3>", rightClick)
#frame.pack()

#root.mainloop()

#8

#class BuckButtons:
#    def __init__(self,master):
#        frame = Frame(master)
#        frame.pack()
#
#        self.printButton = Button(text="Print Message", command=self.printMessage)
#        self.printButton.pack(side=LEFT)
#        
#        self.quitButton = Button(frame, text="Quit",command=frame.quit)
#        self.quitButton.pack(side=LEFT)
#
#    def printMessage(self):
#        print("Wow this actually worked")
#
#root = Tk()
#b = BuckButtons(root)
#root.mainloop()

#9
#def doNothing():
    #print("ok ok I wont..")

#root = Tk()

#menu = Menu(root)
#root.config(menu=menu)

#subMenu = Menu(menu)
#menu.add_cascade(label="file", menu=subMenu)
#subMenu.add_command(label="New Project..", command=doNothing)
#subMenu.add_command(label="New..", command=doNothing)
#subMenu.add_separator()
#subMenu.add_command(label="Exit", command=doNothing)

#editMenu = Menu(menu)
#menu.add_cascade(label="Edit",menu=editMenu)
#editMenu.add_command(label="Redo", command=doNothing)

#root.mainloop()

#10
#def doNothing(): 
#    print("Ok, ok I won't!") 
#root = Tk() 
##Main menu
#menu = Menu(root, tearoff = False) 
#root.config(menu = menu) 
#subMenu = Menu(menu, tearoff = False) 
#menu.add_cascade(label = "File", menu = subMenu) 
#subMenu.add_command(label = "New project", command = doNothing) 
#subMenu.add_command(label = "New...", command = doNothing) 
#subMenu.add_separator() 
#subMenu.add_command(label = "Exit", command = root.destroy) 
#editMenu = Menu(menu, tearoff = False) 
#menu.add_cascade(label = "Edit", menu = editMenu) 
#editMenu.add_command(label = "Redo", command = doNothing) 
##Toolbar  
#toolbar = Frame(root, bg = "blue") 
#insertButt = Button(toolbar, text = "Insert image", command = doNothing).pack(side = LEFT, padx = 2, pady = 2) 
#printButt = Button(toolbar, text = "Print", command = doNothing).pack(side = LEFT, padx = 2, pady = 2) 
#toolbar.pack(side = TOP, fill = X) 
#root.mainloop()

#11
#def doNothing(): 
#    print("Ok, ok I won't!") 
#root = Tk() 
##Main menu 
#menu = Menu(root, tearoff = False) 
#root.config(menu = menu) 
#subMenu = Menu(menu, tearoff = False) 
#menu.add_cascade(label = "File", menu = subMenu) 
#subMenu.add_command(label = "New project", command = doNothing) 
#subMenu.add_command(label = "New...", command = doNothing) 
#subMenu.add_separator() 
#subMenu.add_command(label = "Exit", command = root.destroy) 
#editMenu = Menu(menu, tearoff = False) 
#menu.add_cascade(label = "Edit", menu = editMenu) 
#editMenu.add_command(label = "Redo", command = doNothing) 
## Toolbar  
#toolbar = Frame(root, bg = "blue") 
#insertButt = Button(toolbar, text = "Insert image", command = doNothing).pack(side = LEFT, padx = 2, pady = 2) 
#printButt = Button(toolbar, text = "Print", command = doNothing).pack(side = LEFT, padx = 2, pady = 2) 
#toolbar.pack(side = TOP, fill = X) 
## Status bar 
#status = Label(root, text = "Preparing to do nothing", bd = 1, relief = SUNKEN, anchor = W).pack(side = BOTTOM, fill = X) 
#root.mainloop()

#12
#import tkinter.messagebox
#root = Tk() 
#messagebox.showinfo("Message box", "Monkeys can live forever.") 
#answer = messagebox.askquestion("Question 1", "Do you like silly faces?") 
#if answer == "yes": 
#    print(" XD ") 
#root.mainloop()

#13
root = Tk() 
canvas = Canvas(root, width = 200, height = 100) 
canvas.pack() 
blackLine = canvas.create_line(0, 0, 200, 50) 
# Give start and end point 
redLine = canvas.create_line(0, 100, 200, 50, fill = "red") 
greenBox = canvas.create_rectangle(5, 5, 50, 50, fill = "green")
canvas.delete(redLine) 
canvas.delete(ALL) 
root.mainloop()
