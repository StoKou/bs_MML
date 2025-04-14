// src/assets/show/data.ts

// 定义数据类型
interface ShowItem {
  ImageName: string
  ReferenceImageName: string
  RelativeCaption: string
  type: 'type1' | 'type2'
}

// 导出 JSON 数据
const showData: ShowItem[] = [
  {
    ImageName: 'img_womens_clogs_851.jpg',
    ReferenceImageName: 'img_womens_clogs_512.jpg',
    RelativeCaption: 'is more of a textured material',
    type: 'type1'
  },
  {
    ImageName: 'img_womens_high_heels_838.jpg',
    ReferenceImageName: 'img_womens_high_heels_848.jpg',
    RelativeCaption: 'has less strap design',
    type: 'type1'
  },
  {
    ImageName: 'img_womens_sneakers_963.jpg',
    ReferenceImageName: 'img_womens_sneakers_1011.jpg',
    RelativeCaption: 'has silver hoops near the laces',
    type: 'type1'
  },
]

export default showData
