import numpy as np
import torch
from tqdm import tqdm as tqdm
import torch.nn.functional as F

def test_en(params, first_model, second_model, testset, dataname):
    """Tests a model over the given testset."""
    first_model.eval()
    second_model.eval()
    with torch.no_grad():
        test_queries = testset.get_test_queries()
        test_targets = testset.get_test_targets()

        all_queries = []
        all_imgs = []
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
                    f = torch.cat([F.normalize(first_model.query_eval(imgs, mods)), F.normalize(second_model.query_eval(imgs, mods))], dim=1)
                    f = f.data.cpu().numpy()
                    all_queries += [f]
                    imgs = []
                    mods = []
            all_queries = np.concatenate(all_queries)

            # compute all image features
            imgs = []
            logits = []
            for t in tqdm(test_targets):
                imgs += [t['target_img_data']]
                if len(imgs) >= params.batch_size or t is test_targets[-1]:
                    if 'torch' not in str(type(imgs[0])):
                        imgs = [torch.from_numpy(d).float() for d in imgs]
                    imgs = torch.stack(imgs).float().cuda()
                    imgs = torch.cat([F.normalize(first_model.target_eval(imgs)), F.normalize(second_model.target_eval(imgs))], dim=1).data.cpu().numpy()
                    all_imgs += [imgs]
                    imgs = []
            all_imgs = np.concatenate(all_imgs)

    # feature normalization
    for i in range(all_queries.shape[0]):
        all_queries[i, :] /= np.linalg.norm(all_queries[i, :])
    for i in range(all_imgs.shape[0]):
        all_imgs[i, :] /= np.linalg.norm(all_imgs[i, :])

    # match test queries to target images, get nearest neighbors
    sims = all_queries.dot(all_imgs.T)

    nn_result = [np.argsort(-sims[i, :])[:5] for i in range(sims.shape[0])]
    # 初始化一个列表，用于存储每个样本的前5最相似样本的图片路径
    original_paths = []

    # 遍历nn_result中的每个样本的前50个最相似样本索引
    for nns in nn_result:
        # 对于每个最相似样本的索引，直接从self.imgimages_all中获取对应的图片路径
        original_nns_paths = [testset.imgimages_all[idx] for idx in nns]
        original_paths.append(original_nns_paths)

    return original_paths