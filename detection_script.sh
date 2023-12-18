python detect.py --weights leukonychia.pt --conf 0.4 --save-txt --img-size 640 --name leukonychia --source napsi_test_images
python detect.py --weights pitting.pt --conf 0.25 --save-txt --img-size 640 --name pitting --source napsi_test_images
python detect.py --weights redspot.pt --conf 0.8 --save-txt --img-size 640 --name redspot --source napsi_test_images
python detect.py --weights crumbling.pt --conf 0.6 --save-txt --img-size 640 --name crumbling --source napsi_test_images
python detect.py --weights hyperkeratosis.pt --conf 0.6 --save-txt --img-size 640 --name hyperkeratosis --source napsi_test_images
python detect.py --weights splinter.pt --conf 0.5 --save-txt --img-size 640 --name splinter --source napsi_test_images
python detect.py --weights onycholysis.pt --conf 0.45 --save-txt --img-size 640 --name onycholysis --source napsi_test_images
python detect.py --weights oilspot.pt --conf 0.48 --save-txt --img-size 640 --name oilspot --source napsi_test_images
python napsi_calculator_ai.py 
