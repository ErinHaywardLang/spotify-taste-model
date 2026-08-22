import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class QuietCacheHandler(CacheFileHandler):
    """Cache handler that doesn't print errors"""
    def save_token_to_cache(self, token_info):
        try:
            return super().save_token_to_cache(token_info)
        except Exception:
            # Silently ignore cache write errors
            pass

def get_spotify_client():
    """
    Returns an authenticated Spotify client with quiet cache handling.
    """
    # Find project root directory (where .env file is located)
    current_dir = os.getcwd()
    project_root = current_dir
    
    # If we're in notebooks/ subdirectory, go up one level
    if current_dir.endswith('/notebooks'):
        project_root = os.path.dirname(current_dir)
    
    # Ensure .spotify_cache directory exists in project root
    cache_dir = os.path.join(project_root, ".spotify_cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, "token")
    
    # Essential scopes for music data access
    scopes = [
        "user-read-private",
        "user-library-read", 
        "playlist-read-private",
        "playlist-read-collaborative"
    ]
    
    # Use custom quiet cache handler
    cache_handler = QuietCacheHandler(cache_path=cache_path)
    
    # Check if we already have a valid cached token
    if os.path.exists(cache_path):
        try:
            # Try to use existing cache first
            auth_manager = SpotifyOAuth(
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
                scope=" ".join(scopes),
                cache_handler=cache_handler,
                open_browser=False  # Never open browser for cached tokens
            )
            
            # Test if cached token works
            token_info = auth_manager.get_cached_token()
            if token_info:
                sp = Spotify(auth_manager=auth_manager)
                # Quick test to see if token works
                user = sp.current_user()
                if user:
                    display_name = user.get('display_name', 'Unknown')
                    print(f"Using cached token for: {display_name}")
                    return sp
        except Exception:
            # Cached token failed, will need fresh auth
            pass
    
    # If we get here, we need fresh authentication
    print("🔑 No valid cached token found. You'll need to authenticate in your browser...")
    print("   This should only happen once, then tokens will be cached.")
    
    auth_manager = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=" ".join(scopes),
        cache_handler=cache_handler,
        open_browser=True  # Only open browser when absolutely necessary
    )
    
    sp = Spotify(auth_manager=auth_manager)
    