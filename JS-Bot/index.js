const { Client, Intents, MessageEmbed, Constants, MessageActionRow, MessageButton, Interaction } = require('discord.js');
const client = new Client({ intents: [Intents.FLAGS.GUILDS] });
const { REST } = require('@discordjs/rest');
const { Routes, InteractionResponseType } = require('discord-api-types/v9');
const dotenv = require('dotenv');
const mysql = require('mysql');
const assert = require('assert');
const python = require('python-bridge');
const Fakerator = require("fakerator");
const fakerator = Fakerator("default");
const osu = require('node-os-utils');
const { url } = require('inspector');
const { get } = require('http');
const axios = require('axios').default
const reddit = require('reddit.images')
const { RandomPHUB } = require('discord-phub');
const nsfw = new RandomPHUB(unique = true);
const giphy = require('giphy-api')(process.env.GIPHY_API);

// Process errors
process.on('uncaughtException', function (error) {
    console.log(error.stack);
});

dotenv.config();

// DB Stuff
const db = mysql.createConnection({
    host: "na01-sql.pebblehost.com",
    user: "customer_179919_doxbotdb",
    password: process.env.PASSWORD,
    database: "customer_179919_doxbotdb",
});
db.connect((err) => {
    if (err) throw err;
    console.log('DB Connected')
})

// py bridge
const py = python();
const {
    ex,
    end,
} = py;

// Write commands and descriptions
const commands = [
    { name: 'ping', description: 'Check if the bot is alive' },
    { name: 'help', description: "See a list of the bot's commands" },
    { name: 'dox', description: "Generate fake info about a user", options: [{ name: 'user', description: 'Who the bot should "dox", if blank it will "dox" you.',required: false, type: Constants.ApplicationCommandOptionTypes.USER}] },
    { name: 'support', description: "Get a link to the support server" },
    { name: 'embarrass', description: "Get an embarrassing fact about a user", options: [{ name: 'user', description: 'Who do you want to embarrass', required: false, type: Constants.ApplicationCommandOptionTypes.USER }] },
    { name: 'virgin', description: "Check someones virginity", options: [{ name: 'user', description: "Who's virginity do you want to check", required: false, type: Constants.ApplicationCommandOptionTypes.USER }] },
    { name: 'hate', description: "Tell the server who you hate", options: [{ name: 'user', description: "Who do you want to hate", required: true, type: Constants.ApplicationCommandOptionTypes.USER }] },
    { name: 'love', description: "Tell the server who you love", options: [{ name: 'user', description: "Who do you want to love", required: true, type: Constants.ApplicationCommandOptionTypes.USER }] }, 
    { name: 'pp', description: "Check the length of someones uhhh", options: [{ name: 'user', description: "Who's pp do you want to measure", required: false, type: Constants.ApplicationCommandOptionTypes.USER }] },
    { name: 'server', description: 'Get some server information' },
    { name: 'stats', description: "Get some cool stats about DoxBot" },
    { name: 'lfg', description: "Tell everyone you are looking to play a game", options: [{ name:'game', description:'What game do you want to play', required: true, type: Constants.ApplicationCommandOptionTypes.STRING }] },
    { name: 'iq', description: "Test someone's IQ", options: [{ name: 'user', description: "Who's iq do you want to test", required: false, type: Constants.ApplicationCommandOptionTypes.USER }] },
    { name: 'avatar', description: "Get someones profile picture and a link", options: [{ name: 'user', description: "Who's profile picture do you want", required: false, type: Constants.ApplicationCommandOptionTypes.USER }] },
    { name: 'invite', description: "Get a link to invite DoxBot to you're server" },
    { name: 'meme', description: 'Get a random meme from Reddit' },
    { name: 'nsfw', description: 'Get a nude from a variety of categories', options: [{ name: 'category', description: "Choose a category for the picture, a list can be found at https://www.npmjs.com/package/discord-phub", required: false, type: Constants.ApplicationCommandOptionTypes.STRING }] },
    { name: 'reddit', description: 'Get a random post from a given subreddit', options: [{ name: 'subreddit', description:'What subreddit do you want a post from', required: true, type: Constants.ApplicationCommandOptionTypes.STRING }] },
    { name: 'coinflip', description: 'Flip a coin' },
    { name: 'poll', description: 'Poll the people in your server', options: [{ name: 'option-1', description: 'The first option to put on the poll', required: true, type: Constants.ApplicationCommandOptionTypes.STRING }, { name: 'option-2', description: 'The second option to put on the poll', required: true, type: Constants.ApplicationCommandOptionTypes.STRING }] },
    { name: 'afk', description: 'Let everyone know you are AFK', options: [{ name: 'reason', description: 'Why are you AFK', required: false, type: Constants.ApplicationCommandOptionTypes.STRING}] },
    { name: '8ball', description: 'Ask the magic 8ball a question', options: [{ name: 'question', description: 'What do you want to ask the 8ball', required: true, type: Constants.ApplicationCommandOptionTypes.STRING}] },
    { name: 'dog', description: 'Get a random picture of a dog from Reddit' },
    { name: 'cat', description: 'Get a random picture of a cat from Reddit' },
    { name: 'cstats', description: 'See how many times a command has been run', options: [{ name: 'command', description: 'What command do you want stats on', required: true, type: Constants.ApplicationCommandOptionTypes.STRING }] },
    { name: 'gif', description: 'Get a random gif from GIPHY', options: [{ name: 'search', description: 'Search for a category of gifs', required: false, type: Constants.ApplicationCommandOptionTypes.STRING }] },
]; 

