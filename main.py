import argparse
import lbooth_api


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Downloads the imagges and videos from a URL and saves it to a specified directory.')
    parser.add_argument('url', help='The URL of the resources to download')
    parser.add_argument('directory', help='The path to the directory where the file will be saved')
    args = parser.parse_args()
    lbooth_api.dowload_all_images_and_videos_from_main_url(main_url=args.url, output_folder_path=args.directory)