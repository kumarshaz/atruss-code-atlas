import { defineCollection, z } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
	docs: defineCollection({
		loader: docsLoader(),
		schema: docsSchema({
			extend: z.object({
				org: z.string().optional(),
				repo_name: z.string().optional(),
				language: z.string().optional(),
				framework: z.string().optional(),
				has_pipeline: z.boolean().optional(),
				has_docker: z.boolean().optional(),
				has_kubernetes: z.boolean().optional(),
				has_api: z.boolean().optional(),
				doc_priority: z.string().optional(),
				last_updated: z.union([z.string(), z.date()]).optional(),
				github_url: z.string().optional(),
			}),
		}),
	}),
};
