import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mermaid from 'astro-mermaid';

const site = process.env.ASTRO_SITE || undefined;
const base = process.env.ASTRO_BASE || '/';

export default defineConfig({
	...(site ? { site } : {}),
	base,
	integrations: [
		mermaid({
			autoTheme: true,
			mermaidConfig: {
				maxTextSize: 200000,
				flowchart: {
					curve: 'basis',
					nodeSpacing: 32,
					rankSpacing: 44,
					useMaxWidth: true,
				},
			},
		}),
		starlight({
			title: 'Atruss Code Atlas',
			tableOfContents: false,
			favicon: '/favicon.png',
			customCss: ['./src/styles/material-theme.css'],
			head: [
				{
					tag: 'link',
					attrs: {
						rel: 'preconnect',
						href: 'https://fonts.googleapis.com',
					},
				},
				{
					tag: 'link',
					attrs: {
						rel: 'preconnect',
						href: 'https://fonts.gstatic.com',
						crossorigin: true,
					},
				},
				{
					tag: 'link',
					attrs: {
						rel: 'stylesheet',
						href: 'https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Roboto+Flex:opsz,wght@8..144,400;8..144,500;8..144,600;8..144,700&family=Roboto+Mono:wght@400;500;600&display=swap',
					},
				},
				{
					tag: 'link',
					attrs: {
						rel: 'stylesheet',
						href: 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,400,0..1,0',
					},
				},
			],
			social: [
				{
					icon: 'github',
					label: 'GitHub',
					href: 'https://github.com/kumarshaz/atruss-code-atlas',
				},
			],
			sidebar: [
				{
					label: 'Atlas Overview',
					link: '/',
				},
				{
					label: 'Organization Benchmarks',
					link: '/orgs/',
				},
				{
					label: 'Extracted Reports',
					autogenerate: { directory: 'reports' },
				},
			],
		}),
	],
});
