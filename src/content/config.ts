import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    // ↓ ここで許可するタグの文字列を完全に固定します
    tags: z.array(z.enum(['Omarchy', 'Linux', '開発環境', 'トラブルシューティング'])).optional(),
  }),
});

export const collections = { blog };