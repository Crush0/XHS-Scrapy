import myRequests.mediaRequest as mr
import argparse
import os
import sys

dir_name = os.path.split(os.path.abspath(sys.argv[0]))[0]


def run(args_):
    print('======抓取中======')
    mr.getUserMidea(args_.user_id, args_.cookie, args_)
    print('=====大功告成=====')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_id', type=str, required=True, help='地址栏中用户的ID')
    parser.add_argument('--cookie', type=str, required=True, help="你的Cookie")
    parser.add_argument('--output', type=str, default=os.path.join(dir_name, 'output'), help="输出目录")
    parser.add_argument('--fetch_image', type=str, default=True, help="是否抓取图片")
    parser.add_argument('--fetch_video', type=str, default=True, help="是否抓取视频")
    args = parser.parse_args()
    if args.fetch_image in ['False', 'false', 'n', 'no', '0']:
        args.fetch_image = False
    if args.fetch_video in ['False', 'false', 'n', 'no', '0']:
        args.fetch_video = False
    run(args)
