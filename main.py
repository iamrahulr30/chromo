from flask import Flask , render_template , send_file , redirect , url_for
from flask import request
from forms.FilesForm import ImageFolderForm
import os , zipfile
from functions.preprocessing import predict_images


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/' , methods = ["GET" , "POST"])
def main():
    processing = False
    form = ImageFolderForm()
    if form.validate_on_submit():
        image_fold = [file.filename for file in form.image_folder.data]
        files = []
        print("image data" , image_fold )
        for file in form.image_folder.data :
            print("file : " , file)
            image_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], "chromo" , file.filename)
            files.append(image_folder_path)
            file.save(image_folder_path)
        
        print("redirecting..." *  100 , files)
        predict_images(files)
        # processed_result = process_images(image_folder_path)
        processing = True 
        return redirect(url_for('download_folder'))

    return render_template('layout.html', form=form , processing = processing)


@app.route('/download_folder')
def download_folder():
    print("in download folder")

    # folder_path = os.path.join(app.config['UPLOAD_FOLDER'], "chromo")
    zip_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'chromosomes.zip')

    # # Zip the folder
    # with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    #     print("zip : " , zipfile)
    #     for root, dirs, files in os.walk(folder_path):
    #         print("files : " , files)
    #         for file in files:
    #             print("file : " , file )
    #             file_path = os.path.join(root, file)
    #             arcname = os.path.relpath(file_path, folder_path)
    #             zipf.write(file_path, arcname)

    return send_file(zip_file_path, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)