// Register slash commands
const rest = new REST({ version: '9' }).setToken(process.env.TOKEN);

(async () => {
  try {
    console.log('Started refreshing application (/) commands.');

    await rest.put(
        Routes.applicationGuildCommands(process.env.APP_ID, '731445738290020442', '801360477984522260'),
        { body: commands },
        // Routes.applicationCommands(process.env.APP_ID),
        // {body: commands},
    );

    await rest.put(
        Routes.applicationGuildCommands(process.env.APP_ID, '801360477984522260'),
        { body: commands },
        // Routes.applicationCommands(process.env.APP_ID),
        // {body: commands},
    );

    console.log('Successfully reloaded application (/) commands.');
  } catch (error) {
    console.error(error);
  }
})();

// When the bot is ready
client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

// Define what happens with commands
client.on('interactionCreate', async interaction => {
    if (!interaction.isCommand()) return;

    const { commandName, options, user, guild, channel, ChannelData, } = interaction
    
    if (commandName === 'ping') {
        await interaction.reply({
            content: pingCmd(user),
            ephemeral: true
        })
    }

    if (commandName === 'help') {
        await interaction.reply({
            embeds: [ helpCmd(user, guild) ]
        })
    }

    if (commandName === 'dox') {
        const toDox = options.getUser('user')
        await interaction.reply({
            embeds: [doxCmd(user,guild,toDox)]
        })
    }

    if (commandName === 'support') {
        await interaction.reply({
            embeds: [supportCmd(user,guild)],
            ephemeral: true
        })
    }

    if (commandName === 'embarrass') {
        const embUser = options.getUser('user')
        await interaction.reply({
            embeds: [embarrassCmd(user,guild,embUser)]
        })
    }

    if (commandName === 'virgin') {
        const virgUser = options.getUser('user')
        await interaction.reply({
            embeds: [virginCmd(user,guild,virgUser)]
        })
    }

    if (commandName === 'hate') {
        const hateUser = options.getUser('user')
        await interaction.reply({
            embeds: [hateCmd(user,guild,hateUser)]
        })
    }

    if (commandName === 'love') {
        const loveUser = options.getUser('user')
        await interaction.reply({
            embeds: [loveCmd(user,guild,loveUser)]
        })
    }

    if (commandName === 'pp') {
        const ppUser = options.getUser('user')
        await interaction.reply({
            embeds: [ppCmd(user,guild,ppUser)]
        })
    }

    if (commandName === 'server') {
        await interaction.reply({
            embeds: [serverCmd(user,guild)]
        })
    }

    if (commandName === 'stats') {
        statsCmd(user, guild, async function(embed) {
            await interaction.reply({
                embeds: [embed]
            })
        })
    }

    if (commandName === 'lfg') {
        const game = options.getString('game')
        await interaction.reply({
            embeds: [lfgCmd(user,guild,game)]
        })
    }

    if (commandName === 'iq') {
        const iqUser = options.getUser('user')
        await interaction.reply({
            embeds: [iqCmd(user,guild,iqUser)]
        })
    }

    if (commandName === 'avatar') {
        const avUser = options.getUser('user')
        await interaction.reply({
            embeds: [await avatarCmd(user,guild,avUser)]
        })
    }

    if (commandName === 'invite') {
        const row = new MessageActionRow()
        .addComponents(
            new MessageButton()
                .setLabel('Click Here')
                .setURL('https://doxbot.xyz/invite')
                .setStyle('LINK')
        )
        interaction.reply({
            embeds: [inviteCmd(user,guild)],
            components: [row],
            ephemeral: true
        })
    }

    if (commandName === 'meme') {
        interaction.reply({
            embeds: [await memeCmd(user, guild)]
        })
    }

    if (commandName === 'nsfw') {
        const category = options.getString('category')
        nsfwCmd(user, guild, channel, category, function(embed) {
            interaction.reply({
                embeds: [embed]
            })
        })
    }

    if (commandName === 'reddit') {
        const subreddit = options.getString('subreddit')
        redditCmd(user, guild, subreddit, function(embed) {
            interaction.reply({
                embeds: [embed]
            })
        })
    }

    if (commandName === 'coinflip') {
        interaction.reply({
            embeds: [coinflipCmd(user,guild)]
        })
    }

    if (commandName === 'poll') {
        const opt1 = options.getString('option-1')
        const opt2 = options.getString('option-2')
        const message = await interaction.reply({
            embeds: [pollCmd(user,guild,opt1,opt2)],
            fetchReply: true
        })
        message.react('1️⃣')
        message.react('2️⃣')
    }

    if (commandName === 'afk') {
        const reason = options.getString('reason')
        interaction.reply({
            embeds: [afkCmd(user,guild,reason)]
        })
    }

    if (commandName === '8ball') {
        const question = options.getString('question')
        interaction.reply({
            embeds: [eightballCmd(user,guild,question)]
        })
    }

    if (commandName === 'dog') {
        await dogCmd(user,guild,function(embed) {
            interaction.reply({
                embeds: [embed]
            })
        })
    }

    if (commandName === 'cat') {
        await catCmd(user,guild,function(embed) {
            interaction.reply({
                embeds: [embed]
            })
        })
    }

    if (commandName === 'cstats') {
        const command = options.getString('command')
        cstatsCmd(user,guild,command,function(embed) {
            interaction.reply({
                embeds: [embed]
            })
        })
    }

    if (commandName === 'gif') {
        const search = options.getString('search')
        gifCmd(user,guild,search,function(embed) {
            interaction.reply({
                embeds: [embed]
            })
        })
    }
});

