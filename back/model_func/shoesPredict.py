import os
import sys
# 获取项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
# print(project_root)
# 将项目根目录添加到 sys.path
sys.path.append(project_root)
import torch
import argparse
import torchvision
from model_func.test import test,test2
import time
from datasets import Shoes,FashionIQ
from PIL import Image
from model import collative_model
from model_func.utils import LogCollector
from test_ensemble import test_en
def load_dataset_eval(args):
    """Loads the input datasets."""
    print('Reading dataset ', args.dataset)
    if args.dataset == 'fashioniq':
        testset = FashionIQ(
            path = args.data_path,
            name = args.name,
            test_img_name=args.test_img_name,
            test_txt_name=args.test_txt_name,
            split = 'val',
            transform=torchvision.transforms.Compose([
                torchvision.transforms.Resize(256),
                torchvision.transforms.CenterCrop(224),
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize([0.485, 0.456, 0.406],
                                                 [0.229, 0.224, 0.225])
            ]))
    elif args.dataset == 'shoes':
        testset = Shoes(
            path = args.data_path,
            split = 'test',
            test_img_name=args.test_img_name,
            test_txt_name=args.test_txt_name,
            transform=torchvision.transforms.Compose([
                torchvision.transforms.Resize(256),
                torchvision.transforms.CenterCrop(224),
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize([0.485, 0.456, 0.406],
                                                 [0.229, 0.224, 0.225])
            ]))
    else:
        print('Invalid dataset', args.dataset)
        sys.exit()
    # print('testset size:', len(testset))
    return testset
def predictImage(params):
    """
    根据传入的参数进行图像预测。
    
    参数:
    params (dict): 包含以下键值对的字典：
        - 'dataset': 数据集名称
        - 'model': 模型名称（model1, model2, model3）
    """
    print(params)
    # 解析传入的参数
    dataset = params.get('dataset', 'shoes')  # 默认数据集为 'shoes'
    model_name = params.get('model', 'model1')  # 默认模型为 'model1'
    if dataset=='shoes':

        # 定义 model_dir 字典
        model_dir_dict = {
            'model1': 'model/shoes/AMC_sim_0',
            'model2': 'model/shoes/AMC_sim_1',
            'model3': ['model/shoes/AMC_sim_0', 'model/shoes/AMC_sim_1']  # model3 使用两个路径
            
        }
        
        # 获取项目根目录
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        # 动态生成 data_path
        data_path = os.path.join(project_root, 'data', dataset)
        
        # 根据 model_name 选择 model_dir
        if model_name in model_dir_dict:
            model_dir = model_dir_dict[model_name]
        else:
            raise ValueError(f"未知的模型名称: {model_name}")
        
        # 设置 argparse 参数
        parser = argparse.ArgumentParser()
        parser.add_argument('--dataset', default=dataset, help="数据集名称")
        parser.add_argument('--name', default='dress', help="数据集")
        parser.add_argument('--data_path', default=data_path, help="数据集路径")
        parser.add_argument('--batch_size', type=int, default=32, help="批量大小")
        parser.add_argument('--test_img_name',default=params.get('image_name'),help="上传图片文件的名称，方便检索")
        parser.add_argument('--test_txt_name',default=params.get('test_txt_name'),help="文本文件名称")
        # 根据 model_name 设置 model_dir 参数
        if model_name == 'model3':
            # model3 使用两个路径
            parser.add_argument('--model_dir1', default=os.path.join(project_root, model_dir[0]))
            parser.add_argument('--model_dir2', default=os.path.join(project_root, model_dir[1]))
        else:
            # model1 和 model2 使用单个路径
            parser.add_argument('--model_dir', default=os.path.join(project_root, model_dir))
        
        opt = parser.parse_args()
        
        # 加载模型
        if model_name == 'model3':
            # model3 加载两个模型
            first_model_path = os.path.join(opt.model_dir1, 'train_model.pt')
            second_model_path = os.path.join(opt.model_dir2, 'train_model.pt')
            model1 = torch.load(first_model_path)
            model2 = torch.load(second_model_path)
            # 这里可以根据需要合并或使用两个模型
        else:
            # model1 和 model2 加载单个模型
            model_path = os.path.join(opt.model_dir, 'train_model.pt')
            model = torch.load(model_path)
        
        # 加载数据集
        testset = load_dataset_eval(opt)
        print('-'*50)
        print("data dir",opt.data_path)
        # print("model dir",opt.model_dir)
        print('input img file',opt.test_img_name)
        print("input text caption file",opt.test_txt_name)
        
        # 进行测试
        if model_name in ['model1', 'model2']:
            print(f'-----------------------{opt.model_dir}----------------------------')
            # 对于 model1 和 model2，调用 test 函数
            pic_paths = test(opt, model, testset, opt.dataset)
        elif model_name == 'model3':
            print(f'-----------------------{opt.model_dir1}----------------------------')
            print(f'-----------------------{opt.model_dir2}----------------------------')
            # 对于 model3，调用 test_en 函数
            pic_paths = test_en(opt, model1, model2, testset, opt.dataset)
        # print(pic_paths)
        
        # 读取第一个路径下的图片
        first_image_path = pic_paths[0][0]
        try:
            img1 = Image.open(first_image_path)
        except IOError:
            print("图片读取失败，请检查路径是否正确！")
        
        return img1
    elif dataset=='fashioniq':
       # 获取项目根目录
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        # 动态生成 data_path
        data_path = os.path.join(project_root, 'data', dataset+'/')

        model_path = os.path.join(project_root,"model/fashioniq",params.get('model'))
        # print(f'project_root:{project_root}')
        # print(f"model path:{model_path}")
        # print(f"data-path:{data_path}")
        parser = argparse.ArgumentParser()
        parser.add_argument('--dataset', default = 'fashioniq', help = "data set type")
        
        parser.add_argument('--name', default = params.get('model'), help = "data set type")
        parser.add_argument('--data_path', default = data_path)
        parser.add_argument('--model_dir',default = model_path)
        parser.add_argument('--batch_size', type=int, default=32)
        parser.add_argument('--test_img_name',default=params.get('image_name'),help="上传图片文件的名称，方便检索")
        parser.add_argument('--test_txt_name',default=params.get('test_txt_name'),help="文本文件名称")
        opt = parser.parse_args()
        model_path = os.path.join(opt.model_dir,'train_model.pt')
        model = torch.load(model_path)

        testset = load_dataset_eval(opt)
        print('-'*50)
        print("data dir",opt.data_path)
        print("model dir",opt.model_dir)
        print('input img file',opt.test_img_name)
        print("input text caption file",opt.test_txt_name)
        t = test2(opt, model, testset, opt.dataset)
        first_image_path=t[0]
        # print(first_image_path)
        # print(t)
        try:
            img1 = Image.open(first_image_path)
        except IOError:
            print("图片读取失败，请检查路径是否正确！")
        return img1
def predictImage_test(params):
    return Image.open(params.get('image_file'))