#!/usr/bin/env python2
import pygtk
pygtk.require("2.0")
import gtk

class TextBox:
    def about_dialog(self, data=None):
        about = gtk.AboutDialog()
        about.set_program_name("PyPad")
        about.set_version("0.1")
        about.set_copyright("Copyright (c) xeeew")
        about.set_comments("A simple GTK text editor")
        about.set_logo(gtk.gdk.pixbuf_new_from_file("pypad.png"))
        about.run()
        about.destroy()

    def confirm_dialog(self):
        d = gtk.Dialog()
        d.set_default_size(300, 150)
        d.add_buttons(gtk.STOCK_CANCEL, 0, gtk.STOCK_NO, 1, gtk.STOCK_YES, 2)
        index = self.filename.replace("\\","/").rfind("/") + 1
        label = gtk.Label("Save changes to '" + (self.filename[index:] or "Untitled") + "'?")
        label.show()
        d.vbox.pack_start(label)
        answer = d.run()
        d.destroy()
        return answer

    def save_as(self, data=None):
        textbuffer = self.textview.get_buffer()
        dialog = gtk.FileChooserDialog("Save file",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("Text Files")
        filter.add_mime_type("text/data")
        filter.add_pattern("*.txt")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("All Files")
        filter.add_pattern("*.*")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.filename = dialog.get_filename()
            print "Saved file: " + self.filename
            index = self.filename.replace("\\","/").rfind("/") + 1
            text = textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter())
            self.window.set_title(self.filename[index:] + " - PyPad")
            file = open(self.filename, "w")
            file.write(text)
            file.close()
            textbuffer.set_modified(False)
        dialog.destroy()

    def save(self, data=None):
        if self.filename == "":
            self.save_as()
            return

        textbuffer = self.textview.get_buffer()
        print "Saved file: " + self.filename
        text = textbuffer.get_text(textbuffer.get_start_iter() , textbuffer.get_end_iter())
        file = open(self.filename, "w")
        file.write(text)
        file.close()
        textbuffer.set_modified(False)


    def delete_event(self, widget, data=None):
        textbuffer = self.textview.get_buffer()
        if textbuffer.get_modified():
            # Cancel = 0, No = 1, Yes = 2
            user = self.confirm_dialog()

            if user == 0:
                return True
            elif user == 2:
                self.save()

        gtk.main_quit()
        return False

    def new_file(self, data=None):
        textbuffer = self.textview.get_buffer()
        if textbuffer.get_modified():
            # Cancel = 0, No = 1, Yes = 2
            user = self.confirm_dialog()

            if user == 0:
                return
            elif user == 2:
                self.save()

        self.window.set_title("Untitled - PyPad")
        textbuffer.set_text("")
        textbuffer.set_modified(False)

    def open_file(self, data=None):
        textbuffer = self.textview.get_buffer()
        dialog = gtk.FileChooserDialog("Open..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("Text")
        filter.add_mime_type("text/data")
        filter.add_pattern("*.txt")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.filename = dialog.get_filename()
            print "Opened file: " + self.filename
            index = self.filename.replace("\\","/").rfind("/") + 1
            self.window.set_title(self.filename[index:] + " - PyPad")
            file = open(self.filename, "r")
            text = file.read()
            textbuffer.set_text(text)
            file.close()
            textbuffer.set_modified(False)
        dialog.destroy()

    def menubar(self):
        mb = gtk.MenuBar()

        filemenu = gtk.Menu()
        filem = gtk.MenuItem("_File")
        filem.set_submenu(filemenu)

        agr = gtk.AccelGroup()
        self.window.add_accel_group(agr)

        newi = gtk.ImageMenuItem(gtk.STOCK_NEW, agr)
        key, mod = gtk.accelerator_parse("<Control>N")
        newi.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        newi.connect("activate", self.new_file)
        filemenu.append(newi)

        openi = gtk.ImageMenuItem(gtk.STOCK_OPEN, agr)
        key, mod = gtk.accelerator_parse("<Control>O")
        newi.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        openi.connect("activate", self.open_file)
        filemenu.append(openi)

        savei = gtk.ImageMenuItem(gtk.STOCK_SAVE, agr)
        key, mod = gtk.accelerator_parse("<Control>S")
        savei.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        savei.connect("activate", self.save)
        filemenu.append(savei)

        save_asi = gtk.ImageMenuItem(gtk.STOCK_SAVE_AS, agr)
        key, mod = gtk.accelerator_parse("<Control><Shift>S")
        save_asi.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        save_asi.connect("activate", self.save_as)
        filemenu.append(save_asi)

        sep = gtk.SeparatorMenuItem()
        filemenu.append(sep)

        quiti = gtk.ImageMenuItem(gtk.STOCK_QUIT, agr)
        key, mod = gtk.accelerator_parse("<Control>Q")
        quiti.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        quiti.connect("activate", self.delete_event)
        filemenu.append(quiti)

        helpmenu = gtk.Menu()
        helpm = gtk.MenuItem("_Help")
        helpm.set_submenu(helpmenu)

        about = gtk.ImageMenuItem(gtk.STOCK_ABOUT, agr)
        about.connect("activate", self.about_dialog)
        helpmenu.append(about)

        mb.append(filem)
        mb.append(helpm)
        self.hbox.pack_start(mb, False, False, 0)

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.set_title("Untitled - PyPad")
        self.window.set_default_size(750, 450)

        self.filename = ""

        # hbox holds the menubar, container holds hbox and everything else
        container = gtk.VBox(False, 0)
        self.hbox = gtk.HBox(False, 0)

        container.pack_start(self.hbox, False, False, 0)

        # Create the menubar
        self.menubar()

        # Create scrolling window
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        # Create textbox
        self.textview = gtk.TextView()
        self.textview.set_editable(True)
        self.textview.set_wrap_mode(gtk.WRAP_WORD)
        self.textview.set_cursor_visible(True)

        self.textview.set_border_window_size(gtk.TEXT_WINDOW_LEFT, 1)
        self.textview.set_border_window_size(gtk.TEXT_WINDOW_RIGHT, 1)
        self.textview.set_border_window_size(gtk.TEXT_WINDOW_TOP, 0)
        self.textview.set_border_window_size(gtk.TEXT_WINDOW_BOTTOM, 1)

        # Add textbox to scrolled window
        sw.add(self.textview)
        container.pack_start(sw, True, True, 0)

        self.window.add(container)
        self.window.show_all()

TextBox()
gtk.main()

