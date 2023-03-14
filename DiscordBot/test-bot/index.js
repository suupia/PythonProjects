const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMembers] });

client.once('ready', () => {
	console.log('Ready!'); // 起動した時に"Ready!"とコンソールに出力する
});

client.on("guildMemberAdd", member => {
    if (member.guild.id !== "881033596532555797") return; // 指定のサーバー以外では動作しないようにする
    member.guild.channels.cache.get("1082900457527201883").send(`${member.user}が参加しました！`);
});

client.login("MTA4MDc5ODM0NDE2ODg2OTkyMg.GCr14g.wjBOnxhf7Qp4DxUUcwDJVjJ7QqBWCrg6rhX9ME");
