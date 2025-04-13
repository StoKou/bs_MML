import sys
import numpy as np
import torch
from tqdm import tqdm as tqdm
import torch.nn.functional as F
import time
import os
def test(params, new_model, testset, dataname):
    """Tests a model over the given testset."""
    new_model.eval()
    with torch.no_grad():
        test_queries = testset.get_test_queries()
        test_targets = testset.get_test_targets()
        
        time_a = time.time()
        all_query_glo = []
        all_target_glo = []
        if test_queries:
            # compute test query features
            imgs = []
            mods = []
            for t in tqdm(test_queries):
                imgs += [t['source_img_data']]
                mods += [t['mod']['str']]
                if len(imgs) >= params.batch_size or t is test_queries[-1]:
                    if 'torch' not in str(type(imgs[0])):
                        imgs = [torch.from_numpy(d).float() for d in imgs]
                    imgs = torch.stack(imgs).float().cuda()
                    query_glo = new_model.query_eval(imgs,mods)
                    all_query_glo += [query_glo.data.cpu().numpy()]
                    imgs = []
                    mods = []
                    del query_glo
            all_query_glo = np.concatenate(all_query_glo)

            # compute all image features
            imgs = []
            for t in tqdm(test_targets):
                imgs += [t['target_img_data']]
                if len(imgs) >= params.batch_size or t is test_targets[-1]:
                    if 'torch' not in str(type(imgs[0])):
                        imgs = [torch.from_numpy(d).float() for d in imgs]
                    imgs = torch.stack(imgs).float().cuda()
                    target_glo = new_model.target_eval(imgs)
                    all_target_glo += [target_glo.data.cpu().numpy()]
                    imgs = []
                    del  target_glo
            all_target_glo = np.concatenate(all_target_glo)
        
    # feature normalization
    for i in range(all_query_glo.shape[0]):
        all_query_glo[i, :] /= np.linalg.norm(all_query_glo[i, :])
    for i in range(all_target_glo.shape[0]):
        all_target_glo[i, :] /= np.linalg.norm(all_target_glo[i, :])
    
    
    # match test queries to target images, get nearest neighbors
    sims = all_query_glo.dot(all_target_glo.T)
    
    # test_targets_id = []
    # for i in test_targets:
    #     test_targets_id.append(i['target_img_id'])
    # for i, t in enumerate(test_queries):
    #     sims[i, test_targets_id.index(t['source_img_id'])] = -10e10


    nn_result = [np.argsort(-sims[i, :])[:5] for i in range(sims.shape[0])]

    # 初始化一个列表，用于存储每个样本的前5最相似样本的图片路径
    original_paths = []

    # 遍历nn_result中的每个样本的前50个最相似样本索引
    for nns in nn_result:
        # 对于每个最相似样本的索引，直接从self.imgimages_all中获取对应的图片路径
        original_nns_paths = [testset.imgimages_all[idx] for idx in nns]
        original_paths.append(original_nns_paths)

    return original_paths
def test2(params, new_model, testset, dataname):
    """Tests a model over the given testset."""
    new_model.eval()
    with torch.no_grad():
        test_queries = testset.get_test_queries()
        test_targets = testset.get_test_targets()

        time_a = time.time()
        all_query_glo = []
        all_target_glo = []
        if test_queries:
            # compute test query features
            imgs = []
            mods = []
            for t in tqdm(test_queries):
                imgs += [t['source_img_data']]
                mods += [t['mod']['str']]
                if len(imgs) >= params.batch_size or t is test_queries[-1]:
                    if 'torch' not in str(type(imgs[0])):
                        imgs = [torch.from_numpy(d).float() for d in imgs]
                    imgs = torch.stack(imgs).float().cuda()
                    query_glo = new_model.query_eval(imgs, mods)
                    all_query_glo += [query_glo.data.cpu().numpy()]
                    imgs = []
                    mods = []
                    del query_glo
            all_query_glo = np.concatenate(all_query_glo)

            # compute all image features
            imgs = []
            for t in tqdm(test_targets):
                imgs += [t['target_img_data']]
                if len(imgs) >= params.batch_size or t is test_targets[-1]:
                    if 'torch' not in str(type(imgs[0])):
                        imgs = [torch.from_numpy(d).float() for d in imgs]
                    imgs = torch.stack(imgs).float().cuda()
                    target_glo = new_model.target_eval(imgs)
                    all_target_glo += [target_glo.data.cpu().numpy()]
                    imgs = []
                    del target_glo
            all_target_glo = np.concatenate(all_target_glo)

    # feature normalization
    for i in range(all_query_glo.shape[0]):
        all_query_glo[i, :] /= np.linalg.norm(all_query_glo[i, :])
    for i in range(all_target_glo.shape[0]):
        all_target_glo[i, :] /= np.linalg.norm(all_target_glo[i, :])

    # match test queries to target images, get nearest neighbors
    sims = all_query_glo.dot(all_target_glo.T)

    # test_targets_id = []
    # for i in test_targets:
    #     test_targets_id.append(i['target_img_id'])
    # for i, t in enumerate(test_queries):
    #     sims[i, test_targets_id.index(t['source_img_id'])] = -10e10

    nn_result = [np.argsort(-sims[i, :])[:5] for i in range(sims.shape[0])]

    # 初始化一个列表，用于存储每个样本的前5最相似样本的图片路径
    original_paths = []
    flattened_list = [item for sublist in nn_result for item in sublist]
    # 遍历nn_result中的每个样本的前50个最相似样本索引
    for nns in flattened_list:
        # 对于每个最相似样本的索引，直接从self.images中获取对应的图片路径
        original_nns_paths = testset.images[nns]
        dir = testset.image_dir
        name = testset.name
        path = os.path.join(dir, name,original_nns_paths+".jpg")
        original_paths.append(path)

    return original_paths