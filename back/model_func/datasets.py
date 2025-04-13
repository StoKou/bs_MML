import os
import numpy as np
import PIL
import torch
import json
import torch.utils.data
import glob
import random
import torchvision

class Shoes(torch.utils.data.Dataset):

    def __init__(self, path, test_img_name,test_txt_name,split='train', existed_npy=False, transform=None):
        super(Shoes, self).__init__()
        self.transform = transform
        self.path = path

        self.readpath = 'relative_captions_shoes.json'
        self.existed_npy = existed_npy
        if split == 'train':
            textfile = 'train_im_names.txt'

        elif split == 'test':
            textfile = 'eval_im_names.txt'

        with open(os.path.join(self.path, self.readpath)) as handle:
            self.dictdump = json.loads(handle.read())

        text_file = open(os.path.join(self.path, textfile), 'r')
        imgnames = text_file.readlines()
        imgnames = [imgname.strip('\n') for imgname in imgnames]
        img_path = os.path.join(self.path, 'attributedata')

        self.imgfolder = os.listdir(img_path)
        self.imgfolder = [self.imgfolder[i] for i in range(len(self.imgfolder)) if 'womens' in self.imgfolder[i]]

        ###########################
        if not self.existed_npy:
            self.imgimages_all = []
            for i in range(len(self.imgfolder)):
                path = os.path.join(img_path, self.imgfolder[i])
                imgfiles = [f for f in glob.glob(path + "/*/*.jpg", recursive=True)]
                self.imgimages_all += imgfiles
        else:
            self.imgimages_all = np.load(os.path.join(self.path, 'imgimages_all.npy'), allow_pickle=True).tolist()

        self.imgs = self.imgimages_all
        self.imgimages_raw = [os.path.basename(imgname) for imgname in self.imgimages_all]
        self.test_img_name=test_img_name
        self.test_txt_name=test_txt_name
        self.test_targets = []
        self.test_queries = []

        #############################
        # 我觉得不需要下面的代码， 暂时注释
        # if not self.existed_npy:
        #     self.relative_pairs = self.get_relative_pairs(self.dictdump, imgnames, self.imgimages_all, self.imgimages_raw)
        # else:
        #     if split == 'train':
        #         self.relative_pairs = np.load(os.path.join(self.path, 'relative_pairs_train.npy'), allow_pickle=True).tolist()
        #     elif split == 'test':
        #         self.relative_pairs = np.load(os.path.join(self.path, 'relative_pairs_test.npy'), allow_pickle=True).tolist()

    # 从输入数据中提取图像对（source 和 target）及其对应的描述文本（caption），并返回一个包含这些信息的列表。
    def get_relative_pairs(self, dictdump, imgnames, imgimages_all, imgimages_raw):
        relative_pairs = []
        for i in range(len(imgnames)):
            ind = [k for k in range(len(dictdump))
                    if dictdump[k]['ImageName'] == imgnames[i]
                    or dictdump[k]['ReferenceImageName'] == imgnames[i]]
            for k in ind:
                if imgnames[i] == dictdump[k]['ImageName']:
                    target_imagename = imgimages_all[imgimages_raw.index(
                        imgnames[i])]
                    source_imagename = imgimages_all[imgimages_raw.index(
                        dictdump[k]['ReferenceImageName'])]
                else:
                    source_imagename = imgimages_all[imgimages_raw.index(
                        imgnames[i])]
                    target_imagename = imgimages_all[imgimages_raw.index(
                        dictdump[k]['ImageName'])]
                text = dictdump[k]['RelativeCaption'].strip()
                relative_pairs.append({
                    'source': source_imagename,
                    'target': target_imagename,
                    'mod': text
                })
        return relative_pairs

    def __len__(self):
        return len(self.relative_pairs)
  
    
    def __getitem__(self, idx):

        caption = self.relative_pairs[idx]
        out = {}
        out['source_img_data'] = self.get_img(caption['source'])
        out['target_img_data'] = self.get_img(caption['target'])
        out['mod'] = {'str': caption['mod']}

        return out

    def get_img(self, img_path):
        with open(img_path, 'rb') as f:
            img = PIL.Image.open(f)
            img = img.convert('RGB')
        if self.transform:
            img = self.transform(img)
        return img

    def get_img1(self, img_path):
        with open(img_path, 'rb') as f:
            img = PIL.Image.open(f)
            img = img.convert('RGB')
        return img

    def get_all_texts(self):
        if not self.existed_npy:
            text_file = open(os.path.join(self.path, 'train_im_names.txt'),'r')
            imgnames = text_file.readlines()
            imgnames = [imgname.strip('\n') for imgname in imgnames] # img_womens_athletic_shoes_1.txt list
            train_relative_pairs = self.get_relative_pairs(self.dictdump, imgnames, self.imgimages_all, self.imgimages_raw)
            texts = []
            for caption in train_relative_pairs:
                mod_texts = caption['mod']
                texts.append(mod_texts)
        else:
            texts = np.load(os.path.join(self.path, 'all_texts.npy'), allow_pickle=True).tolist()
        return texts

    def get_test_queries(self):       # query
        self.test_queries = []
        # 涉及到路径修改问题
        test_img_path = os.path.join(self.path, '..', '..', 'uploads')

        txt_path = os.path.join(test_img_path,self.test_txt_name)
        
        # 读取txt文件内容
        with open(txt_path, 'r', encoding='utf-8') as file:
            caption = file.read()  # 读取文件的全部内容
        print(f"txt_path:{txt_path} caption:{caption}")
        # print(f"\n验证读取图片是否正确：{self.imgimages_all[0]} {self.test_img_name}\n")
        jpg_path=os.path.join(test_img_path,self.test_img_name)
        # print(f"jpg path:{jpg_path}")
        mod_str = caption
        out = {}
        out['source_img_id'] = 1
        out['source_img_data'] = self.get_img(jpg_path)
        out['source_img'] = self.get_img1(jpg_path)
        out['target_img_id'] = 0
        out['target_img_data'] = self.get_img(jpg_path)
        out['target_img'] = self.get_img1(jpg_path)
        out['mod'] = {'str': mod_str}
        self.test_queries.append(out)
        return self.test_queries

    def get_test_targets(self):     
        text_file = open(os.path.join(self.path, 'eval_im_names.txt'),'r')
        # text_file = open(os.path.join(self.path, 'train_im_names.txt'),'r')
        imgnames = text_file.readlines()
        imgnames = [imgname.strip('\n') for imgname in imgnames] # img_womens_athletic_shoes_1.txt list
        self.test_targets = []
        for i in imgnames:
            out = {}
            out['target_img_id'] = self.imgimages_raw.index(i)
            out['target_img_data'] = self.get_img(self.imgimages_all[self.imgimages_raw.index(i)])
            self.test_targets.append(out)
        return self.test_targets


