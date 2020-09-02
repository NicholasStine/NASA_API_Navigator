from tkinter import *
import json
import os
import requests
from PIL import Image
from io import BytesIO

# this program needs to be able to select any of the 3 mars rovers, choose from the available camers
# and choose a SOL (martian day), then display the corresponding image(s).

root = Tk()

curiosity_var = IntVar()
opportunity_var = IntVar()
spirit_var = IntVar()

rover_dict = {
    "curiosity": [curiosity_var, "curiosity"],
    "opportunity": [opportunity_var, "opportunity"],
    "spirit": [spirit_var, "spirit"]
}

fhaz_var = IntVar()
rhaz_var = IntVar()
mast_var = IntVar()
chemcam_var = IntVar()
mahli_var = IntVar()
mardi_var = IntVar()
navcam_var = IntVar()
pancam_var = IntVar()
minites_var = IntVar()

camera_dict = {
    "fhaz_var": [fhaz_var, "fhaz"],
    "rhaz_var": [rhaz_var, "rhaz"],
    "mast_var": [mast_var, "mast"],
    "chemcam_var": [chemcam_var, "chemcam"],
    "mahli_var": [mahli_var, "mahli"],
    "mardi_var": [mardi_var, "mardi"],
    "navcam_var": [navcam_var, "navcam"],
    "pancam_var": [pancam_var, "pancam"],
    "minites_var": [minites_var, 'minites']
}

sol_var = StringVar()

# GUI Class
class RoverGUI:

    def __init__(self, master):
        # BUILDING OUT THE GUI
        self.master = master
        master.geometry("500x500")
        master.title("Rover Image Viewer")

        # Image Display
        self.img_label = Label(master, text="Image Display")
        self.img_label.grid(column=4, row=1, columnspan=5, rowspan=3, padx=50, pady=50)

        # Details Display
        self.detail_label = Label(master, text="Detail Display")
        self.detail_label.grid(column=4, row=7, columnspan=5, rowspan=4, padx=50, pady=50)

        # Next & Previous Buttons
        self.prev_button = Button(master, text="Prev")
        self.next_button = Button(master, text="Next")
        self.prev_button.grid(column=5, row=5)
        self.next_button.grid(column=7, row=5)

        # Rover Selector
        self.rover_dropdown = Menubutton(master, text="Rover Selector", relief=RAISED)
        self.rover_dropdown.menu = Menu(self.rover_dropdown)
        self.rover_dropdown["menu"] = self.rover_dropdown.menu
        self.rover_dropdown.menu.add_checkbutton(label="Curiosity", variable=curiosity_var, command=lambda: self.setRoverMenu("curiosity"))
        self.rover_dropdown.menu.add_checkbutton(label="Opportunity", variable=opportunity_var, command=lambda: self.setRoverMenu("opportunity"))
        self.rover_dropdown.menu.add_checkbutton(label="Spirit", variable=spirit_var, command= lambda: self.setRoverMenu("spirit"))
        self.rover_dropdown.grid(column=1, row=1, columnspan=2)

        # Camera Selector
        self.camera_dropdown = Menubutton(master, text="Camera Selector", relief=RAISED)
        self.camera_dropdown.menu = Menu(self.camera_dropdown)
        self.camera_dropdown["menu"] = self.camera_dropdown.menu
        self.camera_dropdown.menu.add_checkbutton(label="FHAZ", variable=fhaz_var, command= lambda: self.setCameraMenu("fhaz"))
        self.camera_dropdown.menu.add_checkbutton(label="RHAZ", variable=rhaz_var, command= lambda: self.setCameraMenu("rhaz"))
        self.camera_dropdown.menu.add_checkbutton(label="MAST", variable=mast_var, command= lambda: self.setCameraMenu("mast"))
        self.camera_dropdown.menu.add_checkbutton(label="CHEMCAM", variable=chemcam_var, command= lambda: self.setCameraMenu("chemcam"))
        self.camera_dropdown.menu.add_checkbutton(label="MAHLI", variable=mahli_var, command= lambda: self.setCameraMenu("mahli"))
        self.camera_dropdown.menu.add_checkbutton(label="MARDI", variable=mardi_var, command= lambda: self.setCameraMenu("mardi"))
        self.camera_dropdown.menu.add_checkbutton(label="NAVCAM", variable=navcam_var, command= lambda: self.setCameraMenu("navcam"))
        self.camera_dropdown.menu.add_checkbutton(label="PANCAM", variable=pancam_var, command= lambda: self.setCameraMenu("pancam"))
        self.camera_dropdown.menu.add_checkbutton(label="MINITES", variable=minites_var, command= lambda: self.setCameraMenu("minites"))
        self.camera_dropdown.grid(column=1, row=2, columnspan=2)

        # Sol Field
        self.sol_label = Label(master, text="Sol Selector")
        self.sol_field = Entry(master, width=10, bg="light gray", textvariable=sol_var)
        self.sol_label.grid(column=1, row=3)
        self.sol_field.grid(column=2, row=3)

        # URL Selector
        self.load_urls_button = Button(master, text="Load URL's", command=self.genAPIURL)
        self.load_urls_button.grid(column=1, row=5, columnspan=2)

        # URL Display
        self.url_display = Label(master, text="URL Display")
        self.url_display.grid(column=1, row=7, columnspan=2, padx=50, pady=50)

        # Image Load Button
        self.load_image_button = Button(master, text="Load Image")
        self.load_image_button.grid(column=1, row=10, columnspan=2)

        # Save Image As

        # Copy Image to Clipboard 

        # Filler Rows and Columns
        filler_column_left = Label(master)
        filler_column_center = Label(master)
        filler_column_right = Label(master)

        filler_column_left.grid(column=0, rowspan=11, padx=10)
        filler_column_center.grid(column=3, rowspan=11, padx=40)
        filler_column_right.grid(column=9, rowspan=11, padx=10)
        
        filler_row_upper = Label(master)
        filler_row_up_center = Label(master)
        filler_row_down_center = Label(master)
        filler_row_lower = Label(master)

        filler_row_upper.grid(row=0, columnspan=9, pady=10)
        filler_row_up_center.grid(row=4, columnspan=9, pady=10)
        filler_row_down_center.grid(row=6, columnspan=9, pady=10)
        filler_row_lower.grid(row=11, columnspan=9, pady=10)

    # GUI METHODS
    # Clear Previous Menu Selection
    def setRoverMenu(self, menuOption):
        for rover in rover_dict:
            if(menuOption != rover_dict[rover][1]):
                rover_dict[rover][0].set(0)

    def setCameraMenu(self, menuOption):
        for camera in camera_dict:
            if(menuOption != camera_dict[camera][1]):
                camera_dict[camera][0].set(0)

    # Image Display
    def displayImage():
        pass

    # Next & Previous Buttons
    def nextImage():
        pass

    def previousImage():
        pass

    # Generate the API request URL
    def genAPIURL(self):
        for rover in rover_dict:
            if(rover_dict[rover][0].get() == 1):
                current_rover = rover_dict[rover][1]
        for camera in camera_dict:
            if(camera_dict[camera][0].get() == 1):
                current_camera = camera_dict[camera][1]
        current_sol = sol_var.get()
        ImgRequest(current_rover, current_camera, current_sol)
                

    # Save Image As
    def saveImage():
        pass

    # Copy Image to Clipboard 
    def copyImage():
        pass