// DB Query to add command stat
function cmdRun(cmdName, user) {
    db.query(`SELECT used FROM commands WHERE name = '${cmdName}'`, (err,rows) => {
        rows.forEach((row) => {
            if (err) throw err;
            let num = row.used;
            num++
            db.query(`UPDATE commands SET used = ${num} WHERE name = '${cmdName}'`, (err,result) => {
                if (err) throw err;
            })
        })
    })
    console.log(`${cmdName} -- ${user.username}#${user.discriminator}`)
}

// Help Command
function helpCmd(user, guild) {
    const cmdName = 'help'
    const embed = new MessageEmbed()
        .setColor('#ff6666')
        .setTitle('DoxBot Help')
        .setDescription('All DoxBot commands are run using the `/` prefix')
        .addField('Music:', 'none', false)
        .addField('Moderation:', 'none', false)
        .addField('Economy:', 'none', false)
        .addField('Starboard:', 'none', false)
        .addField('Server Stats:', 'none', false)
        .addField('Utility:', '`ping`, `support`, `server`, `stats`, `invite`, `coinflip`, `lfg [game]`', false)
        .addField('Fun:', '`dox`, `pp [user]`, `virgin [user]`, `hate [user]`, `love [user]`, `iq [user]`, `nsfw`, `reddit [subreddit]`, `embarrass [user]`, `meme`, ', false)
        .addField('Links', '[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)', false)
    cmdRun(cmdName, user)
    return embed
}

