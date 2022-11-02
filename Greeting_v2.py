# -*- coding: utf-8 -*-
import os, sys, errno
import signal
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
           'ひれふせっ　にんげんっ',
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
           'おうおうおうおうおうー',
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
           'ひでぶっ',
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
           'くそがっ',
           'ぎゅー']
t_st = 0

img = cv.imread('受付_Idle.jpg')
#cv.namedWindow("M's Aisatsu Unit", cv.WINDOW_NORMAL)
#cv.setWindowProperty("M's Aisatsu Unit", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
#cv.imshow("M's Aisatsu Unit", img)
img_resize = cv.resize(img, (430,630))
cv.imshow("M's Aisatsu Unit", img_resize)
cv.moveWindow("M's Aisatsu Unit", -10, -30) 

#アイドル動画をループ再生
#cmd = "exec omxplayer --loop アイドル.mp4"
#idleProc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
#time.sleep(3)

jtalk.jtalk('えむず　あいさつユニット　しどうっ')
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

            # 目検出を行う
            eye_grayimg = grayimg[70:300, 100:400]
            eyerect = eye_cascade.detectMultiScale(eye_grayimg, minNeighbors=6, minSize=(20,20))
            # 上半身検出を行う
            upperbodyrect = upperbody_cascade.detectMultiScale(grayimg, scaleFactor=1.1, minNeighbors=3, minSize=(40,40))

            # 目を検出した場合
            if len(eyerect) > 0:
                # 検出した場所すべてに緑色で枠を描画する
                for rect in eyerect:
                    cv.rectangle(stream.array, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 255, 0), thickness=3)

            # 上半身を検出した場合
            if len(upperbodyrect) > 0:
                # 検出した場所すべてに緑色で枠を描画する
                for rect in upperbodyrect:
                    cv.rectangle(stream.array, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (255, 0, 0), thickness=3)

            # 結果の画像を表示する
            cv.imshow('camera', stream.array)
            img_resize = cv.resize(stream.array, (100, 100))
            cv.imshow("camera", img_resize)
            cv.moveWindow("camera", 0, 300) 

            # 体か目を検出したら挨拶
            if len(eyerect) > 1 or len(upperbodyrect) > 0:
                print("eyrect=",len(eyerect),"upperbodyrect=",len(upperbodyrect))
                #前回から5秒以上経過していたら挨拶
                if (time.time() - t_st) > 5:
#                    #アイドル動画停止
#                    os.killpg(os.getpgid(idleProc.pid), signal.SIGTERM)
                    #挨拶動画再生
                    cmd = "exec omxplayer 受付.mp4"
                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
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
                    time.sleep(3)
                    #挨拶動画停止
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
#                    #アイドル動画再起動
#                    cmd = "exec omxplayer --loop アイドル.mp4"
#                    idleProc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
#                    time.sleep(3)

                    # 初期位置がずれていたときの補正
                    cv.moveWindow("M's Aisatsu Unit", -10, -30) 

                    t_st = time.time()

            # 現在時刻読み込み
            d = datetime.now()
            if d.hour == nxt_h and d.minute == nxt_m:
#                #アイドル動画停止
#                os.killpg(os.getpgid(idleProc.pid), signal.SIGTERM)
                #挨拶動画再生
                cmd = "omxplayer 受付.mp4"
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
                jtalk.jtalk(mono_lst[random.randint(0, len(mono_lst) - 1)])
                time.sleep(3)
                #挨拶動画停止
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
#                #アイドル動画再起動
#                cmd = "exec omxplayer --loop アイドル.mp4"
#                idleProc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
#                time.sleep(3)

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
