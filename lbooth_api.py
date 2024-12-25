import os
import time

import requests
from bs4 import BeautifulSoup
import tqdm

BASE_DOWNLOA_DIMAGE_URL="https://lbooth.com/snippet/download_moment?moment_short_id={moment_short_id}&type={type}"

def get_image_download_link(moment_short_id):
    return BASE_DOWNLOA_DIMAGE_URL.format(moment_short_id=moment_short_id, type='regular-photo')

def get_video_download_link(moment_short_id):
    return BASE_DOWNLOA_DIMAGE_URL.format(moment_short_id=moment_short_id, type='countdown-video')

def get_boomerang_download_link(moment_short_id):
    return BASE_DOWNLOA_DIMAGE_URL.format(moment_short_id=moment_short_id, type='boomerang-video')

def get_moment_shorts_ids_from_main_url(url):
    response=requests.get(url)
    # with open('./response.html', 'w') as f:
    #     f.write(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')

    divs_strip_moment = soup.find_all('div', class_='strip-moment')

    moment_shorts_ids=[]

    for div in divs_strip_moment:
        moment_short_id=div.find('a')['href'][1:] # remove the first character wich is a '/'
        moment_shorts_ids.append(moment_short_id)
        
    return moment_shorts_ids

def request_and_save_content_as_file(url, file_path):
    """Downloads the content from the given URL and saves it to the specified file.

    Args:
        url: The URL of the resource to download.
        file_path: The path to the file where the content will be saved.

    Returns:
        None
    """
    # print(f"Saving content from {url} to {file_path}")
    time.sleep(1)
    return

    response = requests.get(url)

    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        # print(f"Content saved successfully to {file_path}")
    else:
        print(f"Error downloading content. Status code: {response.status_code}")

def request_and_save_image(moment_short_id, output_folder_path):
    output_path=os.path.join(output_folder_path, f'{moment_short_id}.jpg')
    image_download_url=get_image_download_link(moment_short_id)
    return request_and_save_content_as_file(image_download_url, output_path)

def request_and_save_video(moment_short_id, output_folder_path):
    output_path=os.path.join(output_folder_path, f'{moment_short_id}.mp4')
    video_download_url=get_video_download_link(moment_short_id)
    return request_and_save_content_as_file(video_download_url, output_path)

def dowload_all_images_and_videos_from_main_url(main_url, output_folder_path):
    """
    The main url is expected to be of the form 

        https://lbooth.com/<album_id>
    
    Example:

        https://lbooth.com/W4VgZQNQMTP
    
    
    """
    assert os.path.exists(output_folder_path), f"The folder {full_output_folder_path} does not exists!"


    moment_shorts_ids=get_moment_shorts_ids_from_main_url(main_url)
    print(f"Found {len(moment_shorts_ids)} images/videos for URL: {main_url}")

    album_id=main_url.split('/')[-1]

    full_output_folder_path=os.path.join(output_folder_path, album_id)

    # print(f"{output_folder_path=}, {album_id=}, {full_output_folder_path=}")

    if not os.path.exists(full_output_folder_path):
        os.mkdir(full_output_folder_path)
        print(f"Creating {full_output_folder_path} ...")

    print(f"Downloading contents to {full_output_folder_path} ...")
    for moment_short_id in tqdm.tqdm(moment_shorts_ids):
        request_and_save_image(moment_short_id, full_output_folder_path)
        request_and_save_video(moment_short_id, full_output_folder_path)

