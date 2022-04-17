import skimage.data
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import selectivesearch
import os
import time
import openpyxl as opx

def main(scale, sigma, min_size):

    # loading astronaut image
    img = skimage.data.astronaut()
    # img = skimage.data.chelsea() 
    
    # perform selective search
    begin = time.time()
    img_lbl, regions = selectivesearch.selective_search(
        img, scale=scale, sigma=sigma, min_size=min_size)
    end = time.time()
    # print time
    ss_time = end-begin
    print(ss_time) 
    
    candidates = set()
    for r in regions:
        # excluding same rectangle (with different segments)
        if r['rect'] in candidates:
            continue
        # excluding regions smaller than 2000 pixels
        if r['size'] < 2000:
            continue
        # distorted rects
        x, y, w, h = r['rect']
        if w / h > 1.2 or h / w > 1.2:
            continue
        candidates.add(r['rect'])

    # draw rectangles on the original image
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(img)
    for x, y, w, h in candidates:
        # print(x, y, w, h)
        rect = mpatches.Rectangle(
            (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)

    # plt.show()
    
    # # save
    root = r'D:\Github\selectivesearch\out'
    # img_name = 'scale={}--sigma={}--min_size={}.png'.format(scale, sigma, min_size)
    # plt.savefig(os.path.join(root, img_name))
    
    # excel
    excel_name = '1.xlsx'
    excel_path = os.path.join(root, excel_name)
    wb = opx.load_workbook(excel_path)
    ws = wb.active
    ws.append([scale, sigma, min_size, ss_time])
    wb.save(excel_path)

if __name__ == "__main__":
    
    scale_list = [300, 400, 500, 600]
    sigma_list = [0.7, 0.8, 0.9]
    min_size_list = [10, 50, 100]
    for scale in scale_list:
        for sigma in sigma_list:
            for min_size in min_size_list:
                print('scale={}  --  sigma={}  --  min_size={}'.format(scale, sigma, min_size))
                main(scale, sigma, min_size)
    