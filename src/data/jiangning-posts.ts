export interface JiangningPost {
  id: string;          // e.g. 'jn1'
  number: number;
  title: string;
  subtitle: string;    // 文章类型，如 '商业观察', '时评', '投资随笔'
  description: string;
  publishDate: string;
  slug: string;
  color: string;
  tags: string[];
  author: string;
  source: string;
}

export const jiangningPosts: JiangningPost[] = [
  {
    id: 'jn1',
    number: 1,
    title: '从MANUS收购被否谈起',
    subtitle: '商业观察',
    description: '一家公司在获得国家媒体表扬后迁往新加坡并出售给META——这不是法律问题，而是规则与规矩的问题。君子交绝，不出恶声。',
    publishDate: '2026-04-29',
    slug: 'jn1',
    color: '#0f766e',
    tags: ['MANUS', '创业', '商业逻辑', '规则'],
    author: '唐僧的碎碎念',
    source: '唐僧的禅房',
  },
];
