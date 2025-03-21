try:
    from . import utils as ut
    from . import global_state
    from .base_boxes import bindArrows
except (SystemError, ValueError, ImportError):
    import utils as ut
    import global_state
    from base_boxes import bindArrows

try:
    import tkinter as tk  # python 3
    import tkinter.font as tk_Font
except:
    import Tkinter as tk  # python 2
    import tkFont as tk_Font

# TODO: bindArrows seems to be in the wrong place.


boxRoot = None
entryWidget = None
__enterboxText = ''
__enterboxDefaultText = ''
cancelButton = None
okButton = None


def __fillablebox(msg, title="", default="", mask=None, image=None, root=None):
    """
    Show a box in which a user can enter some text.
    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.
    Returns the text that the user entered, or None if they cancel the operation.
    """

    global boxRoot, __enterboxText, __enterboxDefaultText
    global cancelButton, entryWidget, okButton

    if title is None:
        title = ""
    if default is None:
        default = ""
    __enterboxDefaultText = default
    __enterboxText = __enterboxDefaultText

    if root:
        root.withdraw()
        boxRoot = tk.Toplevel(master=root)
        boxRoot.withdraw()
    else:
        boxRoot = tk.Tk()
        boxRoot.withdraw()

    boxRoot.protocol('WM_DELETE_WINDOW', __enterboxQuit)
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(global_state.window_position)
    boxRoot.bind("<Escape>", __enterboxCancel)

    # ------------- define the messageFrame ---------------------------------
    messageFrame = tk.Frame(master=boxRoot)
    messageFrame.pack(side=tk.TOP, fill=tk.BOTH)

    # ------------- define the imageFrame ---------------------------------
    try:
        tk_Image = ut.load_tk_image(image)
    except Exception as inst:
        print(inst)
        tk_Image = None
    if tk_Image:
        imageFrame = tk.Frame(master=boxRoot)
        imageFrame.pack(side=tk.TOP, fill=tk.BOTH)
        label = tk.Label(imageFrame, image=tk_Image,
                         font=(global_state.EgFont.text_font_name, 
                            global_state.EgFont.text_font_size, 
                            global_state.EgFont.text_font_style,
                            global_state.EgFont.text_font_slant
                            )
                         )
        label.image = tk_Image  # keep a reference!
        label.pack(side=tk.TOP, expand=tk.YES, fill=tk.X, padx='1m', pady='1m')

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = tk.Frame(master=boxRoot)
    buttonsFrame.pack(side=tk.TOP, fill=tk.BOTH)

    # ------------- define the entryFrame ---------------------------------
    entryFrame = tk.Frame(master=boxRoot)
    entryFrame.pack(side=tk.TOP, fill=tk.BOTH)

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = tk.Frame(master=boxRoot)
    buttonsFrame.pack(side=tk.TOP, fill=tk.BOTH)

    # -------------------- the msg widget ----------------------------
    messageWidget = tk.Message(messageFrame, width="4.5i", text=msg,
                               font=(global_state.EgFont.text_font_name, 
                                    global_state.EgFont.text_font_size, 
                                    global_state.EgFont.text_font_style,
                                    global_state.EgFont.text_font_slant
                                    )
                               )
    messageWidget.configure(
        font=(global_state.PROPORTIONAL_FONT_FAMILY, global_state.PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(
        side=tk.RIGHT, expand=1, fill=tk.BOTH, padx='3m', pady='3m')

    # --------- entryWidget ----------------------------------------------
    entryWidget = tk.Entry(entryFrame, width=40,
                           font=(global_state.EgFont.text_font_name, 
                                global_state.EgFont.text_font_size, 
                                global_state.EgFont.text_font_style,
                                global_state.EgFont.text_font_slant
                                )
                           )
    bindArrows(entryWidget)
    entryWidget.configure(
        font=(global_state.PROPORTIONAL_FONT_FAMILY, global_state.TEXT_ENTRY_FONT_SIZE))
    if mask:
        entryWidget.configure(show=mask)
    entryWidget.pack(side=tk.LEFT, padx="3m")
    entryWidget.bind("<Return>", __enterboxGetText)
    entryWidget.bind("<Escape>", __enterboxCancel)
    # put text into the entryWidget
    entryWidget.insert(0, __enterboxDefaultText)

    # ------------------ ok button -------------------------------
    okButton = tk.Button(buttonsFrame, takefocus=1, text="OK", 
                         font=(global_state.EgFont.button_font_name, 
                               global_state.EgFont.button_font_size, 
                               global_state.EgFont.button_font_style,
                               global_state.EgFont.button_font_slant
                            )
                         )
    bindArrows(okButton)
    okButton.pack(
        expand=1, side=tk.LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event
    # handler
    commandButton = okButton
    handler = __enterboxGetText
    for selectionEvent in global_state.STANDARD_SELECTION_EVENTS:
        commandButton.bind("<{}>".format(selectionEvent), handler)

    mouse_handlers = ut.mouse_click_handlers(__enterboxGetText)
    for selectionEvent in global_state.STANDARD_SELECTION_EVENTS_MOUSE:
        okButton.bind("<%s>" % selectionEvent, mouse_handlers[selectionEvent])

    # ------------------ cancel button -------------------------------
    cancelButton = tk.Button(buttonsFrame, takefocus=1, text="Cancel",
                                font=(global_state.EgFont.button_font_name, 
                                      global_state.EgFont.button_font_size, 
                                      global_state.EgFont.button_font_style,
                                      global_state.EgFont.button_font_slant
                                )
                             )
    bindArrows(cancelButton)
    cancelButton.pack(
        expand=1, side=tk.RIGHT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event
    # handler
    commandButton = cancelButton
    handler = __enterboxCancel
    for selectionEvent in global_state.STANDARD_SELECTION_EVENTS:
        commandButton.bind("<{}>".format(selectionEvent), handler)
    mouse_handlers = ut.mouse_click_handlers(__enterboxCancel)
    for selectionEvent in global_state.STANDARD_SELECTION_EVENTS_MOUSE:
        cancelButton.bind("<%s>" % selectionEvent, mouse_handlers[selectionEvent])


    # ------------------- time for action! -----------------
    entryWidget.focus_force()  # put the focus on the entryWidget
    boxRoot.deiconify()
    boxRoot.mainloop()  # run it!

    # -------- after the run has completed ----------------------------------
    if root:
        root.deiconify()
    boxRoot.destroy()  # button_click didn't destroy boxRoot, so we do it now
    return __enterboxText


def __enterboxQuit():
    return __enterboxCancel(None)


def __enterboxCancel(event):
    global __enterboxText

    __enterboxText = None
    boxRoot.quit()


def __enterboxGetText(event):
    global __enterboxText

    __enterboxText = entryWidget.get()
    boxRoot.quit()


def __enterboxRestore(event):
    global entryWidget

    entryWidget.delete(0, len(entryWidget.get()))
    entryWidget.insert(0, __enterboxDefaultText)
