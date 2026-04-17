export interface Chapter {
  id: string;
  number: number | null;
  title: string;
  titleEn?: string;
  subtitle: string;
  description: string;
  descriptionEn?: string;
  publishDate: string;
  type: 'main' | 'extra' | 'intro';
  pages: number;
  status: 'available' | 'restricted';
  slug: string;
  color: string;
  tags: string[];
}

export const chapters: Chapter[] = [
  {
    id: 'how0',
    number: 0,
    title: '怎样真正活过',
    titleEn: 'How to Truly Live',
    subtitle: 'How to truly live',
    description: 'Lifetime 是一张主题乐园通票，你 always 试图多玩几个园儿。探讨厉害的人与不厉害的人的发育线，以及赚钱的终极意义——给世界端盘儿菜。',
    descriptionEn: 'Lifetime is a theme park pass — you always try to visit more parks. Explore the development paths of the elite and non-elite, and the ultimate meaning of wealth — serving original dishes to the world.',
    publishDate: '2025-07-28',
    type: 'main',
    pages: 14,
    status: 'available',
    slug: 'how0',
    color: '#6366f1',
    tags: ['人生哲学', '厉害/不厉害', '发育线', '端盘儿菜', 'The Passion'],
  },
  {
    id: 'how1',
    number: 1,
    title: '怎样理财',
    titleEn: 'How to Manage Wealth',
    subtitle: 'How to manage wealth',
    description: '从第一桶金到永续财富自由的路径。讨论 W₀（约3000万）的实现逻辑，以及不厉害的人如何通过价值投资实现财务自由。',
    descriptionEn: 'The path from first bucket of gold to perpetual financial freedom. Discusses the logic behind W₀ (~30M RMB) and how the non-elite can achieve financial freedom through value investing.',
    publishDate: '2025-07-24',
    type: 'main',
    pages: 20,
    status: 'available',
    slug: 'how1',
    color: '#10b981',
    tags: ['理财', '投资', 'W₀', '价值投资', '财富自由'],
  },
  {
    id: 'how2',
    number: 2,
    title: '怎样上岸',
    titleEn: 'How to Reach the Shore',
    subtitle: 'How to reach the shore',
    description: '从 W₁ 到 W₂（约3亿）的路径。传与有缘，公众号不贴。',
    descriptionEn: 'The path from W₁ to W₂ (~300M RMB). Restricted content, not publicly posted.',
    publishDate: '2025-07-24',
    type: 'main',
    pages: 0,
    status: 'restricted',
    slug: 'how2',
    color: '#f59e0b',
    tags: ['上岸', 'W₁', 'W₂'],
  },
  {
    id: 'how3',
    number: 3,
    title: '怎样保级',
    titleEn: 'How to Maintain Position',
    subtitle: 'How to maintain your position',
    description: '上岸之后人人都要学的课题。财富的保全不仅仅是投资的问题，更是一种生活方式和认知框架。',
    descriptionEn: 'A mandatory subject after reaching the shore. Wealth preservation is not just an investment issue — it is a lifestyle and cognitive framework.',
    publishDate: '2025-07-24',
    type: 'main',
    pages: 12,
    status: 'available',
    slug: 'how3',
    color: '#3b82f6',
    tags: ['保级', '财富保全', '认知框架', '生活方式'],
  },
  {
    id: 'how4',
    number: 4,
    title: '怎样搞事',
    titleEn: 'How to Make Things Happen',
    subtitle: 'How to make things happen',
    description: '厉害的人的专属课题。从0到1的创业逻辑，梦幻队长理论，以及给世界端盘儿菜的具体路径。',
    descriptionEn: 'The exclusive subject for the elite. The startup logic from 0 to 1, the Dream Captain theory, and the concrete path to serving original dishes to the world.',
    publishDate: '2025-07-24',
    type: 'main',
    pages: 14,
    status: 'available',
    slug: 'how4',
    color: '#ef4444',
    tags: ['创业', '搞事', '梦幻队长', '0到1', '原创贡献'],
  },
  {
    id: 'how5',
    number: 5,
    title: '怎样预测未来',
    titleEn: 'How to Predict the Future',
    subtitle: 'How to predict the future',
    description: '厉害的人的第二专属课题。理解历史规律与技术趋势，在人类知识凸包的前沿做出判断。',
    descriptionEn: "The elite's second exclusive subject. Understanding historical patterns and technological trends, and making judgments at the frontier of humanity's knowledge convex hull.",
    publishDate: '2025-07-24',
    type: 'main',
    pages: 19,
    status: 'available',
    slug: 'how5',
    color: '#8b5cf6',
    tags: ['预测未来', '技术趋势', '历史规律', 'AI', '凸包'],
  },
  {
    id: 'how6',
    number: 6,
    title: '怎样 Anything',
    titleEn: 'How to Do Anything',
    subtitle: 'How to do anything',
    description: '番外篇。二流技术的汇集——怎样失恋、怎样赢、怎样选专业……以及更多。既然是 Anything，话题无穷无尽。',
    descriptionEn: 'Extra chapter. A collection of second-tier techniques — how to get over a breakup, how to win, how to choose a major, and more. Since it is "Anything", topics are endless.',
    publishDate: '2025-07-24',
    type: 'extra',
    pages: 23,
    status: 'available',
    slug: 'how6',
    color: '#ec4899',
    tags: ['番外', 'Anything', '二流技术', '实用指南'],
  },

];

export interface Concept {
  id: string;
  title: string;
  description: string;
  category: string;
  relatedChapters: string[];
  relatedConcepts: string[];
}