// Ping Command
function pingCmd(user) {
    const cmdName = 'ping';
    const response = `Pong! **${Math.round(client.ws.ping)}ms**`
    cmdRun(cmdName, user)
    return response
}

// Dox Command
function doxCmd(user, guild, toDox) {
    const cmdName = 'dox'  
    const name = fakerator.names.name()
    const ip = fakerator.internet.ip()
    const height = `${Math.floor(Math.random() * 6)}' ${Math.floor(Math.random() * 11)}"`
    const weight = `${Math.floor(Math.random() * 400) + 50} Lbs.`
    const address = fakerator.address.street()
    const coordinates = fakerator.address.geoLocation()
    const email = fakerator.internet.email()
    const password = fakerator.internet.password(7)
    const phone = fakerator.phone.number()
    const ssn = `${Math.floor(Math.random() * 999) + 100}-${Math.floor(Math.random() * 90) + 10}-${Math.floor(Math.random() * 9999) + 1000}`
    
    if (toDox === null) {
        toDox = user
    }

    const embed = new MessageEmbed()
        .setColor('RED')
        .setTitle(`Doxing ${toDox.username}`)
        .addField('Full Name:', name, false)
        .addField('IP Address:', ip, false)
        .addField('SSN:', ssn, false)
        .addField('Height:', height, false)
        .addField('Weight:', weight, false)
        .addField('Address:', address, false)
        .addField('Email:', email, false)
        .addField('Password:', password, false)
        .addField('Phone Number:', phone, false)

    cmdRun(cmdName, user)
    return embed
}

// Support Command
function supportCmd(user, guild) {
    const cmdName = 'support'
    const embed = new MessageEmbed()
        .setColor('RANDOM')
        .setTitle('Need some help?')
        .setDescription('[Click Here For The Offical Support Server](https://doxbot.xyz/server)')
    cmdRun(cmdName, user)
    return embed
}

// Embarrass command
function embarrassCmd(user,guild,embUser) {
    const cmdName = 'embarrass'
    if (embUser === null) {
        embUser = user
    }
    const embarrassArray = ['', 'They peed the bed last night' , 'They havent showered in 3 weeks' , 'Their favorite movie is "Cuties" uhhh' , 'They collect their belly button lint' , 'They tried to slide in my DMs last night' , 'Got friendzoned by 4 different people in one day' , 'Says "bababoey" unironically' , 'Doesnt wipe after they poop' , 'Still sleeps in their moms bed' , 'Some how managed to fail study hall' , 'Their destiny is to be a 40 year old virgin']
    const embarrassNum = Math.floor(Math.random() * embarrassArray.length)
    const embed = new MessageEmbed()
        .setColor('RANDOM')
        .setTitle(`${embUser.username} - ${embarrassArray[embarrassNum]}`)
    cmdRun(cmdName, user)
    return embed
}

// Virgin Command
function virginCmd(user, guild, virgUser) {
    const cmdName = 'virgin'
    cmdRun(cmdName, user)
    if (virgUser === null) {
        virgUser = user
    }
    const virgAray = ['<:yestick:799590853588811818> Ya no shit' , '<:notick:799590818054668307> Nope, gross' , '<:yestick:799590853588811818> Obviously' , '<:notick:799590818054668307> Fuck Master']
    const virginNum = Math.floor(Math.random() * virgAray.length)
    if (virginNum == 0) {
        const embed = new MessageEmbed()
            .setColor('GREEN')
            .setTitle(`${virgUser.username} - ${virgAray[virginNum]}`)
        return embed
    } else if (virginNum == 2) {
        const embed = new MessageEmbed()
            .setColor('GREEN')
            .setTitle(`${virgUser.username} - ${virgAray[virginNum]}`)
        return embed
    } else {
        const embed = new MessageEmbed()
            .setColor('RED')
            .setTitle(`${virgUser.username} - ${virgAray[virginNum]}`)
        return embed
    }
}

