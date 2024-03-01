from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.models import load_model
import zipfile , os , random
# from main import app
class_names = ['1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '21', '22', '23', '24', '3', '4', '5', '6', '7', '8', '9']
try :
    model = load_model("..\\functions\\best_weights_resnet_2024-03-01 (1).h5") 
    # model = load_model("..\\functions\\best_weights_resnet.h5")

except:
    print("File not found")

def predict_images(file_names , model = model ):
    images = []
    for file in file_names :
        img = Image.open(file)
        img = img.resize((100, 100 ))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_array = keras_image.img_to_array(img)
        
        img_array /= 255.0
        img_array = np.expand_dims(img_array, axis=0)
        print("img_arr : " , img_array )

        pred = class_names[model.predict(img_array).argmax()]
        images.append([ file , pred ])
    save_img(images)
    return "Done"
    
def save_img(files) :
    dict_ = { i : 0 for i in range(1 ,25)}
    base = "..\\uploads"
    for file , class_ in files :
        print("class : " , class_)
        dict_[class_] += 1
        file_path = os.path.join(base , "chromo", file)
        zip_file_path = os.path.join(base , 'chromosomes.zip')

        # Zip the folder
        print(file , file_path , zip_file_path)
        with zipfile.ZipFile(zip_file_path, 'a', zipfile.ZIP_DEFLATED) as zipf:
            # Add the file to the zip archive
            arcname=os.path.join('chromosomes', str(int(class_) + 1), os.path.basename(file))
            print(arcname)
            zipf.write(file, arcname = arcname )
            print(f"{file}..Done")
    
    print("Total_count" , dict_)

# base = "..\\uploads"
# predictions = predict_images([ f"{base}\\chromo\\dragonstone.jpg" , f"{base}\\chromo\\hi.jpg"])

# print(f"chr{predictions}")
# base = "..\\uploads\\chromosomes"
# lst_ = [f"{base}\\{i}" for i in range(1 , 25)]
# os.makedirs(base)
# for i in lst_:
#     if not os.path.exists(i) :
#         os.makedirs(i)

def make_preds(model , n : int) :
    base = "D:\\here\\single_chromosomes"
    lst_ = [f"{base}\\{i}" for i in range(1 , 25)]
    j = 1
    for i in lst_ : 
        dct = dict()
        images = []
        for dir_ , _ , files in os.walk(i) :
            images.extend(random.sample( files, min(n, len(files))))
        for file in images :
            img = Image.open(os.path.join(i , file))
            img = img.resize((100, 100 ))
            if img.mode != 'RGB' :
                img = img.convert('RGB')
            img_array = keras_image.img_to_array(img)
            
            img_array /= 255.0
            img_array = np.expand_dims(img_array, axis=0)
            prediction = class_names[model.predict(img_array , verbose = 0).argmax()]
            if prediction not in dct :
                dct[prediction] = 1
            else :
                dct[prediction] += 1
        print(f"preds {j}: " , dct)
        j += 1

make_preds(model , 4)

    