class FashionIQ(torch.utils.data.Dataset):
    def __init__(self, path, test_img_name,test_txt_name,gallery_all=True, name = 'dress',split = 'train',transform=None):
        super(FashionIQ, self).__init__()

        self.path = path
        self.image_dir = self.path + 'images'
        self.split_dir = self.path + 'image_splits'
        self.caption_dir = self.path + 'captions'
        self.name = name
        self.split = split
        self.transform = transform
        self.gallery_all = gallery_all
        self.test_img_name=test_img_name
        self.test_txt_name=test_txt_name
        self.test_targets = []
        self.test_queries = []

        # 不同系统路径有差异，下面代码用于检测
        # caption_path = os.path.join(self.caption_dir, "cap.{}.{}.json".format(self.name, self.split))
        # print("Caption path:", caption_path)
        with open(os.path.join(self.caption_dir, "cap.{}.{}.json".format(self.name, self.split)), 'r') as f:
            self.ref_captions = json.load(f)
        with open(os.path.join(self.split_dir, "split.{}.{}.json".format(self.name, self.split)), 'r') as f:
            self.images = json.load(f)

    def concat_text(self, captions):
        text = "<BOS> {} <AND> {} <EOS>".format(captions[0], captions[1])
        return text

    def __len__(self):
        return len(self.ref_captions)


    def __getitem__(self, idx):
        caption = self.ref_captions[idx]
        mod_str = self.concat_text(caption['captions'])
        candidate = caption['candidate']
        target = caption['target']

        out = {}
        out['source_img_data'] = self.get_img(candidate)
        out['target_img_data'] = self.get_img(target)
        out['mod'] = {'str': mod_str}

        return out

    # def get_img(self,image_name):
    #     img_path = os.path.join(self.image_dir,self.name,image_name + ".jpg")
    #     with open(img_path, 'rb') as f:
    #         img_womens_athletic_shoes_1.txt = PIL.Image.open(f)
    #         img_womens_athletic_shoes_1.txt = img_womens_athletic_shoes_1.txt.convert('RGB')
    #
    #     if self.transform:
    #         img_womens_athletic_shoes_1.txt = self.transform(img_womens_athletic_shoes_1.txt)
    #     return img_womens_athletic_shoes_1.txt
    from PIL import Image as PIL

    def get_img(self, image_name):
        img_path = os.path.join(self.image_dir, self.name, image_name + ".jpg")
        try:
            with open(img_path, 'rb') as f:
                img = PIL.Image.open(f)
                img = img.convert('RGB')

            if self.transform:
                img = self.transform(img)
        except (IOError, FileNotFoundError) as e:
            # 如果在打开或处理图片时发生错误，打印错误信息并返回None
            # print(f"Error opening or processing image {img_path}: {e}")
            return None
        return img
    # def get_img1(self,image_name):
    #     img_path = os.path.join(self.image_dir,self.name,image_name + ".jpg")
    #     img_path = img_path.replace("\\", "/")
    #     with open(img_path, 'rb') as f:
    #         img_womens_athletic_shoes_1.txt = PIL.Image.open(f)
    #         img_womens_athletic_shoes_1.txt = img_womens_athletic_shoes_1.txt.convert('RGB')
    #     return img_womens_athletic_shoes_1.txt
    from PIL import Image as PIL
    def get_img1(self, image_name):
        img_path = os.path.join(self.image_dir, self.name, image_name + ".jpg")
        try:
            with open(img_path, 'rb') as f:
                img = PIL.Image.open(f)
                img = img.convert('RGB')
        except (IOError, FileNotFoundError) as e:
            # 如果在打开或处理图片时发生错误，打印错误信息并返回None
            # print(f"Error opening or processing image {img_path}: {e}")
            return None
        return img
    def get_all_texts(self):
        texts = []
        with open(os.path.join(self.caption_dir, "cap.{}.{}.json".format(self.name, 'train')), 'r') as f:
            train_captions = json.load(f)
        for caption in train_captions:
            mod_texts = caption['captions']
            texts.append(mod_texts[0])
            texts.append(mod_texts[1])
        return texts

    # def get_test_queries(self):       # query
    #     self.test_queries = []
    #     for idx in range(len(self.ref_captions)):
    #         caption = self.ref_captions[idx]
    #         mod_str = self.concat_text(caption['captions'])
    #         candidate = caption['candidate']
    #         target = caption['target']
    #         out = {}
    #         out['source_img_id'] = self.images.index(candidate)
    #         out['source_img'] = self.get_img1(candidate)
    #         out['source_img_data'] = self.get_img(candidate)
    #         out['target_img_id'] = self.images.index(target)
    #         out['target_img_data'] = self.get_img(target)
    #         out['target_img'] = self.get_img1(target)
    #         out['mod'] = {'str': mod_str}
    #
    #         self.test_queries.append(out)
    #
    #     return self.test_queries

    def get_test_queries(self):  # query
        self.test_queries = []
        # 在self.imgfolder路径下搜索txt文件
        # 涉及到路径修改问题
        test_img_path = os.path.join(self.path, '..', '..', 'uploads')

        
        txt_path = os.path.join(test_img_path,self.test_txt_name)
        
        # 读取txt文件内容
        with open(txt_path, 'r', encoding='utf-8') as file:
            caption = file.read()  # 读取文件的全部内容
        # print(f"txt_path:{txt_path} caption:{caption}")
        jpg_files = []

        # print(f"\n验证读取图片是否正确：{self.imgimages_all[0]} {self.test_img_name}\n")
        jpg_path=os.path.join(test_img_path,self.test_img_name)
        # print(f"jpg path:{jpg_path}")

        mod_str = caption
        out = {}

        # 尝试获取source_img_id
        out['source_img_id'] = 0
        # 尝试获取source_img
        out['source_img'] = self.get_img1_2(jpg_path)
        # 尝试获取source_img_data
        out['source_img_data'] = self.get_img_2(jpg_path)
        # 尝试获取target_img_id
        out['target_img_id'] = 1
        # 尝试获取target_img_data
        out['target_img_data'] = self.get_img_2(jpg_path)
        # 尝试获取target_img
        out['target_img'] = self.get_img1_2(jpg_path)
        # 设置mod属性
        out['mod'] = {'str': mod_str}

        self.test_queries.append(out)
        return self.test_queries


    def get_test_targets(self):

        self.test_targets = []
        for idx in range(len(self.images)):
            target = self.images[idx]
            out = {}
            out['target_img_id'] = idx
            img_data = self.get_img(target)  # 先获取图片数据
            if img_data is not None:  # 判断是否为None
                out['target_img_data'] = img_data
                self.test_targets.append(out)  # 如果不是None，才添加到列表中

        return self.test_targets
    def get_img_2(self, img_path):
        with open(img_path, 'rb') as f:
            img = PIL.Image.open(f)
            img = img.convert('RGB')
        if self.transform:
            img = self.transform(img)
        return img

    def get_img1_2(self, img_path):
        with open(img_path, 'rb') as f:
            img = PIL.Image.open(f)
            img = img.convert('RGB')
        return img