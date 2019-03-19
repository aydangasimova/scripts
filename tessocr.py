import os
import shutil
from glob import glob
from tqdm import tqdm
import argparse
from collections import OrderedDict
from PIL import Image
import cv2
import pytesseract
import Levenshtein
from skimage.color import rgb2gray
from skimage import img_as_ubyte, img_as_float
from matplotlib import pyplot as plt


def split_video(path_to_video, out_path_to_images, time_period=2):
    """
    Splits video <path_to_video> to create images every <time_period> second
    and place it into folder <out_path_to_images>. Thus there will be L / time_period
    images, where L is the video length in secs.
    """
    path_to_video = path_to_video.replace(' ', '\ ')
    os.system('mkdir -p %s' % out_path_to_images)
    print('Splitting video:')
    print('ffmpeg -i {} -vf fps=1/{} {}/image%d.png'.format(path_to_video,
                                                            time_period,
                                                            out_path_to_images))
    result = os.system('ffmpeg -i {} -vf fps=1/{} {}/image%d.png > /dev/null 2>&1'.format(path_to_video,
                                                                                          time_period,
                                                                                          out_path_to_images))
    if result == 0:
        print('Success!')


def show_image(image):
    plt.figure(figsize=(20, 10))
    plt.imshow(image)


def show_hist(image):
    plt.figure(figsize=(10, 10))
    plt.hist(image.ravel(), 256)
    plt.show()


def crop_image(sk_img, crop_percentage=0.25):
    cropped = sk_img[-int(sk_img.shape[0] * crop_percentage):]
    return cropped


def preprocess_image(sk_img, show=False):
    """ First filter by color, then by grayscale to get white subtitles """

    if show:
        show_hist(sk_img)

    cropped = crop_image(sk_img, 0.2)

    # Filter channels that are not > threshold
    crop_mask = cropped > 0.95
    cropped[crop_mask] = 1.0
    cropped[~crop_mask] = 0

    if show:
        show_image(cropped)

    # Just pick ones that were white in real image
    grayscale_cropped = rgb2gray(cropped)
    final_image = grayscale_cropped == 1

    return final_image


def extract_text_from_sk_image(sk_img, img_preprocess_func, show=False):
    image = img_preprocess_func(sk_img)
    if show:
        show_image(image)
    cv_image = img_as_ubyte(image)
    text = pytesseract.image_to_string(cv_image)
    return text


def apply_ocr_to_many_images(path_to_images, out_txt_file, keep_images=False):
    """
    :path_to_images: a folder with images called image1.png, image2.png etc.
                     produced by the split_video func
    :out_txt_file: result will be written to this file
    :keep_images: whether to keep <path_to_images> in the end
    """
    print('Performing frame-wise OCR...')
    subtitles_by_image = ['']
    num_files = len(glob(os.path.join(path_to_images, '*')))
    for i in tqdm(range(1, num_files + 1)):
        image_path = os.path.join(path_to_images, 'image%d.png' % i)
        img = cv2.imread(image_path)
        sk_img = img_as_float(img)
        # os.remove(image_path)
        curr_text = extract_text_from_sk_image(sk_img, preprocess_image)
        # curr_text = subprocess.check_output(['tesseract', image_path, 'stdout']).decode('utf-8')
        lev_ratio = Levenshtein.ratio(curr_text, subtitles_by_image[-1])
        if lev_ratio < 0.5:
            subtitles_by_image.append(curr_text.replace('\n', ' ').strip())

    if not keep_images:
        shutil.rmtree(path_to_images)
    # removing duplicates
    subtitles_by_image = list(OrderedDict.fromkeys(subtitles_by_image[1:]))
    with open(out_txt_file, 'w') as out_f:
        out_f.write('\n'.join(subtitles_by_image))
    print('Done!')


def parse_args():
    parser = argparse.ArgumentParser(description="Video to subtitles v0.1")
    parser.add_argument('-i', '--input', help='Path to input video', required=True, type=str)
    parser.add_argument('-t', '--time_period', help='Video will be splitted in chunks of this length in secs.',
                        required=False, default=2, type=int)
    parser.add_argument('-o', '--output', help='Path to output txt file', required=False, default='out_subtitles.txt',
                        type=str)
    parser.add_argument('-tmp', '--tmp_dir', help='Path to tmp folder with images', required=False,
                        default='split_images', type=str)
    parser.add_argument('-keep', '--keep_images',
                        help='Whether to keep intermediate images. By default, they are deleted', action='store_true')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    split_video(path_to_video=args.input, out_path_to_images=args.tmp_dir, time_period=args.time_period)
    apply_ocr_to_many_images(path_to_images=args.tmp_dir, out_txt_file=args.output, keep_images=args.keep_images)


if __name__ == '__main__':
    main()