// We hate command
function hateCmd(user, guild, hateUser) {
    const cmdName = 'hate'
    const embed = new MessageEmbed()
        .setColor('RED')
        .setTitle(`We hate ${hateUser.username}`)
    cmdRun(cmdName, user)
    return embed
}

// We love command
function loveCmd(user, guild, loveUser) {
    const cmdName = 'love'
    const embed = new MessageEmbed()
        .setColor('GREEN')
        .setTitle(`We love ${loveUser.username}`)
    cmdRun(cmdName, user)
    return embed
}

// PP Command
function ppCmd(user, guild, ppUser) {
    const cmdName = 'pp'
    if (ppUser === null) {
        ppUser = user
    }
    const ppArray = ['Homies hung as a horse', 'Shrimp gang for life' , 'Aye nothing wrong with average' , '"Have you put it in yet?" Sound familiar?' , '3 inch punisher' , 'Its belived that the ancient Egyptions spoke of a mythical schlong like theirs' , 'Sheesh my guys packin' , 'Hey man, its ok its not the size of the boat its the motion of the ocean right?' , 'ERROR: NO PP DETECTED' , 'A good 6er' , 'IDK when I went to inspect it, it wrapped around my neck and I passed out' , 'Its ok man some like it to be small and soft' ,'Damn theyve got a solid 9 inches soft' , 'Seeing theirs made me want to appologize to Mrs. DoxBot for not being able to give her that']
    const ppNum = Math.floor(Math.random() * ppArray.length)
    const embed = new MessageEmbed()
        .setColor('RANDOM')
        .setTitle(`${ppUser.username} - ${ppArray[ppNum]}`)
    cmdRun(cmdName, user)
    return embed 
}

// Server command
function serverCmd(user, guild) {
    const cmdName = 'server'
    const serverName = guild.name
    const serverDesc = guild.description
    const serverId = `${guild.id}`
    const region = guild.region
    const memCount = guild.memberCount
    const iconUrl = guild.iconURL()
    const embed = new MessageEmbed()
        .setColor('RANDOM')
        .setThumbnail(iconUrl)
        .setTitle(serverName)
        .setDescription(`Description: ${serverDesc}`)
        .addField('Server ID', serverId, true)
        .addField('Members', `${memCount}`, true)
    cmdRun(cmdName, user)
    return embed
}

// Stats command

function numCmdRun(callback) {
    var sql = 'SELECT SUM(used) FROM commands AS sum';
    db.query(sql, function(err, results) {
        if (err) {
            throw err
        }
        var res = Object.values(JSON.parse(JSON.stringify(results)))
        return callback(res[0]['SUM(used)'])
    })
}

function statsCmd(user, guild, callback) {
    const cmdName = 'stats'
    const guilds = client.guilds.cache.size
    const users = client.users.cache.size
    const cpu = osu.cpu
    const mem = osu.mem

    numCmdRun(function (result) {
        cpu.usage().then(cpuPercentage => {
            mem.info().then(info => {
                const cmdsRun = result
                const embed = new MessageEmbed()
                    .setColor('#ff6666')
                    .setThumbnail('https://doxbot.xyz/images/doxlogo2')
                    .setTitle('DoxBot Stats')
                    .addField("Servers:", `${guilds}`, true)
                    .addField('Users:', `${users}`, true)
                    .addField('Commands:', '162', true)
                    .addField('Cmds. Run', `${cmdsRun}`, true)
                    .addField('CPU %', `${cpuPercentage}`, true)
                    .addField('Mem. %', `${info.freeMemPercentage}%`, true)
                    .addField('Ping', `${Math.round(client.ws.ping)}ms`, true)
                    .addField('Library:', 'Discord.JS', true)
                    .addField('Owner:', 'dickey#6969', true) 
                return callback(embed)
            });
        })
    }) 
    cmdRun(cmdName, user)
}

