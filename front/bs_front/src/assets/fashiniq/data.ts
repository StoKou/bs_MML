// {
//     "target": "B00BZ8GPVO",
//     "candidate": "B008MTHLHQ",
//     "captions": [
//         "is longer",
//         "is lighter and longer"
//     ]
// }
// // src/assets/show/data.ts
// {
//     "target": "B00BN3RT7U",
//     "candidate": "B008CLTEOW",
//     "captions": [
//         "is darker",
//         "Is a darker grey"
//     ]
// }
// {
//     "target": "B005LUQ0FI",
//     "candidate": "B000FLD4AC",
//     "captions": [
//         "has no sleeves and is light pink",
//         " pink"
//     ]
// }
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
      ImageName: 'B008MTHLHQ.jpg',
      ReferenceImageName: 'B00BZ8GPVO.jpg',
      RelativeCaption: 'is lighter and longer',
      type: 'type1'
    },
    {
      ImageName: 'B008CLTEOW.jpg',
      ReferenceImageName: 'B00BN3RT7U.jpg',
      RelativeCaption: 'Is a darker grey',
      type: 'type1'
    },
    {
      ImageName: 'B000FLD4AC.jpg',
      ReferenceImageName: 'B005LUQ0FI.jpg',
      RelativeCaption: 'has no sleeves and is light pink',
      type: 'type1'
    },
  ]
  
  export default showData
  