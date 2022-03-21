pip install wldhx.yadisk-direct

mkdir data
mkdir data/video_defects
mkdir data/video_original
mkdir data/images
mkdir data/masks
mkdir data/defects

curl -L $(yadisk-direct https://disk.yandex.ru/d/4qNNox1GEqbfZQ) -o ./data/defects.zip
unzip  ./data/defects.zip -d data/video_defects
rm ./data/defects.zip

curl -L $(yadisk-direct https://disk.yandex.ru/i/jNm5Yyh7ymUnMQ) -o ./data/video_original/film_1.mp4
curl -L $(yadisk-direct https://disk.yandex.ru/i/khqcMg8MmSxjGQ) -o ./data/video_original/film_2.mp4

