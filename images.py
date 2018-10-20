import zipfile


def extract_images(filename):
    z = zipfile.ZipFile(filename)

    #print list of valid attributes for ZipFile object
    print dir(z)

    #print all files in zip archive
    all_files = z.namelist()

    #get all files in word/media/ directory
    images = filter(lambda x: x.startswith('word/media/'), all_files)
    print images

    #open an image and save it
    # image1 = z.open('word/media/image1.jpeg').read()
    # f = open('image1.jpeg','wb')
    # f.write(image1)
    # image2 = z.open('word/media/image2.jpeg').read()
    # f = open('image2.jpeg','wb')
    # f.write(image2)

    for i in range(1, len(images)):
        image_name = 'image{0}.jpeg'.format(i)
        image = z.open('word/media/' + image_name).read()
        f = open(image_name, 'wb')
        f.write(image)
    #Extract file
    # z.extract('word/media/image1.jpeg', r'path_to_dir')