import os, math, re
from PIL import Image, ImageFont, ImageDraw 

fontPath = "arial.ttf" #'Aaargh.ttf'#
#fontPath = "/usr/share/fonts/dejavu-lgc/DejaVuLGCSansCondensed-Bold.ttf"
font = ImageFont.truetype(fontPath, 30)

def make_big_plot(folders,root):

	no_of_col = 4
	no_of_row = 3

	plot_types = ['RDF','No_of_Neighbours']
	for plot_type in plot_types:
		counter = 0
		page_counter = 1
		while counter < len(folders):
			folder = folders[0]
			img  = Image.open(root+'/'+folder+'/'+folder+'_'+plot_type+'.png')
			width, height = img.size
			total_width  = int(math.ceil(width  * 3.0))
			total_height = int(math.ceil(height * 4.0))

			new_im = Image.new('RGB', (total_width, total_height), (255, 255, 255))

			col_offset = 0
			for i in range(no_of_col):
				row_offset = 0
				for j in range(no_of_row):
					if counter < len(folders):
						folder = folders[counter]
						#img  = mpimg.imread(root+'/'+folder+'/'+folder+'_RDF.png')
						img  = Image.open(root+'/'+folder+'/'+folder+'_'+plot_type+'.png')
						draw = ImageDraw.Draw(img)
						draw.text((80, 40),folder,(0,0,0),font=font)
						new_im.paste(img, (row_offset,col_offset))
						row_offset += width
						counter += 1
				col_offset += height
			new_im.save(root+'/'+'ALL_'+str(plot_type)+'_Page_'+str(page_counter)+'.png')
			page_counter += 1


for root, dirs, files in os.walk('all_comps_GeoProps', topdown=False):
	if not 'GeoProps' in root:
		dirs[:] = []
		files[:] = []
	if any([('cu' in a_dir) for a_dir in dirs]):
		folders = [folder for folder in os.listdir(root) if not '.DS_Store' in folder and os.path.isdir(root+'/'+folder)]
		folders = [re.split('(\d+)',folder) for folder in folders]
		folders = [folder[:-1] for folder in folders]
		#print(folders)
		folders = [(folder[0],int(folder[1]),folder[2],int(folder[3])) for folder in folders]
		folders.sort()
		folders = [''.join([folder[0],str(folder[1]),folder[2],str(folder[3])]) for folder in folders]
		make_big_plot(folders,root)
		dirs[:] = []
		files[:] = []

for root, dirs, files in os.walk('select_comps_GeoProps', topdown=False):
	if not 'GeoProps' in root:
		dirs[:] = []
		files[:] = []
	if 'cu' in root:
		dirs.sort()
		make_big_plot(dirs,root)
		dirs[:] = []
		files[:] = []