# ImgRequeste Class
class ImgRequest:
    def __init__(self, rover, camera, sol):
        self.API_ROOT_ADDRESS = "https://api.nasa.gov/mars-photos/api/v1/rovers/"
        self.API_KEY = "MfZEUxZHkH1u9hJgLIdWYnxMbsV53UcvzyA3bhmK"
        self.rover = rover
        self.camera = camera
        self.sol = sol

        self.url_list = []
        self.img_list = []
        self.loaded_images = []
        self.api_response = None
        self.make_request()
        self.extract_urls()
        current_image = self.load_image(self.url_list[0])
        current_image.show()

    # this class needs to be able to request all images based on the search criteria
    
    # Make the API request
    def make_request(self):
        api_address = "%s%s/photos?sol=%s&camera=%s&api_key=%s" % (self.API_ROOT_ADDRESS, self.rover, self.sol, self.camera, self.API_KEY)
        self.api_response = requests.get(api_address)
        print(self.api_response.status_code)

    # Extract the appropriate URL's
    def extract_urls(self):
        json_response = json.loads(self.api_response.content)
        self.url_list.clear()
        for image in json_response["photos"]:
            # print(image["img_src"])
            self.url_list.append(image["img_src"])

    # Load each image into a list of images
    def load_image(self, url):
        print("\n\n\n LOADING ZE IMAGES!!!")
        # print(self.url_list)
        img_response = requests.get(url)
        return_image = Image.open(BytesIO(img_response.content))
        self.img_list.append(return_image)
        return return_image



my_gui = RoverGUI(root)



# ImgRequest("curiosity", "mast", "1000")

root.mainloop()


