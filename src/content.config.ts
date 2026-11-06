import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const guides = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/guides' }),
  schema: z.object({
    title: z.string(),
    description: z.string().max(165),
    publishedAt: z.coerce.date(),
    updatedAt: z.coerce.date().optional(),
    category: z.enum(['Architecture', 'Comparison', 'Compatibility', 'Performance']),
    takeaway: z.string(),
    readingMinutes: z.number().int().positive(),
  }),
});

export const collections = { guides };
