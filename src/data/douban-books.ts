export interface DoubanBook {
  title: string;
  author: string;
  category: string;
}

export interface DoubanBookList {
  id: string;
  title: string;
  source: string;
  author: string;
  description: string;
  books: DoubanBook[];
}

export const doubanBookLists: DoubanBookList[] = [
  {
    id: 'zyt-reads',
    title: '张一鸣豆瓣标记读物',
    source: '微信读书',
    author: '张一鸣',
    description: '字节跳动创始人张一鸣在豆瓣标记过的书单，涵盖商业管理、个人成长、技术、文学等多个领域。',
    books: [
      // 商业/管理
      { title: '道路与梦想：我与万科（1983-1999）', author: '王石', category: '商业' },
      { title: '野蛮生长', author: '冯仑', category: '商业' },
      { title: '联想风云', author: '凌志军', category: '商业' },
      { title: '激荡三十年：中国企业1978~2008（上）', author: '吴晓波', category: '商业' },
      { title: '赢（尊享版）', author: '杰克·韦尔奇、苏茜·韦尔奇', category: '商业' },
      { title: '思科风暴', author: '罗伯特·斯莱特', category: '商业' },
      { title: '世界因你不同：李开复自传', author: '李开复、范海涛', category: '商业' },
      { title: '给你一个亿你能干什么？', author: '查立', category: '商业' },
      { title: '3G资本帝国', author: '克里斯蒂娜·柯利娅', category: '商业' },
      { title: '卓有成效的管理者', author: '彼得·德鲁克', category: '商业' },
      { title: '浪潮之巅（第2版）', author: '吴军', category: '商业' },
      { title: '沸腾十五年', author: '林军', category: '商业' },
      // 个人成长/心理学
      { title: '高效能人士的七个习惯', author: '史蒂芬·柯维', category: '个人成长' },
      { title: '影响力', author: '罗伯特·西奥迪尼', category: '个人成长' },
      { title: '少有人走的路：心智成熟的旅程', author: 'M. 斯科特·派克', category: '个人成长' },
      { title: '把时间当作朋友（第3版）', author: '李笑来', category: '个人成长' },
      { title: '别做正常的傻瓜', author: '王婷婷', category: '个人成长' },
      { title: '掌控注意力——打败分心与焦虑', author: '露西·乔·帕拉迪诺', category: '个人成长' },
      { title: '注意力：专注的科学与训练', author: '让-菲利普·拉夏', category: '个人成长' },
      { title: 'A Sense of Urgency', author: 'John P. Kotter', category: '个人成长' },
      { title: '伟大的博弈', author: '约翰·S·戈登', category: '个人成长' },
      // 文学
      { title: '笑傲江湖', author: '金庸', category: '文学' },
      { title: '鹿鼎记', author: '金庸', category: '文学' },
      { title: '连城诀', author: '金庸', category: '文学' },
      { title: '围城', author: '钱钟书', category: '文学' },
      { title: '万历十五年', author: '黄仁宇', category: '文学' },
      // 技术
      { title: 'UNIX环境高级编程（第3版）', author: 'W. 理查德·史蒂文斯、史蒂芬·A. 拉戈', category: '技术' },
      { title: '离散数学及其应用（原书第8版）', author: '肯尼思·H. 罗森', category: '技术' },
      { title: 'MySQL性能调优与架构设计', author: '简朝阳', category: '技术' },
      { title: 'Facebook效应', author: '大卫·柯克帕特里克', category: '技术' },
      // 其他
      { title: '在北大听讲座大全集', author: '刘国生', category: '其他' },
      { title: '身体语言密码', author: '哈里·巴尔肯', category: '其他' },
      { title: '无痛一身轻', author: '戴维斯', category: '其他' },
      { title: '网络江湖三十六计', author: '程苓峰、王晶', category: '其他' },
      { title: '疯狂的站长', author: '温世豪', category: '其他' },
      { title: '谈判：如何在博弈中获得更多', author: '盖温·肯尼迪', category: '其他' },
      { title: 'The Five Dysfunctions of a Team', author: 'Patrick M. Lencioni', category: '其他' },
      { title: '如何阅读一本书', author: '莫提默·艾德勒、查尔斯·范多伦', category: '其他' },
      { title: '断舍离', author: '山下英子', category: '其他' },
    ],
  },
];
