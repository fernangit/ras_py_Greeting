# -*- coding: utf-8 -*-
import sys, errno
import picamera
import picamera.array
import cv2 as cv

from datetime import datetime
import time
import random
import subprocess

import jtalk

morning = 'おはようございまーすっ'
evening = 'おつかれさまですーーぅ'
mng_lst = ['ういーす',
           'おーす',
           'ぐっもーにん',
           'おはよございます',
           'おはようさん',
           'おはようさんがりあ',
           'おいーす',
           'おはようぐると',
           'ざいまーす',
           'ざいますっ',
           'もーにん',
           'おはよお',
           'ざーす']
evg_lst = ['おつかれさまんさー',
           'おっつー',
           'おつかれーしょん',
           'おつかれさん',
           'おつかれさんがりあ',
           'おつかれさんにくえんさん',
           'おつかれー',
           'おつかれさまんさたばさ',
           'おつかれっすー',
           'おいっす',
           'おつかれーらいす',
           'おいーっす',
           'おつかれいしゅう',
           'おつかれえ',
           'いーす',
           'ちーす']
mono_lst = ['んーーーー',
           'なんだかとってもこどく',
           'じこちゅうでいくぞー',
           'ひとりはこわい',
           'それがおまえらのやりかたかー',
           'だが　ことわる',
           'どんとしんく　ふぃーーる',
           'おれのなをいってみろ',
           'なっ何をするだー',
           '認めたくないものだな　わかさゆえのあやまちというものを',
           'バスケがしたいです',
           'やれやれだぜ',
           'きんきんにひえてやがる',
           'てめえらの血はなにいろだーっ',
           'ズビズバー',
           'みろ　人間がゴミのようだ',
           'ぬんっ',
           'うりりりりりりぃぃ',
           'めめたぁ',
           'せいっ',
           'ぱぱうぱうぱう',
           'ひいーー',
           'ふーーー',
           'ふっ',
           'ふっふっふっふっ',
           'しぇーー',
           'しゅっ',
           'しょっ',
           'じゃっ',
           'しゃーーー',
           'おらおらおらおらおらー',
           'ばるばるばるばるばるー',
           'ばおーー',
           'きゅー',
           'むーーーー',
           'おおおおおおおお',
           'むむむ',
           'うむ',
           'うわーー',
           'にーーーん',
           'はふ',
           'はひ',
           'むーーーーん',
           'ひproc.stdin.write("q")でぶっ',
           'あべしっ',
           'ぐぬぬ',
           'ひょっ',
           'ぐわーーーー',
           'ぐおーーーー',
           'おうふ',
           'すううううーー',
           'ぶううううーー',
           'ぶーーーーーん',
           'ごごごごごご',
           'ずこっ',
           'ずっきゅうううん',
           'どっきゅうううん',
           'ぎゃーん',
           'がーーーん',
           'ざわ ざわ ざわ',
           'びくっ',
           'ぎくっ',
           'あたたたたたたた',
           'ほおあ',
           'ぎゅー']
t_st = 0
'''
img = cv.imread('受付_Moment.jpg')
img_resize = cv.resize(img, (640, 365))
cv.imshow("M's Aisatsu Unit", img_resize)
cv.moveWindow("M's Aisatsu Unit", -35, -3) 
'''

#アイドル動画をループ再生
cmd = "exec omxplayer --loop アイドル.mp4"
idleProc = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE)

jtalk.jtalk('えむず　あいさつユニット しどうっ')
d = datetime.now()
nxt_h = d.hour
nxt_m = random.randint(0, 59)

'''
for i in mono_lst:
    print(i)
    jtalk.jtalk(i)
    time.sleep(3)
for i in mng_lst:
    print(i)
    jtalk.jtalk(i)
    time.sleep(1)
for i in evg_lst:
    print(i)
    jtalk.jtalk(i)
    time.sleep(1)
'''
# カメラ初期化
with picamera.PiCamera() as camera:
    # カメラの画像をリアルタイムで取得するための処理
    with picamera.array.PiRGBArray(camera) as stream:
        # 解像度の設定
        camera.resolution = (512, 384)
        # 顔検出のための学習元データを読み込む
        face_cascade = cv.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
        # 目検出のための学習元データを読み込む
        eye_cascade = cv.CascadeClassifier('haarcascades/haarcascade_eye.xml')
        # 体検出のための学習元データを読み込む
        body_cascade = cv.CascadeClassifier('haarcascades/haarcascade_fullbody.xml')
        # 上半身検出のための学習元データを読み込む
        upperbody_cascade = cv.CascadeClassifier('haarcascades/haarcascade_upperbody.xml')
        # 下半身検出のための学習元データを読み込む
        lowerbody_cascade = cv.CascadeClassifier('haarcascades/haarcascade_lowerbody.xml')

        while True:
            # カメラから映像を取得する（OpenCVへ渡すために、各ピクセルの色の並びをBGRの順番にする）
            camera.capture(stream, 'bgr', use_video_port=True)
            # 顔検出の処理効率化のために、写真の情報量を落とす（モノクロにする）
            grayimg = cv.cvtColor(stream.array, cv.COLOR_BGR2GRAY)

