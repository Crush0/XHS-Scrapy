import json
import os
import requests
import utils.headerUtils as headerU
import utils.MediaUtils as imageU

USER_POSTED = 'https://edith.xiaohongshu.com/api/sns/web/v1/user_posted'


def cookie_to_dic(cookie):
    return {item.split('=')[0]: item.split('=')[1] for item in cookie.split('; ')}


def getUserMidea(user_id, cookie, args, cursor=''):
    note_id = []

    def getUserImageHelper(cursor_):
        cookie_ = cookie_to_dic(cookie)
        params = {
            'num': '30',
            'cursor': cursor_,
            'user_id': user_id,
        }
        url = USER_POSTED.format(cursor_, user_id)
        header = headerU.getHeader(url, param=params, data={}, cookie=cookie_)
        resp = requests.get(url, headers=header, params=params, cookies=cookie_)
        json_data = json.loads(resp.text)
        if not json_data['success']:
            raise Exception(f'{url} 请求失败')
        new_cursor = json_data['data']['cursor']
        notes = json_data['data']['notes']
        for note in notes:
            if (note['type'] == 'normal' and args.fetch_image) or (note['type'] == 'video' and args.fetch_video):
                note_id.append(note['note_id'])
        if json_data['data']['has_more']:
            getUserImageHelper(new_cursor)
        else:
            for note_id_ in note_id:
                feed(note_id_, cookie_, args)

    getUserImageHelper(cursor)
    note_id.clear()


def feed(note_id_, cookie_, args):
    username = ''
    json_data = {
        'source_note_id': note_id_
    }
    url = 'https://edith.xiaohongshu.com/api/sns/web/v1/feed'
    header = headerU.getHeader(url, param={}, data=json_data, cookie=cookie_)
    json_data = json.dumps(json_data).replace(' ', '')
    response = requests.post(url, cookies=cookie_, headers=header,
                             data=json_data)
    json_data = json.loads(response.text)
    if json_data['success']:
        items = json_data['data']['items']
        for item in items:
            if item['model_type'] == 'note':
                note_card = item['note_card']
                if username == '':
                    username = note_card['user']['nickname']
                if note_card['type'] == 'normal':
                    print(f'开始下载[图片]:{note_id_}')
                    image_parse(username, note_id_, note_card, args)
                elif note_card['type'] == 'video':
                    print(f'开始下载[视频]:{note_id_}')
                    video_parse(username, note_id_, note_card, args)


def video_parse(username, note_id_, note_card, args):
    media = note_card['video']['media']
    stream = media['stream']
    save_path = os.path.join(args.output, username, 'video')
    key = ''
    for k, v in stream.items():
        if len(v) != 0:
            key = k
            break
    if key != '':
        video_url = stream[key][0]['master_url']
        imageU.downloadFromUrl(video_url, save_path, f'{note_card["title"].replace(" ","")}.mp4')
    print(f'{note_id_}下载完成')


def image_parse(user_id, note_id_, note_card, args):
    image_list = note_card['image_list']
    index = 0
    save_path = os.path.join(args.output, user_id, 'images')
    for image in image_list:
        trace_id = image['trace_id']
        url = f"https://sns-img-qc.xhscdn.com/{trace_id}"
        imageU.downloadFromUrl(url, save_path, f'{note_card["title"].replace(" ","")}-{index}.png')
        index += 1
    print(f'{note_id_}下载完成')
