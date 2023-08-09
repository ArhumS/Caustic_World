#Usage $python3 stich_test.py --base_path=C:/Users/as2016/Downloads/o_piece_l_5_4 -seq_id 3 --prefix=predict_left
#to do it for a range of sequence, for example from 1 to 100
#python3 stich_test.py --base_path=C:/Users/as2016/Downloads/o_piece_l_5_4 -seq_id 1-100
#python3 stich_test.py --base_path=C:/Users/as2016/Downloads/o_piece_l_5_4 -seq_id 1-6 --prefix=predict_left

from PIL import Image
import os
import glob
import sys
import subprocess
import argparse

def get_args():
      parser = argparse.ArgumentParser()
      parser.add_argument("--base_path", type =str, default = None,  help  = "base directory of image files")
      parser.add_argument("--ext", type = str, default = '.png', help = "extension of image files")
      parser.add_argument("--save_dir", type =str , default = None,  help ="output directory")
      parser.add_argument("-seq_id", type = str, default = None, required = True, help = "Sequence id")
      parser.add_argument('--x_offset', type = int, default = 0, help = "x offset")
      parser.add_argument('--y_offset', type = int, default = 0,  help ="y offset")
      parser.add_argument("--prefix", type = str, default ="", help ="prefix for saving files")      
      
      return parser.parse_args()

def get_pwd():
      
      return str(subprocess.check_output('pwd')).replace('\\', '/').replace(' ', "")
            
def get_sequence(base, seq_id, ext = '.png'):
   
      files = glob.glob(os.path.join(base, '*' +ext))
      files = [os.path.split(f)[1] for f in files]
      res = []
      print(f"{len(files)} pieces found ")
      for file in files:
            f= file.split('_')
            
            if f[-2] == f"{seq_id}":
                res.append(file)
      
      if len(res) == 0:
            print(f"No files found with the sequence id {seq_id}")
      else:
            print(f"{len(res)} files found with sequence id {seq_id}")
      
      return res

def stack(base, seq_id, x_offset = 0, y_offset = 0, ext = '.png', save_dir = None, prefix = ""):
      
      files = get_sequence(base, seq_id, ext = ext)
      final_image = Image.new("RGB", (1422, 948))
      sorted_files = {}
      for img in files:
            _ = img.split('_')
            subseq = int(_[-1].replace(ext,""))
            sorted_files[subseq] = img
            
      print("Images are sorted")
      for i in range(len(sorted_files.keys())):#range(len(sorted_files)):
            image = sorted_files[i]

            image = Image.open(os.path.join(base,image))
            final_image.paste(image, (x_offset, y_offset))
            x_offset += image.width
            if x_offset >= final_image.width:
                  x_offset = 0
                  y_offset += image.height
      if save_dir:
            if not os.path.isdir(save_dir):
                  print(" Output directory doesnt exist,creating one ....")
                  os.makedirs(save_dir)
      else:
            save_dir = os.mkdir(os.path.join(base,"stitched"))
            print(f"save directory not specified, using {base}/stitched as the save directory")
      final_image.save(os.path.join(save_dir, f"{prefix}{seq_id}.png"))
      print(f"img saved as", os.path.join(save_dir, f'{prefix}_{seq_id}.png'))       

if __name__ == "__main__":
      
      args = get_args()
	
      if '-' in args.seq_id:
            ranges_seq = args.seq_id.split('-')
            low_seq = ranges_seq[0]
            high_seq = ranges_seq[1]
            try:
                  low_seq = int(low_seq)
                  high_seq = int(high_seq)
			
                  for i in range(low_seq, high_seq+1):
                      stack(args.base_path, i, save_dir = args.save_dir, x_offset = args.x_offset, y_offset =args.y_offset, ext = args.ext, prefix = args.prefix)
            except Exception as e:
                  print("Invalid sequence range")
                  
      '''else:
            try:
                  args.seq_id = int(args.seq_id)
                  stack(args.base_path, args.seq_id, save_dir = args.save_dir, x_offset = args.x_offset, y_offset =args.y_offset, ext = args.ext, prefix = args.prefix)
            except Exception as e:
                  print("Invalid sequence")
                  sys.exit()   
            print("stitch Done.")'''
      
     
"""img_ext = '.png'
sub_images = []
ranges_seq = args.seq_id.split('-')
low_seq = ranges_seq[0]
high_seq = ranges_seq[1]
for i in range(1,7):
    sub_image = Image.open(f"{base_path}{i}{image_extension}")  
    sub_images.append(sub_image)

final_image = Image.new("RGB", (1422, 948))

x_offset = 0
y_offset = 0
for sub_image in sub_images:
    final_image.paste(sub_image, (x_offset, y_offset))
    x_offset += sub_image.width
    if x_offset >= final_image.width:
        x_offset = 0
        y_offset += sub_image.height

final_image.save("left_0.png")"""