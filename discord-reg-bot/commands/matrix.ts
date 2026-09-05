import type { Command } from './index.ts';

export default {
	data: {
		name: 'matrix',
		description: 'Create New Matrix User',
	},
	async execute(interaction) {
		await interaction.reply('Pong!');
	},
} satisfies Command;
