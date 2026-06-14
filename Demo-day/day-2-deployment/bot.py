import os
import discord
from discord.ext import commands
import httpx
from dotenv import load_dotenv

# Load token dari file .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Setup intents wajib Discord
intents = discord.Intents.default()
intents.message_content = True  # WAJIB di-checklist di Developer Portal
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # --- CHECKLIST 3: Bot Online (Hijau) ---
    print(f"🎉 {bot.user.name} sudah online dan siap tempur di Discord!")

# --- CHECKLIST 4: Demo !chat + mention ---
@bot.command(name="chat")
async def chat_command(ctx, *, message: str = None):
    if not message:
        await ctx.send(f"{ctx.author.mention}, kamu mau nanya apa? Contoh: `!chat WiFi lemot`")
        return
    
    # Kirim status "typing..." biar kelihatan responsif pas demo depan kelas
    async with ctx.typing():
        try:
            # Tembak request ke backend FastAPI
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{API_URL}/chat", json={"message": message}, timeout=15.0)
                
            if res.status_code == 200:
                bot_response = res.json().get("response", "(Kosong)")
                # Berikan mention ke user sesuai syarat checklist
                await ctx.send(f"{ctx.author.mention} {bot_response}")
            else:
                await ctx.send(f"Gagal konek ke otak BERT (Status: {res.status_code})")
        except Exception as e:
            await ctx.send(f"Error menghubungi backend: {e}")

bot.run(TOKEN)