export const concepts: Concept[] = [
  {
    id: 'pan',
    title: '端盘儿菜',
    description: '在人类的知识/效率/思想/文化凸包上，做出原创的贡献。这是厉害的人的终极使命。',
    category: '核心哲学',
    relatedChapters: ['how0', 'how4'],
    relatedConcepts: ['tuchu', 'passion'],
  },
  {
    id: 'tuchu',
    title: '知识凸包',
    description: '人类已知知识的边界。在凸包上做原创贡献，才算真正给世界创造新价值。',
    category: '核心哲学',
    relatedChapters: ['how0', 'how5'],
    relatedConcepts: ['pan', 'yuanchuang'],
  },
  {
    id: 'passion',
    title: 'The Passion',
    description: '并非生理需求或被他人指派，每天不用催自己就干的事。找到 The Passion 是厉害的人的起点。',
    category: '个人成长',
    relatedChapters: ['how0'],
    relatedConcepts: ['lihaipeople', 'xuexiquxian'],
  },
  {
    id: 'lihaipeople',
    title: '厉害的人',
    description: '愿意给世界做原创贡献的人。其发育线以 how4/how5 为核心。',
    category: '人群分类',
    relatedChapters: ['how0', 'how4', 'how5'],
    relatedConcepts: ['bulihaipeople', 'pan'],
  },
  {
    id: 'bulihaipeople',
    title: '不厉害的人',
    description: '选择了不给世界做原创贡献的人（非贬义）。其发育线以 how1/how2 为核心，how3 人人都要学。',
    category: '人群分类',
    relatedChapters: ['how0', 'how1', 'how3'],
    relatedConcepts: ['lihaipeople', 'w0'],
  },
  {
    id: 'w0',
    title: 'W₀（~3000万）',
    description: '不厉害版的理财目标。约3000万可投资本金，对应永续财富自由的起点。',
    category: '财富体系',
    relatedChapters: ['how1'],
    relatedConcepts: ['w1', 'w2', 'bulihaipeople'],
  },
  {
    id: 'w1',
    title: 'W₁（~3亿）',
    description: '通过《怎样上岸》实现的财富量级。需要特殊机缘与心法，无通用路径。',
    category: '财富体系',
    relatedChapters: ['how2'],
    relatedConcepts: ['w0', 'w2'],
  },
  {
    id: 'w2',
    title: 'WH（~70亿+）',
    description: '厉害的人通过搞事实现的财富量级。不厉害的人无法完成。',
    category: '财富体系',
    relatedChapters: ['how4'],
    relatedConcepts: ['w1', 'lihaipeople'],
  },
  {
    id: 'gonglizero',
    title: '公理零：人类有未来',
    description: '5hows 的基础公理。信不信由你，没法论证。所有推论都建立在这个公理之上。',
    category: '理论基础',
    relatedChapters: ['how0'],
    relatedConcepts: ['guiyinzhen', 'jihe'],
  },
  {
    id: 'guiyinzhen',
    title: '归因真命题',
    description: '非严格真命题，但大概率是归因真命题的表述。5hows 大多数叙述属此类。区别于严格真命题。',
    category: '理论基础',
    relatedChapters: ['how0'],
    relatedConcepts: ['gonglizero', 'jihe'],
  },
  {
    id: 'jihe',
    title: '几何式写作',
    description: '按欧式几何结构展开——先有公理，然后定理，再推论。5hows 尽可能遵循此逻辑结构。',
    category: '理论基础',
    relatedChapters: ['how0'],
    relatedConcepts: ['gonglizero', 'guiyinzhen'],
  },
  {
    id: 'xuexiquxian',
    title: '学习曲线',
    description: '厉害的人只对自己的学习曲线负责。曲线足够陡峭，且 The Passion 与世界需求交不空，厉害就藏不住。',
    category: '个人成长',
    relatedChapters: ['how0'],
    relatedConcepts: ['passion', 'lihaipeople'],
  },
  {
    id: 'menghuanduizhang',
    title: '梦幻队长',
    description: '判断一件事的大小的金标准：你是一号位，且吸引了 n 个梦幻队长。梦幻队长越多，事业价值指数增加。',
    category: '创业理论',
    relatedChapters: ['how4'],
    relatedConcepts: ['lihaipeople', 'pan'],
  },
  {
    id: 'panjr',
    title: 'GRw=20%（理财极限）',
    description: '理财有极限回报率约为20%。这来自世界对"钱"的需求极限，厉害的人不受此约束。',
    category: '财富体系',
    relatedChapters: ['how1', 'how0'],
    relatedConcepts: ['w0', 'lihaipeople'],
  },
];

export interface TimelineEvent {
  date: string;
  title: string;
  description: string;
  type: 'publication' | 'milestone';
}

export const timeline: TimelineEvent[] = [
  {
    date: '2025-04',
    title: '5hows 创作完成',
    description: '写成于2504（2025年4月）',
    type: 'milestone',
  },
  {
    date: '2025-07-24',
    title: '主系列集中发布',
    description: '1怎样理财、3怎样保级、4怎样搞事、5怎样预测未来、6怎样Anything 同日发布',
    type: 'publication',
  },
  {
    date: '2025-07-28',
    title: '《0.怎样真正活过》发布',
    description: '代序篇，厉害版与不厉害版的发育线',
    type: 'publication',
  },
  {
    date: '2026-03-13',
    title: '《7.怎样Anything 2026版》开笔',
    description: '春雷乍动，树上的果实落地，新篇章启动',
    type: 'milestone',
  },
];