// LFG Command
function lfgCmd(user, guild, game) {
    const cmdName = 'lfg'
    const embed = new MessageEmbed()
        .setColor('RANDOM')
        .setTitle(`${user.username} is looking to play ${game}`)
        .setDescription(`If you're interested, DM them - <@${user.id}>`)
    cmdRun(cmdName, user)
    return embed
}

// IQ Comand
function iqCmd(user, guild, iqUser) {
    const cmdName = 'iq'
    if (iqUser === null) {
        iqUser = user
    }
    const iqArray = ['Homies dumb as bricks. IQ = 4', 'Literally 0', 'Our holy overlord. IQ = 10,000', 'Enstein is that you? IQ = 258', 'IQ = 21', 'I am a JS program that doesnt even really exist and I am still smarter than this guy. IQ = 1', 'IQ = 14', 'IQ = 413, my god...', 'They forget their glasses are on their head, IQ = 32', 'About the eqivalant as my creator, IQ = 1947', 'IQ = 46', 'Look up a picture of dumb in the dictionary and you will get a picture of this guy, IQ = 5', 'IQ = 134', 'IQ = 102', 'IQ = 2', 'sO dum i furget hoW 2 spill, ia = -291', 'No :)', 'ERROR: NO IQ DETECTED', 'At least they have a big di.. oh wait no my sources are telling me thats almost as small as their IQ, IQ = -131344', 'You know what they say... actually no I dont know what they say my creator forgot. IQ = 420', 'HAHA FUNNY SEX NUMBER IQ = 69']
    const iqNum = Math.floor(Math.random() * iqArray.length)
    const embed = new MessageEmbed()
        .setColor('RANDOM')
        .setTitle(`${iqUser.username}#${iqUser.discriminator} IQ Test: ${iqArray[iqNum]}`)
    cmdRun(cmdName, user)
    return embed
}

// Avatar Command
async function avatarCmd(user, guild, avUser) {
    const cmdName = 'avatar'
    if (avUser === null) {
        avUser = user
    }
    const avUser2 = await avUser.fetch()
    const embed = new MessageEmbed()
        .setTitle(`${avUser.username}'s Avatar`)
        .setColor(avUser2.hexAccentColor)
        .setDescription(`URL: [Click Here](${avUser.displayAvatarURL()})`)
        .setImage(avUser.displayAvatarURL())
    cmdRun(cmdName, user)
    return embed
}

// Invite Command
function inviteCmd(user, guild) {
    const cmdName = 'invite'
    const embed = new MessageEmbed()
        .setTitle('Invite DoxBot to your server!')
    cmdRun(cmdName, user)
    return embed
}

// Meme command
async function memeCmd(user, guild) {
    const cmdName = 'meme'
    const memeRes = await axios({
        method: 'get',
        url: 'https://memes.blademaker.tv/api?lang=en',
        responseType: 'json'
    })
    const res = memeRes['data']
    const title = res['title']
    const ups = res['ups']
    const sub = res['subreddit']
    const link = `https://reddit.com/${res['id']}`
    const author = res['author']
    const image = res['image']
    const embed = new MessageEmbed()
        .setTitle(`${title}`)
        .setColor('ORANGE')
        .setURL(`${link}`)
        .setImage(image)
        .setFooter({text: `👍: ${ups} | r/${sub} | u/${author}`})
    cmdRun(cmdName, user)
    return embed
}

