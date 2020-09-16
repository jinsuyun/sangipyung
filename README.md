사용법
./darkent detector test /.data경로 /.cfg경로/ /.weights경로/ /입력 이미지 경로/ -out /이미지 저장경로/ -txt /txt 저장 경로/ -dont_show(이미지 안보이게 설정) -gpus 1(GPU 설정) 


-out /저장경로/ : 모델을 돌린 이미지를 저장한다.


-txt /저장경로/ : 이미지에 대한 Object detection의 정보를 저장된 경로에 result.txt 파일로 저장한다.


-gpus num : gpu 설정한다.

예시)
./darknet detector test /mnt/hdd2/darknet/sanjabu/san10_FVL.data /mnt/hdd2/darknet/sanjabu/san10.cfg /mnt/hdd2/darknet/sanjabu/0930train/backup/san10_52000.weights /mnt/hdd2/darknet/sanjabu/201705M02D14H26m58s/CAM_FL/ /mnt/hdd2/darknet/sanjabu/0929/201705M02D14H26m58s_GT/ -out /mnt/hdd2/darknet/sanjabu/1001/out_52000_re -dont_show -gpus 1
