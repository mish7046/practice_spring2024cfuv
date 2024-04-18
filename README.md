# practice_spring2024cfuv
### что и как
main.py -- сервер. на него отправлять POST-запросы с файлом типа pdf, docx или png/jpg. в ответ приходит json текстом.  
inference.py -- здесь класс-обработчик `TextParser` для работы с текстовыми документами, класс-обработчик `ImageParser` для картинок. Картинки обрабатываются с помощью нейронки YOLO. Веса для нейронки в файле `yolov8s-1503.pt`. `FileParser` смотрит на mime-тип файла и решает, какой обработчик использовать.

### запуск и как попробовать
`uvicorn main:app` - запустит сервер на 127.0.0.1:8000 (порт по умолчанию)  
отправить файл:  
`curl -F "file=@путь_к_файлу" localhost:8000` 