// NSFW Command
function nsfwCmd(user, guild, channel, category, callback) {
    const cmdName = 'nsfw'

    if (channel.nsfw) {

        if (category === null) {
            const image = nsfw.getRandom("jpg")
            const embed = new MessageEmbed()
                .setTitle(`Random ${image.category} picture`)
                .setImage(image.url)
                cmdRun(cmdName, user)
            return callback(embed)
        } else {
            if (nsfw.categories.includes(category)) {
                const image = nsfw.getRandomInCategory( category, "jpg")
                const embed = new MessageEmbed()
                    .setTitle(`Random ${image.category} picture`)
                    .setImage(image.url)
                    cmdRun(cmdName, user)
                return callback(embed)
            } else {
                const embed = new MessageEmbed()
                    .setTitle('That is not a valid category')
                    .setColor('RED')
                    .addField('Valid categories', '`3d-porn`, `aesthetic`, `amateur`, `anal`, `asian`, `asmr`, `ass`, `bath-shower`, `bdsm`, `boobs`, `cock`, `cosplay`, `creampie`, `cuckhold`, `cumshots`, `dilf`, `double-penetration`, `ebony`, `feet`, `femdom`, `fisting`, `food-play`, `funny`, `furry`, `glory-hole`, `goth`, `hands`, `hentai-no-loli`, `hentai`, `horror`, `interracial`, `joi`, `lactation`, `latin`, `lgbt-bisexual`, `lgbt-femboy`, `lgbt-gay`, `lgbt-lesbian`, `lgbt-transgender`, `lgbt-twink`, `lingerie`, `massage`, `mature`, `milf`, `naked-wrestling`, `oral`, `orgy`, `pegging`, `petite`, `plus-size`, `pornstar`, `pov`, `public`, `pussy`, `rimming`, `rough`, `solo`, `squirting`, `tattoos-piercings`, `tease`, `thighs`, `threesomes`, `toys`, `uniform`, `vintage`, `watersports`', false)
                return callback(embed)
            }
        }

    } else {
        const embed = new MessageEmbed()
            .setTitle('That command can only be used in a NSFW channel')
            .setColor('RED')
        cmdRun(cmdName, user)
        return callback(embed)
    }
} 

// Specific reddit command
function redditCmd(user, guild, subreddit, callback) {
    const cmdName = 'reddit'
    try {
        reddit.FetchSubredditPost({ subreddit: subreddit }).then((data) => {
            if (data.NSFW) {
                const embed = new MessageEmbed()
                    .setTitle('That is an NSFW subreddit, please use the NSFW command for this')
                    .setColor('RED')
                    cmdRun(cmdName, user)
                return callback(embed)
            }

            const embed = new MessageEmbed()
                .setTitle(data.title)
                .setURL(data.postLink)
                .setColor('ORANGE')
                .setImage(data.image)
                .setFooter({ text: `👍: ${data.upvotes} | By: u/${data.author} | r/${data.subreddit}` })
            cmdRun(cmdName, user)
            return callback(embed)
        })
    } catch (error) {
        const embed = new MessageEmbed()
            .setTitle('Error: Please contact support [Here](https://doxbot.xyz/server)')
            .setColor('RED')
            cmdRun(cmdName, user)
        return callback(embed)
    }
}

// Coin flip command
function coinflipCmd(user, guild) {
    const cmdName = 'coinflip'
    const choice = Math.round(Math.random())
    if (choice === 1) {
        const embed = new MessageEmbed()
            .setTitle('<:simp_coin:824720566241853460> Heads!')
            .setColor('GOLD')
            cmdRun(cmdName, user)
        return embed
    } else {
        const embed = new MessageEmbed()
            .setTitle('<:fuck_coin:824720614543196220> Tails!')
            .setColor('GOLD')
        cmdRun(cmdName, user)
        return embed
    }
}

// Poll Command
function pollCmd(user, guild, opt1, opt2) {
    const cmdName = 'poll'
    const embed = new MessageEmbed()
        .setTitle(`Poll:`)
        .addField('Option 1️⃣', opt1, false)
        .addField('Option 2️⃣', opt2, false)
        .setFooter({ text:'React with 1️⃣ or 2️⃣' })
    cmdRun(cmdName, user)
    return embed
}

// AFK command
function afkCmd(user, guild, reason) {
    const cmdName = 'afk'
    if (reason === null) {
        reason = 'None'
    }
    const embed = new MessageEmbed()
        .setTitle(`${user.tag} is AFK`)
        .setDescription(`Reason: ${reason}`)
    cmdRun(cmdName, user)
    return embed
}