#            # 顔検出を行う
#            facerect = face_cascade.detectMultiScale(grayimg, scaleFactor=1.2, minNeighbors=2, minSize=(100, 100))
            # 目検出を行う
            cv.rectangle(stream.array, (100,70), (400,300), (0, 0, 255), 2)
            eye_grayimg = grayimg[70:300, 100:400]
            eyerect = eye_cascade.detectMultiScale(eye_grayimg, minNeighbors=6, minSize=(20,20))
#            eyerect = eye_cascade.detectMultiScale(grayimg, minNeighbors=6)
#            # 体検出を行う
#            bodyrect = body_cascade.detectMultiScale(grayimg, scaleFactor=1.1, minNeighbors=3, minSize=(40,40))
            # 上半身検出を行う
            upperbodyrect = upperbody_cascade.detectMultiScale(grayimg, scaleFactor=1.1, minNeighbors=3, minSize=(40,40))
#            # 下半身検出を行う
#            lowerbodyrect = lowerbody_cascade.detectMultiScale(grayimg, scaleFactor=1.1, minNeighbors=3, minSize=(40,40))

#            # 顔が検出された場合
#            if len(facerect) > 0:
#                # 検出した場所すべてに赤色で枠を描画する
#                for rect in facerect:
#                    cv.rectangle(stream.array, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0, 255), thickness=3)

            # 目を検出した場合
            if len(eyerect) > 0:
                # 検出した場所すべてに緑色で枠を描画する
                for rect in eyerect:
                    cv.rectangle(stream.array, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 255, 0), thickness=3)

#            # 体を検出した場合
#            if len(bodyrect) > 0:
#                # 検出した場所すべてに緑色で枠を描画する
#                for rect in bodyrect:
#                    cv.rectangle(stream.array, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (255, 0, 0), thickness=3)

            # 上半身を検出した場合
            if len(upperbodyrect) > 0:
                # 検出した場所すべてに緑色で枠を描画する
                for rect in upperbodyrect:
                    cv.rectangle(stream.array, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (255, 0, 0), thickness=3)

#            # 下半身を検出した場合
#            if len(lowerbodyrect) > 0:
#                # 検出した場所すべてに緑色で枠を描画する
#                for rect in lowerbodyrect:
#                    cv.rectangle(stream.array, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (255, 0, 0), thickness=3)

            # 結果の画像を表示する
#            cv.imshow('camera', stream.array)
            img_resize = cv.resize(stream.array, (100, 100))
            cv.imshow("camera", img_resize)
            cv.moveWindow("camera", 0, 300) 
#
#            # 顔か目を検出したら挨拶
#            if len(facerect) > 0 or len(eyerect) > 1:
            # 体を検出したら挨拶
#            if len(bodyrect) > 0 or len(upperbodyrect) > 0 or len(lowerbodyrect) > 0:
#            if len(bodyrect) > 0 or len(upperbodyrect) > 0:
            if len(eyerect) > 1 or len(upperbodyrect) > 0:
                if (time.time() - t_st) > 5:
                    #前回から5秒以上経過していたら挨拶
                    try:
                        idleProc.stdin.write("q")
                    except IOError as e:
                        print("Handle error")

                    cmd = "exec omxplayer 受付.mp4"
                    proc = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE)
                    d = datetime.now()
                    rnd = random.randint(0, 40)
                    print(rnd)
                    if (d.hour > 5) and (d.hour < 12):
                        if rnd > (len(mng_lst) - 1):
                            jtalk.jtalk(morning)
                        else:
                            jtalk.jtalk(mng_lst[rnd])
                    else:
                        if rnd > (len(evg_lst) - 1):
                            jtalk.jtalk(evening)
                        else:
                            jtalk.jtalk(evg_lst[rnd])

#                    proc.kill()
                    time.sleep(3)
                    try:
                        proc.stdin.write("q")
                    except IOError as e:
                        print("Handle error")

                    #アイドル動画をループ再生
                    cmd = "exec omxplayer --loop アイドル.mp4"
                    idleProc = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE)

                    t_st = time.time()
#                    # 初期位置がずれていたときの補正
#                    cv.moveWindow("M's Aisatsu Unit", -35, -3) 

            # 現在時刻読み込み
            d = datetime.now()
            if d.hour == nxt_h and d.minute == nxt_m:
                try:
                    idleProc.stdin.write("q")
                except IOError as e:
                    print("Handle error")
                cmd = "omxplayer 受付.mp4"
                proc = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE)
                jtalk.jtalk(mono_lst[random.randint(0, len(mono_lst) - 1)])
#                proc.kill()
                time.sleep(3)
                try:
                    proc.stdin.write("q")
                except IOError as e:
                    print("Handle error")
                #アイドル動画をループ再生
                cmd = "exec omxplayer --loop アイドル.mp4"
                idleProc = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE)

                nxt_h = d.hour + 1
                nxt_m = random.randint(0, 59)
                print(nxt_h, nxt_m)

            # カメラから読み込んだ映像を破棄する
            stream.seek(0)
            stream.truncate()
            
            # 何かキーが押されたかどうかを検出する（検出のため、1ミリ秒待つ）
            if cv.waitKey(1) > 0:
                break

        # 表示したウィンドウを閉じる
        cv.destroyAllWindows()
