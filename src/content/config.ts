import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    excerpt: z.string(),
    date: z.date(),
    author: z.string().default('Evans Mathibe'),
    tags: z.array(z.string()),
    cover: z.string(),
  }),
});

const services = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    shortTitle: z.string(),
    positionLine: z.string(),
    deliverables: z.array(z.string()),
    order: z.number(),
  }),
});

const locations = defineCollection({
  type: 'content',
  schema: z.object({
    region: z.string(),
    role: z.string(),
    blurb: z.string(),
    coordinates: z.tuple([z.number(), z.number()]).optional(),
    capabilities: z.array(z.string()),
  }),
});

export const collections = { blog, services, locations };