// 8-ball command
function eightballCmd(user, guild, question) {
    const cmdName = '8ball'
    const resArray = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', 'Dont count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt', 'Yes.', 'Yes – definitely.', 'You may rely on it.']
    const resNum = Math.floor(Math.random() * resArray.length)
    const res = resArray[resNum]
    const embed = new MessageEmbed()
        .setTitle('Magic 8-ball')
        .setThumbnail('https://img.pngio.com/magic-8-ball-by-horoscopecom-get-free-divination-games-just-for-fun-magic-8-ball-png-300_300.png')
        .addField(`A: ${res}`, `Q: ${question}`, false)
    cmdRun(cmdName, user)
    return embed
}

// Dog command
async function dogCmd(user, guild, callback) {
    const cmdName = 'dog'
    reddit.FetchSubredditPost({ subreddit: 'DogPics' }).then((data) => {
        var image = data.image
        if (data.gallery) {
            image = data.image[0]
        }
        const embed = new MessageEmbed()
            .setTitle(data.title)
            .setURL(data.postLink)
            .setColor('ORANGE')
            .setImage(data.image)
            .setFooter({ text: `👍: ${data.upvotes} | By: u/${data.author} | r/${data.subreddit}` })
        cmdRun(cmdName, user)
        return callback(embed)
    })
}

// Cat command
async function catCmd(user, guild, callback) {
    const cmdName = 'cat'
    reddit.FetchSubredditPost({ subreddit: 'catpics' }).then((data) => {
        var image = data.image
        if (data.gallery) {
            image = data.image[0]
        }
        const embed = new MessageEmbed()
            .setTitle(data.title)
            .setURL(data.postLink)
            .setColor('ORANGE')
            .setImage(data.image)
            .setFooter({ text: `👍: ${data.upvotes} | By: u/${data.author} | r/${data.subreddit}` })
        cmdRun(cmdName, user)
        return callback(embed)
    })
}

// Command stats
function cstatsCmd(user, guild, command, callback) {
    const cmdName = 'cstats'
    if (command === 'all') {
        var sql = 'SELECT SUM(used) FROM commands AS sum';
        db.query(sql, function(err, results) {
            if (err) {
                throw err
            }
            var res = Object.values(JSON.parse(JSON.stringify(results)))
            const num = res[0]['SUM(used)']
            const embed = new MessageEmbed()
                .setTitle('Commands Run')
                .setColor('RANDOM')
                .setDescription(`DoxBot has executed **${num}** commands`)
                .setFooter({ text: 'Since Febuary 29, 2021' })
            cmdRun(cmdName, user)
            return callback(embed)
        })
    } else {
        db.query(`SELECT used FROM commands WHERE name = '${command}'`, (err,rows) => {
            rows.forEach((row) => {
                if (err) throw err;
                let num = row.used;
                const embed = new MessageEmbed()
                    .setTitle('Commands Run')
                    .setColor('RANDOM')
                    .setDescription(`**/${command}** has been used **${num}** times`)
                    .setFooter({ text: 'Since Febuary 29, 2021' })
                cmdRun(cmdName, user)
                return callback(embed)
            })
        })
    }
}

// Giphy command
function gifCmd(user, guild, search, callback) {
    const cmdName = 'gif'
    if (search === null) {
        search = 'random'
    }
    giphy.search({
        q: search,
        rating: 'g',
        limit: 5
    }, function (err, res) {
        if (err) {
            throw err
        }
        
        const resNum = Math.round(Math.random() * res.data.length)
        const resFinal = res.data[resNum]

        const embed = new MessageEmbed()
            .setTitle(resFinal.title)
            .setURL(resFinal.url)
            .setColor('RANDOM')
            .setImage(`https://media.giphy.com/media/${resFinal.id}/giphy.gif`)
            .setFooter({ text: `By: ${resFinal.user}`, iconURL: resFinal.user.avatar_url })
        return callback(embed)
    });
}

// Run bot
client.login(process.env.TOKEN);