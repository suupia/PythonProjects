// discord.js モジュールのインポート
const Discord = require('discord.js');

// Discord Clientのインスタンス作成
const client = new Discord.Client();

// トークンの用意
const token = 'ここにコピーしたBotのトークン';

// 起動するとconsoleにready...と表示される
client.on('ready', () => {
    console.log('ready...');
});

client.on('message', message => {
    if(message.author.bot) return; //BOTのメッセージには反応しない

    if(message.content === "/hello"){ //送られたメッセージがhelloだったら
        message.channel.send("HELLO!")
        //メッセージが送られたチャンネルに HELLO!と送信する
    }
})

// Discordへの接続
client.login(token);
