from pytube import Playlist, YouTube
import customtkinter
import threading
import re
import unicodedata

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("700x480")
app.title("TK YT Downloader")

def slugify(value, allow_unicode=False):
    """
        Taken from https://github.com/django/django/blob/master/django/utils/text.py
        Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
        dashes to single dashes. Remove characters that aren't alphanumerics,
        underscores, or hyphens. Convert to lowercase. Also strip leading and
        trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
        
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        
    value = re.sub(r'[^\w\s-]', '', value.lower())
    
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def is_playlist(url):
    return bool(re.search(r'[?&]list=', url))

def startDownload():
    
    download_thread = threading.Thread(target=downloadInThread)
    download_thread.daemon = True
    download_thread.start()
    
def downloadInThread():
    
    button.configure(state="disabled")
    
    try:
        
        type = downloadType.get();
        url = ytUrl.get();
        
        if(not url):
            result.configure(text="Insert a video URL")      
            return
        
        result.configure(text="Wait a moment...", text_color="white")      
        downloadProgress.set(0)
    
        if is_playlist(url):
            
            p = Playlist(url)
            ytTitle.configure(text=p.title)
            totalVideos = len(p.videos)
            cleanedTitle = slugify(p.title)
            
            if(type == "Audio only"):
                print("Downloading audio only")
                
                for i, video in enumerate(p.videos):
                    video.streams.get_audio_only().download(f"./Downloads/{cleanedTitle}")
                    downloadProgress.set((i + 1) / totalVideos)

            else:
                print("Downloading audio & video")
                
                for i, video in enumerate(p.videos):
                    video.streams.get_highest_resolution().download(f"./Downloads/{cleanedTitle}")
                    downloadProgress.set((i + 1) / totalVideos)
        
        else:
            yt = YouTube(url, on_progress_callback=progressBarUpdate)
            ytTitle.configure(text=yt.title)

            if type == "Audio only":
                yt.streams.get_audio_only().download("./Downloads")
                
            else:
                yt.streams.get_highest_resolution().download("./Downloads")
                
        result.configure(text="Download concluded!", text_color="white")
    
    except Exception as e:
        result.configure(text=e, text_color="red")

    button.configure(state="normal")

def progressBarUpdate(stream, chunk, bytes_remaining):
    
    totalSize = stream.filesize
    bytesDownloaded = totalSize - bytes_remaining
    completed = bytesDownloaded / totalSize * 100
    
    print(str(int(completed)) + "%")
    
    downloadProgress.set(float(completed) / 100)
    downloadProgress.update()

# Video Title
ytTitle = customtkinter.CTkLabel(master=app, text="Title")
ytTitle.pack()

# Video URL
ytUrl = customtkinter.CTkEntry(master=app, placeholder_text="Youtube URL", width=300)
ytUrl.pack()

# Download Type
downloadType = customtkinter.StringVar(value="Audio only")
downloadTypeButton = customtkinter.CTkComboBox(app, values=["Audio only", "Audio & video"], variable=downloadType)
downloadTypeButton.set("Audio only")
downloadTypeButton.pack(padx=10, pady=10)

# Start Download
button = customtkinter.CTkButton(master=app, text="Download", command=startDownload)
button.pack(padx=10, pady=10)

# Progress Bar
downloadProgress = customtkinter.CTkProgressBar(master=app)
downloadProgress.set(0)
downloadProgress.pack(padx=10, pady=10)

result = customtkinter.CTkLabel(master=app, text="")
result.pack(padx=10, pady=5)

app.mainloop()