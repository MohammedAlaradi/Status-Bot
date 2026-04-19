import dotenv from "dotenv";
import { Client, GatewayIntentBits } from "discord.js";
import fetch from "node-fetch";
dotenv.config();



const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

const channelCooldowns = new Map();

client.once("ready", () => {
  console.log(`Status Bot is online as ${client.user.tag}`);
});


client.login(process.env.DISCORD_TOKEN);