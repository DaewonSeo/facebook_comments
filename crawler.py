# coding:utf-8
# python version 2.7

import facebook
import json
import pprint
import requests
import csv
import sys
import re


def main(access_token, file_name, post_id, email_check_regex):
    

    graph = facebook.GraphAPI(access_token)
    f = open('{}'.format(file_name), 'wb')
    csv_writer = csv.writer(f)
    profile = graph.get_object(id=post_id)
    comment_dummy = profile['comments']['data']

    for comment in comment_dummy:
        user_name = comment['from']['name']
        created_time = comment['created_time']
        message = comment['message']
        email_address = email_check_regex.match(message)
        if email_address is not None:
            email = email_address.group()
        else:
            email  = ""
        csv_writer.writerow([user_name.encode('utf-8'), created_time, message.encode('utf-8'), email])
        
    next_dummy = profile['comments']['paging']['next']

    while True:
        
        request_next = requests.get(next_dummy).json()
        comment_dummy = request_next['data']
        for comment in comment_dummy:
            user_name = comment['from']['name']
            created_time = comment['created_time']
            message = comment['message']
            email_address = email_check_regex.match(message)
            if email_address is not None:
                email =  email_address.group()
            else:
                email = ""
            csv_writer.writerow([user_name.encode('utf-8'), created_time, message.encode('utf-8'), email])
        try:
            next_dummy = request_next['paging']['next']
        except KeyError:
            print "모든 댓글이 모였습니다."
            f.close()
            sys.exit(1)

            
if __name__ == "__main__":
    access_token = '' #페이스북 액세스토큰 값 넣기
    # https://developers.facebook.com/tools/explorer/ 에서 로그인 후 액세스 토큰 가져오기. 
    
    email_check_regex = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)') # 댓글중 이메일 주소를 가져오기 위한 정규표현식 값 설정.
    file_name = 'comments.csv' # 파일이름명
    post_id = '' #디주얼에 댓글 가져오기 원하는 포스트의 id값 기재.
    main(access_token, file_name, post_id, email_check_regex)

